import base64
import cv2
import io
import numpy as np
import re
from datetime import datetime
from PIL import Image

# import fitz  # PyMuPDF library
# import PyPDF2  # PyPDF2 library
import os
import subprocess
import torch
from pdf2image import convert_from_path
from unidecode import unidecode
import pandas as pd
import itertools    
os.sys.path
from io import StringIO


def is_pdf(pdf_bytes):
    try:
        return pdf_bytes[:4] == b'%PDF'
    except Exception as e:
        print("Error in is_pdf_bytes:", e)
        return False
