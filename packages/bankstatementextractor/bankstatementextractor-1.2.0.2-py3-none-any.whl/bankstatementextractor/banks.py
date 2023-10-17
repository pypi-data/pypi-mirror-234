import base64
import cv2
import io
import numpy as np
import re
from datetime import datetime
from PIL import Image
from bankstatementextractor.banks_utils import *
# from banks_utils import *
import json
import fitz  # PyMuPDF library
import PyPDF2  # PyPDF2 library
import os
import subprocess
import torch
from pdf2image import convert_from_path
from unidecode import unidecode
import pandas as pd
import itertools    
os.sys.path
from io import StringIO
import traceback 

class Banks:

    def __init__(self):
        pass
    # adcb_1
    def adcb_1(self,pdf_bytes):
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            output = []  # Initialize the output list

            for page in doc:
                try:
                    page_output = page.get_text("blocks")
                    output.append(page_output)
                except Exception as e:
                    print(f"Error while processing page: {e}")
                    return None

            plain_text_data = []

            for page_output in output:
                previous_block_id = 0
                page_plain_text_data = []

                for block in page_output:
                    try:
                        if block[6] == 0:
                            if previous_block_id != block[5]:
                                plain_text = unidecode(block[4])
                                page_plain_text_data.append(plain_text)
                                previous_block_id = block[5]
                    except Exception as e:
                        print(f"Error while processing block: {e}")
                        return None

                if 'Consolidated Statement\n' in page_plain_text_data:
                    continue

                page_plain_text_data = [text for text in page_plain_text_data if not text.startswith(('balance', 'opening'))]

                plain_text_data.append(page_plain_text_data)

            account_number = None
            name = None
            opening_balance = None
            closing_balance = None
            currency_code = None

            # Iterate through the first sublist
            for line in plain_text_data[0]:
                try:
                    if line.startswith('Account Name(s)'):
                        name = line.split('\n')[1]
                    elif line.startswith('Account Number'):
                        account_number_with_currency = line.split('\n')[1]
                        account_number = account_number_with_currency.split(' ')[0]
                        currency_code = account_number_with_currency.split(' ')[1]   
                    elif line.startswith('Opening Balance'):
                        opening_balance_with_currency = line.split('\n')[1]
                        opening_balance = float(opening_balance_with_currency.replace(',', '').replace('AED', ''))
                    elif line.startswith('Closing Balance'):
                        closing_balance_with_currency = line.split('\n')[1]
                        closing_balance = float(closing_balance_with_currency.replace(',', '').replace('AED', ''))
                except Exception as e:
                    print(f"Error while processing account info: {e}")
                    return None

            obj = {
                "account_id": "",
                "name": name,
                "currency_code": currency_code,
                "type": "",
                "iban": "",
                "account_number": account_number,
                "bank_name": "ADCB",
                "branch": "",
                "credit": "",
                "address":""
            }       
            new_lst = []

            for sublist in plain_text_data:
                keep = False  # Flag to indicate whether to keep the elements

                for i, element in enumerate(sublist):
                    if element.startswith('Posting Date\nValue Date\nDescription\nRef/Cheque No'):
                        keep = True  
                        new_sublist = sublist[i+1:]  # Create a new sublist starting from the target element
                        break

                if keep:
                    new_lst.append(new_sublist)  # Add the new sublist to the result list if the target element is found


            flat_data = [item for sublist in new_lst for item in sublist]
            split_data = [entry.strip().split('\n') for entry in flat_data]

            lst = []
            current_element = []

            pattern = re.compile(r'^\d{2}/\d{2}/\d{4}')

            for sublist in split_data:
                if pattern.match(sublist[0]):
                    if current_element:
                        lst.append(current_element)
                    current_element = sublist
                else:
                    current_element += sublist

            if current_element:
                lst.append(current_element)

            lst_1 = []

            for sublist in lst:
                if len(sublist) > 6:
                    new_sublist = sublist[:2] + sublist[-3:]
                    new_sublist.insert(2, ' '.join(sublist[2:-3]))
                    lst_1.append(new_sublist)
                else:
                    lst_1.append(sublist)

            # Create a DataFrame with specific column names
            df = pd.DataFrame(lst_1, columns=['timestamp', 'Value Date', 'description',  'debit', 'credit', 'running_balance'])
            df['debit'] = df['debit'].str.replace(',', '').astype(float)
            df['credit'] = df['credit'].str.replace(',', '').astype(float)
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y')
            df['running_balance'] = df['running_balance'].str.replace(',', '').astype(float)
            df['amount'] = df.apply(lambda row: -row['debit'] if row['debit'] != 0 else row['credit'], axis=1)
            for key, value in obj.items():
                df[key] = value
            df.drop(['debit', 'credit','Value Date'], axis=1, inplace = True)
            error_flags = {
                "data_cover_last_3_months": False,
                "statement_extracted_last_7_days": False,
                "outstanding_amount_match": False
            }

            # Check if the data covers the last 3 months
            if (df['timestamp'].max() - df['timestamp'].min()).days < 90:
                error_flags["data_cover_last_3_months"] = True
                print("Error: Upload a 3 months bank statement")
                return None

            # Check if the statement was extracted within the last 7 days of upload
            if (datetime.now().date() - df['timestamp'].max().to_pydatetime().date()).days > 7:
                error_flags["statement_extracted_last_7_days"] = True
                print("Error: Upload a statement extracted within the last 7 days")
                return None

            #Check if the outstanding amount matches the expected total
            if round(abs(df['amount'].sum()), 2) != round(abs(opening_balance - closing_balance), 2):
                error_flags["outstanding_amount_match"] = True
                print("Error: Upload not edited bank statement") 
                None
            
            df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d')
            json_data = df.to_json(orient='records')
            return json_data
        
        except Exception as e:
            print(f"Error during processing: {e}")
            traceback.print_exc()
            return None

    def liv_1(self,pdf_bytes):
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            output = []
            for page in doc:
                page_output = page.get_text("blocks")  # Get the text blocks for each page
                output.append(page_output)  # Append the page output to the main output list

            plain_text_data = []  # Initialize an empty list to store the plain text

            for page_output in output:
                previous_block_id = 0  # Set a variable to mark the block id
                page_plain_text_data = []  # Initialize an empty list to store the plain text for each page

                for block in page_output:
                    if block[6] == 0:  # We only take the text
                        if previous_block_id != block[5]:  # Compare the block number
                            plain_text = unidecode(block[4])
                            page_plain_text_data.append(plain_text)  # Store the plain text in the list for the current page
                            previous_block_id = block[5]  # Update the previous block id

                # Check if 'Consolidated Statement' is present in the sublist and delete the sublist
                if 'Consolidated Statement\n' in page_plain_text_data:
                    continue  # Skip the current page 
                plain_text_data.append(page_plain_text_data)

            # Initialize variables to store information
            name = None
            address = None
            statement_period = None
            account_balance = None
            account_no = None
            iban = None

            # Iterate through the list and search for the respective information
            for item in plain_text_data[0]:
                if item.startswith('Name :'):
                    name = item.split('Name :')[1].replace('\n', '')
                elif item.startswith('Address :'):
                    address = item.split('Address :')[1].replace('\n', '')
                elif item.startswith('Statement period :'):
                    statement_period = item.split('Statement period :')[1].replace('\n', '')
                elif item.startswith('Account balance :'):
                    account_balance = item.split('Account balance :')[1].replace('\n', '')
                elif item.startswith('AccountNo :'):
                    account_no = item.split('AccountNo :')[1].replace('\n', '')
                elif item.startswith('IBAN :'):
                    iban = item.split('IBAN :')[1].replace('\n', '')

            obj = {
                'account_id':'',
                'name': name,
                'currency_code': 'AED',
                'type': '',
                'iban': iban,
                'account_number': account_no,
                'bank_name': 'LIV by ENBD',
                'branch': '',
                'address': address,
                'account_balance': account_balance
            }

            opening_balance_index = next((i for sublist in plain_text_data for i, text in enumerate(sublist) if text.startswith('IBAN :')), -1)

            if opening_balance_index != -1:
                for i in range(len(plain_text_data)):
                # Remove all elements before opening_balance_index + 1 in each sublist
                    plain_text_data[i] = plain_text_data[i][opening_balance_index + 1:]


            plain_text_data = [[element for element in sublist if not element.startswith(('Confirmation of the correctness', 'This statement is generated on', 'Money in'))] for sublist in plain_text_data]
            plain_text_data = list(itertools.chain.from_iterable(plain_text_data))
            plain_text_data = [element.rstrip() for element in plain_text_data]
            plain_text_data = [elem.split('\n') for elem in plain_text_data]

            # Initialize empty lists to store data
            dates = []
            transactions = []
            amounts = []
            balances = []

            # Regex pattern to match date'dd/mm/yyyy'
            date_pattern = r'\d{2}/\d{2}/\d{4}'

            # Initialize a transaction variable to concatenate transaction details
            transaction = ""

            # Iterate through the list
            for item in plain_text_data:
                if re.match(date_pattern, item[0]):
                    # If the item is a date, store it and reset the transaction variable
                    date = item[0]
                    transaction = ""
                else:
                    # Concatenate the elements in the sublist after the date to form the transaction
                    transaction += " ".join(item) + " "

                    # Check if the item contains an amount and balance
                    amount_match = re.search(r'([-+]?\d{1,3}(?:,\d{3})*\.\d+)', item[0])
                    if amount_match:
                        amount = amount_match.group(1).replace(',', '')  # Remove commas
                        balance = item[-1].replace(',', '')  # Remove commas
                        # Append data to respective lists
                        dates.append(pd.to_datetime(date, format='%d/%m/%Y'))
                        transactions.append(transaction.strip())  # Remove trailing spaces
                        amounts.append(pd.to_numeric(amount))
                        balances.append(pd.to_numeric(balance))

            # Create a DataFrame
            df = pd.DataFrame({'timestamp': dates, 'description': transactions, 'amount': amounts, 'running_balance': balances})
            
            
            for key, value in obj.items():
                df[key] = value
            error_flags = {
                "data_cover_last_3_months": False,
                "statement_extracted_last_7_days": False,
                "outstanding_amount_match": False
            }

            # # Check if the data covers the last 3 months
            # if (df['timestamp'].max() - df['timestamp'].min()).days < 90:
            #     error_flags["data_cover_last_3_months"] = True
            #     print("Error: Upload a 3 months bank statement")
            #     return None

            # # Check if the statement was extracted within the last 7 days of upload
            # if (datetime.now().date() - df['timestamp'].max().to_pydatetime().date()).days > 7:
            #     error_flags["statement_extracted_last_7_days"] = True
            #     print("Error: Upload a statement extracted within the last 7 days")
            #     return None

    #         #Check if the outstanding amount matches the expected total
    #         if round(abs(df['amount'].sum()), 2) != round(abs(opening_balance - closing_balance), 2):
    #             error_flags["outstanding_amount_match"] = True
    #             print("Error: Upload not edited bank statement")
                    
            df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d')
            json_data = df.to_json(orient='records')
            print(json_data)
            return json_data

        except Exception as e:
            print(f"Error during processing: {e}")
            traceback.print_exc()
            return None
    
        
    