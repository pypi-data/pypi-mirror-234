import base64
import cv2
import io
import numpy as np
import re
from datetime import datetime
from PIL import Image
from pdf2image import convert_from_bytes

from bankstatementextractor.banks_utils import *
from bankstatementextractor.banks import Banks
import bankstatementextractor.constants as const
from bankstatementextractor.Incom_expense import Incom_expense

# from banks_utils import *
# from banks import Banks
# import constants as const
# from Incom_expense import Incom_expense

import os
import subprocess
import torch 
os.sys.path
from io import BytesIO
import pkg_resources


class BankExtractor:

    def __init__(self):
        """
        This is the initialization function of a class that imports a spoof model and loads an BS
        extractor.
        """
        # self.bank_labels = ["adib_1","cbd_1","liv_1"]
    
    def __check_pdf_metadata(self, pdf_bytes):
        try:
            # Run the pdfinfo command with input as bytes
            # print('before run')
            pdfinfo_process = subprocess.run(["pdfinfo", "-"], input=pdf_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if pdfinfo_process.returncode != 0:
                return False, "pdfinfo command failed."

            pdfinfo_output = pdfinfo_process.stdout
            # print(pdfinfo_output)
        except FileNotFoundError:
            return False, "pdfinfo command not found. Make sure it's installed and in your PATH."
        # Extract the creator and producer strings, created_at, and modified_at from the pdfinfo output
        creator_string = None
        producer_string = None
        created_at = None
        modified_at = None

        for line in pdfinfo_output.splitlines():
            line_str = line.decode('utf-8')  # Convert bytes to string
            if line_str.startswith("Creator:"):
                creator_string = line_str[len("Creator:"):].strip()
            elif line_str.startswith("Producer:"):
                producer_string = line_str[len("Producer:"):].strip()
            elif line_str.startswith("CreationDate:"):
                created_at = line_str[len("CreationDate:"):].strip()
            elif line_str.startswith("ModDate:"):
                modified_at = line_str[len("ModDate:"):].strip()

        crt_list_good= const.creator_lst_good
        crt_list_bad=const.creator_lst_bad
        prod_list_good=const.producer_lst_good
        prod_list_bad=const.producer_lst_bad
        # Check conditions based on the presence of strings in the lists and created/modified timestamps
        if creator_string in crt_list_good and producer_string in prod_list_good:
            return True, None
        elif creator_string in crt_list_good and producer_string in prod_list_bad:
            return False, "Upload a non-edited PDF"
        elif creator_string in crt_list_bad and producer_string in prod_list_good:
            return False, "Upload a non-edited PDF"
        elif creator_string in crt_list_bad and producer_string in prod_list_bad:
            return False, "Upload a non-edited PDF"
        elif creator_string not in crt_list_good + crt_list_bad and producer_string in prod_list_good:
            if created_at == modified_at:
                return True, None
            else:
                return False, "Upload a non-edited PDF"
        elif creator_string not in crt_list_good + crt_list_bad and producer_string in prod_list_bad:
            return False, "Upload a non-edited PDF"
        elif creator_string in crt_list_good and producer_string not in prod_list_good + prod_list_bad:
            if created_at == modified_at:
                return True, None
            else:
                return False, "Upload a non-edited PDF"
        elif creator_string in crt_list_bad and producer_string not in prod_list_good + prod_list_bad:
            return False, "Upload a non-edited PDF"
        else:
            if created_at == modified_at:
                return True, None
            else:
                return False, "Upload a non-edited PDF"
        
        # return result, message, metadata

    # Function to convert PDF to images using pdf2image library
    def convert_pdf_to_images(self, pdf_content_stream):
        try:
            images = convert_from_bytes(pdf_content_stream.read(), dpi=300)
            return images
        except Exception as e:
            return []
    
    def __process_pdf_and_detect_labels(self, pdf_content, confidence_threshold=0.85):
        try:
            # Convert the PDF content bytes into a readable stream
            pdf_content_stream = BytesIO(pdf_content)

            # Convert the first page of the PDF to an image
            images = self.convert_pdf_to_images(pdf_content_stream)

            if images:
                # Convert PIL image to a bytes-like object
                img_byte_array = BytesIO()
                images[0].save(img_byte_array, format='JPEG')
                img_byte_array.seek(0)
                # print(f"img arr: {img_byte_array}")

                # Load the YOLOv5 model
                model_path = pkg_resources.resource_filename('bankstatementextractor', 'models/best.pt')
                model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

                # Load the image from the bytes-like object
                img = Image.open(img_byte_array)

                # Perform inference
                results = model(img)

                # Get bounding box coordinates, confidence scores, and labels
                boxes = results.pred[0][:, :4].cpu().numpy()
                confidences = results.pred[0][:, 4].cpu().numpy()
                labels = results.pred[0][:, 5].cpu().numpy().astype(int)

                detected_labels = []

                # Filter detections based on confidence threshold and collect labels
                for box, confidence, label in zip(boxes, confidences, labels):
                    if confidence >= confidence_threshold:
                        label_name = model.names[label]
                        detected_labels.append(label_name)

                return detected_labels
            else:
                return []
        except Exception as e:
            return []
            
            
    def extract(self, pdf_bytes):
        data=None
        res={}
        # Check PDF metadata
        metadata_result, metadata_message = self.__check_pdf_metadata(pdf_bytes)
        if metadata_result:
            # Process PDF and detect labels
            detected_labels = self.__process_pdf_and_detect_labels(pdf_bytes)
            if detected_labels and len(detected_labels)==1:
                print("Detected Labels:", detected_labels)
                banks = Banks()
                label = detected_labels[0]
                if label in const.bank_labels:
                    data=getattr(banks, label)(pdf_bytes)
                else:
                    print(f"No function found for label: {label}")
            else:
                print("No labels detected.")
        else:
            print("Metadata Check Failed:", metadata_message)

        if data:
            res=Incom_expense().income_detection(data)
        return res
        
