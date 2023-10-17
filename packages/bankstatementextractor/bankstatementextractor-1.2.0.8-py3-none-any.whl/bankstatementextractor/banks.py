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
    def enbd_1(self,pdf_bytes):
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            plain_text_data = []

            for page in doc:
                page_output = [unidecode(block[4]) for block in page.get_text("blocks") if block[6] == 0]
                plain_text_data.append(page_output)

            # Personal details extraction
            elements_above_target = []

            # Iterate through the elements in the first sublist
            for item in plain_text_data[0]:
                if item.startswith('Date\nDescription\n'):
                    break
                elements_above_target.append(item)
            elements_above_target = [element.replace('\n', ' ') for element in elements_above_target]

            flattened_string = ' '.join(elements_above_target)

            name = None
            branch = None
            opening_balance = None
            account_type = None
            iban = None
            currency_info = None
            account_number = None

            # Check if the flattened string contains the required details
            if 'Name' in flattened_string and 'Branch' in flattened_string and 'Opening Balance' in flattened_string and 'Account Type' in flattened_string and '(IBAN)' in flattened_string and 'Currency' in flattened_string:
                name = flattened_string.split('Name')[1].split('Branch')[0].strip()
                branch = flattened_string.split('Branch')[1].split('Opening Balance')[0].strip()
                opening_balance = flattened_string.split('Opening Balance')[1].strip()
                currency_info = flattened_string.split('Currency')[1].split('Account Number')[0].strip()
                account_type = flattened_string.split('Account Type')[1].split('Name')[0].strip()
                temp = flattened_string.split('(IBAN)')[1].split('Account Type')[0].strip()
                open_bracket_index = temp.find("(")
                close_bracket_index = temp.find(")")
                iban = temp[open_bracket_index + 1:close_bracket_index]  
                account_number = temp[:open_bracket_index]  

            obj = {
                "account_id": "",
                "name": name,
                "currency_code": currency_info,
                "type": account_type,
                "iban": iban,
                "account_number": account_number,
                "bank_name": "ENBD",
                "branch": branch,
                #"credit": "",
                "address": ""
            }

            # Transaction Extraction
            for i, sublist in enumerate(plain_text_data):
                for j, item in enumerate(sublist):
                    if item.startswith('Date\nDescription\nDebit\nCredit\nAccount Balance\n'):
                        # Found the starting element, remove all elements before it
                        plain_text_data[i] = sublist[j + 1:]
                        break

            flat_data = [item for sublist in plain_text_data for item in sublist]
            split_data = [entry.strip().split('\n') for entry in flat_data]

            date_pattern = r'\d{2} \w{3} \d{4}' 


            matching_indexes = []
            for idx, sublist in enumerate(split_data):
                if len(sublist) > 0 and re.match(date_pattern, sublist[0]):
                    matching_indexes.append(idx)
            data = []
            amount = ''
            running_balance = ''
            # Iterate through the indexes of matching sublists
            for idx in matching_indexes:
                try:
                    sublist = split_data[idx]

                    # Extract the date value from the first element that matches the date pattern
                    timestamp = re.search(date_pattern, sublist[0]).group()
                    date_value = pd.to_datetime(timestamp, format='%d %b %Y')

                    # Join the remaining elements in the sublist to form the description
                    description = ' '.join(sublist[1:])

                    # Check if there's a sublist after the current one
                    if idx + 1 < len(split_data):
                        next_sublist = split_data[idx + 1]

                        # Check if the first element of the next sublist matches the amount format
                        if re.match(r'[-]?\d{1,3}(,\d{3})*\.\d{2}', next_sublist[0]):
                            # If yes, add it to the 'amount' column
                            amount = next_sublist[0]

                            # Check if the last element of the next sublist matches the running balance format
                            if re.match(r'AED [-]?\d{1,3}(,\d{3})*\.\d{2}', next_sublist[-1]):
                                # If yes, extract it as 'running_balance'
                                running_balance = next_sublist[-1]

                    # Append the data to the list
                    data.append([timestamp, description, amount, running_balance])
                except Exception as e:
                    print(f"Error while processing transaction data: {e}")

            # Create a DataFrame from the processed data
            df = pd.DataFrame(data, columns=['timestamp', 'description', 'amount', 'running_balance'])
            df['amount'] = df['amount'].str.replace(',', '').astype(float)
            df['running_balance'] = df['running_balance'].str.replace('AED ', '').str.replace(',', '').astype(float)
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d %b %Y', errors='coerce')
            for key, value in obj.items():
                df[key] = value
            error_flags = {
                "data_cover_last_3_months": False,
                "statement_extracted_last_7_days": False,
                "outstanding_amount_match": False
            }

            # Check if the data covers the last 3 months
            if (df['timestamp'].max() - df['timestamp'].min()).days < 90:
                error_flags["data_cover_last_3_months"] = True
                print("Error: Upload a 3 months bank statement")

            # Check if the statement was extracted within the last 7 days of upload
            if (datetime.now().date() - df['timestamp'].max().to_pydatetime().date()).days > 7:
                error_flags["statement_extracted_last_7_days"] = True
                print("Error: Upload a statement extracted within the last 7 days")

            df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d')
            
            json_data = df.to_json(orient='records')
            return json_data

        except Exception as e:
            print(f"Error while processing the PDF: {e}")
            return None
    def adib_1(self, pdf_bytes):
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            output = []

            for page in doc:
                page_output = page.get_text("blocks")
                output.append(page_output)

            plain_text_data = []

            for page_output in output:
                previous_block_id = 0
                page_plain_text_data = []

                for block in page_output:
                    if block[6] == 0:
                        if previous_block_id != block[5]:
                            plain_text = unidecode(block[4])
                            page_plain_text_data.append(plain_text)
                            previous_block_id = block[5]

                if 'Consolidated Statement\n' in page_plain_text_data:
                    continue

                page_plain_text_data = [text for text in page_plain_text_data if not text.startswith(('balance', 'opening'))]

                plain_text_data.append(page_plain_text_data)

            name = None
            address = None
            account_number = None
            acc_type = None
            currency_code = None

            for i, element in enumerate(plain_text_data[0]):
                if element.startswith('Account'):
                    name = plain_text_data[0][i - 2].strip()
                    address = plain_text_data[0][i - 1].strip()
                    account_info = plain_text_data[0][i + 1].strip().split('\n')
                    account_number = account_info[0].strip()
                    acc_type = account_info[1].strip()
                    currency_code = account_info[2].strip()
                else:
                    name = plain_text_data[0][0].split('\n')[0]
                    address = ' '.join(plain_text_data[0][0].split('\n')[1:])
                    account_number = plain_text_data[0][2].split('\n')[0]
                    acc_type = plain_text_data[0][2].split('\n')[1]
                    currency_code =plain_text_data[0][2].split('\n')[2]

            obj = {
                "account_id": "",
                "name": name,
                "currency_code": currency_code,
                "type": acc_type,
                "iban": "",
                "account_number": account_number,
                "bank_name": "ADIB",
                "branch": "",
                #"credit": "",
                "address": address
            }

            flat_data = [item for sublist in plain_text_data for item in sublist]

            ob = r'Opening Balance\n([\d,.]+)'
            opening_balance = None

            for item in flat_data:
                match = re.search(ob, item)
                if match:
                    opening_balance = match.group(1)
                    opening_balance = float(opening_balance.replace(',', ''))
                    break

            cb = r'Closing Balance \n([\d,.]+)'
            closing_balance = None

            for item in flat_data:
                match = re.search(cb, item)
                if match:
                    closing_balance = match.group(1)
                    closing_balance = float(closing_balance.replace(',', ''))
                    break

            pattern = r'(\d{2}-\d{2}-\d{4})\s+([\s\S]*?)\n([\d,]+\.\d{2})\n([\d,]+\.\d{2})'
            matches = re.findall(pattern, '\n'.join(flat_data))
            data_list = []
            previous_amount2 = None

            for match in matches:
                date = match[0]
                description = match[1]
                amount1 = match[2]
                amount2 = match[3]
                amount2_numeric = float(amount2.replace(',', ''))

                if previous_amount2 is not None and amount2_numeric < previous_amount2:
                    amount1 = '-' + amount1

                previous_amount2 = amount2_numeric

                data_list.append((date, description, amount1, amount2))

            columns = ["timestamp", "description", "amount", "running_balance"]
            df = pd.DataFrame(data_list, columns=columns)
            df['amount'] = df['amount'].apply(lambda x: float(x.replace(',', '')))
            df['running_balance'] = df['running_balance'].apply(lambda x: float(x.replace(',', '')))
            df['timestamp'] = pd.to_datetime(df['timestamp'], format="%d-%m-%Y")

            if df.loc[0, 'running_balance'] < opening_balance:
                df.loc[0, 'amount'] = -df.loc[0, 'amount']

            for key, value in obj.items():
                df[key] = value

            error_flags = {
                "data_cover_last_3_months": False,
                "statement_extracted_last_7_days": False,
                "outstanding_amount_match": False
            }

            if (df['timestamp'].max() - df['timestamp'].min()).days < 90:
                error_flags["data_cover_last_3_months"] = True

            if (datetime.now().date() - df['timestamp'].max().to_pydatetime().date()).days > 7:
                error_flags["statement_extracted_last_7_days"] = True

            if round(abs(df['amount'].sum()), 2) != round(abs(opening_balance - closing_balance), 2):
                error_flags["outstanding_amount_match"] = True

            df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%m-%Y')
            print(df)

            json_data = df.to_json(orient='records')
            print(obj)
            
            return json_data

        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def cbd_1(self, pdf_bytes):
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            output = []
            data_ = []
            prev_balance = 0
            pattern = r'^\d{2}/\d{2}/\d{4}'  # Pattern to check if the transaction starts with a date
            count = 0
            name = ''
            currency = ''
            acc_type = ''
            iban = ''
            account_number = ''
            branch = '' 
            
            for page in doc:
                output += page.get_text("blocks")

            for tup in output:
                trans = tup[4].encode("ascii", errors="ignore").decode()

                # TODO: extracting account details
                if count == 2:
                    if trans.startswith('::\n'):
                        branch = output[count+1][4].replace('\n',',').rstrip(',')
                        name = output[count+2][4].strip().split('\n')[1].strip()
                    else:
                        branch = trans.replace('\n',',').rstrip(',')
                        name = output[count+1][4].strip().split('\n')[1].strip()

                if trans.lower().startswith('acct. no.') and account_number == '':
                    account_number = trans.strip().split('\n')[1].strip()

                if trans.lower().startswith('iban') and iban == '':
                    iban = trans.strip().split('\n')[1].strip()
                    acc_type = trans.strip().split('\n')[-1].strip()

                if trans.strip().lower().startswith('currency') and currency == '':
                    currency = trans.strip().split('\n')[1]
                    if "-" in currency:
                        currency = currency[currency.index('-')+1:].strip()

                if trans.strip().startswith('Balance Brought FWD'):
                    prev_balance = float(trans.split('\n')[1].replace(',', ''))

                # TODO: extracting transaction details
                if re.match(pattern, trans):
                    trans_list = trans.split('\n')
                    t_date = trans_list[0]

                    # TODO: extraction of description - number of lines = 1
                    if len(trans_list) == 6:
                        description = trans_list[1]
                        cur_balance = float(trans_list[4].replace(',', ''))

                        # check if the transaction is debit or credit
                        if float(cur_balance) > float(prev_balance):
                            amount = trans_list[3]
                        else:
                            amount = '-' + trans_list[3]

                    # TODO: extraction of description - number of lines = 2
                    elif len(trans_list) == 7:
                        description = trans_list[1] + ' ' + trans_list[2]
                        cur_balance = float(trans_list[5].replace(',', ''))

                        # check if the transaction is debit or credit
                        if float(cur_balance) > float(prev_balance):
                            amount = trans_list[4]
                        else:
                            amount = '-' + trans_list[4]

                    # TODO: extraction of description - number of lines = 3
                    elif len(trans_list) == 8:
                        description = trans_list[1] + ' ' + trans_list[2] + ' ' + trans_list[3] 
                        cur_balance = float(trans_list[6].replace(',', ''))

                        # check if the transaction is debit or credit
                        if float(cur_balance) > float(prev_balance):
                            amount = trans_list[5]
                        else:
                            amount = '-' + trans_list[5]

                    # TODO: extraction of description - number of lines = 4
                    elif len(trans_list) == 9:
                        description = trans_list[1] + ' ' + trans_list[2] + ' ' + trans_list[3] + ' ' + trans_list[4]
                        cur_balance = float(trans_list[7].replace(',', ''))

                        # check if the transaction is debit or credit
                        if float(cur_balance) > float(prev_balance):
                            amount = trans_list[6]
                        else:
                            amount = '-' + trans_list[6]

                    # TODO: extraction of description - number of lines = 5
                    elif len(trans_list) == 10:
                        description = trans_list[1] + ' ' + trans_list[2] + ' ' + trans_list[3] + ' ' + trans_list[4] + ' ' + trans_list[5]
                        cur_balance = float(trans_list[8].replace(',', ''))

                        # check if the transaction is debit or credit
                        if float(cur_balance) > float(prev_balance):
                            amount = trans_list[7]
                        else:
                            amount = '-' + trans_list[7]

                    obj = {
                            'name' : name,
                            'currency_code' : currency,
                            'type' : acc_type,
                            'iban' : iban,
                            'account_number' : account_number,
                            'bank_name' : 'Commercial Bank of Dubai',
                            'branch' : branch,
                            "timestamp": pd.to_datetime(t_date, format='%d/%m/%Y'),
                            "description":description,
                            "amount":amount,
                            "running_balance":cur_balance
                        }
                    data_.append(obj)
                    prev_balance = cur_balance

                count += 1

            df = pd.DataFrame(data_)
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
            
            df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d')
            json_data = df.to_json(orient='records')
            print(json_data)
            return json_data

        except Exception as e:
            print(f"Error during processing: {e}")
            return None
    def adcb_2(self, pdf_bytes):
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            output = []

            for page in doc:
                page_output = page.get_text("blocks")
                output.append(page_output)

            plain_text_data = []

            for page_output in output:
                previous_block_id = 0
                page_plain_text_data = []

                for block in page_output:
                    if block[6] == 0:
                        if previous_block_id != block[5]:
                            plain_text = unidecode(block[4])
                            page_plain_text_data.append(plain_text)
                            previous_block_id = block[5]
                plain_text_data.append(page_plain_text_data)

            iban_pattern = r'IBAN: (AE\d{20})'
            currency_pattern = r'Currency: ([A-Z]{3})'
            branch_pattern = r'Branch: (.*?)\nAccount Title:'
            name_pattern = r'Account Title: (.*)'
            account_details_pattern = r'Account Details: (.*?)\nCurrency:'
            account_merge_split_pattern = r' - '

            for sublist in plain_text_data:
                iban = None
                currency = None
                branch = None
                name = None
                account_merge = None
                account_number = None
                acc_type = None

                for line in sublist:
                    iban_match = re.search(iban_pattern, line)
                    currency_match = re.search(currency_pattern, line)
                    branch_match = re.search(branch_pattern, line)
                    name_match = re.search(name_pattern, line)
                    account_details_match = re.search(account_details_pattern, line)

                    if iban_match:
                        iban = iban_match.group(1)

                    if currency_match:
                        currency = currency_match.group(1)

                    if branch_match:
                        branch = branch_match.group(1)

                    if name_match:
                        name = name_match.group(1)

                    if account_details_match:
                        account_merge = account_details_match.group(1)
                        account_parts = account_merge.split(account_merge_split_pattern)
                        if len(account_parts) == 2:
                            account_number, acc_type = account_parts
                            
                        obj = {
                            "account_id": "",
                            "name": name,
                            "currency_code": currency,
                            "type": acc_type,
                            "iban": iban,
                            "account_number": account_number,
                            "bank_name": "ADCB",
                            "branch": branch,
                            #"credit": "",
                            "address": ""
                        }     

                    if iban and currency and branch and name and account_number and acc_type:
                        break       

            filtered_list = [sublist for sublist in plain_text_data if not any(item.startswith('Consolidated Statement of Accounts') for item in sublist)]
            filtered_list_1 = [[entry for entry in sublist if not entry.startswith(('Total', 'End Of Statement'))] for sublist in filtered_list]
            new_lst = []

            for sublist in filtered_list_1:
                keep = False

                for i, element in enumerate(sublist):
                    if element.startswith('Date\nDescription\nChq/Ref No.'):
                        keep = True
                        new_sublist = sublist[i+2:]
                        break

                if keep:
                    new_lst.append(new_sublist)
            
            flat_data = [item for sublist in new_lst for item in sublist] 
            split_data = [entry.strip().split('\n') for entry in flat_data]

            data = []
            timestamp = None
            value_date = None
            description = None
            ref_cheque_no = None
            running_balance = None
            amount = None

            for sublist in split_data:
                if len(sublist) > 0 and re.match(r'\d{2}/\d{2}/\d{4}', sublist[0]):
                    timestamp = sublist[0]

                if len(sublist) >= 3 and re.match(r'\d{2}/\d{2}/\d{4}', sublist[-3]):
                    value_date = sublist[-3]

                if re.match(r'[-]?\d{1,3}(,\d{3})*\.\d{2}', sublist[-1]):
                    running_balance = sublist[-1]

                if len(sublist) >= 2 and re.match(r'[-]?\d{1,3}(,\d{3})*\.\d{2}', sublist[-2]):
                    amount = sublist[-2]
                description = ' '.join(sublist[1:-3])

                row_data = {
                    'timestamp': timestamp,
                    'Value Date': value_date,
                    'description': description,
                    'Ref/Cheque No': ref_cheque_no,
                    'running_balance': running_balance,
                    'amount': amount
                }

                data.append(row_data)

            df = pd.DataFrame(data, columns=['timestamp', 'description', 'amount', 'running_balance'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y')
            df['running_balance'] = df['running_balance'].str.replace(',', '').astype(float)
            df['amount'] = df['amount'].str.replace(',', '').astype(float)
            for i in range(1, len(df)):
                if df.at[i, 'running_balance'] < df.at[i - 1, 'running_balance']:
                    df.at[i, 'amount'] = -df.at[i, 'amount']
            for key, value in obj.items():
                df[key] = value
            
            error_flags = {
                "data_cover_last_3_months": False,
                "statement_extracted_last_7_days": False,
                "outstanding_amount_match": False
            }

            if (df['timestamp'].max() - df['timestamp'].min()).days < 90:
                error_flags["data_cover_last_3_months"] = True
                print("Error: Upload a 3 months bank statement")

            if (datetime.now().date() - df['timestamp'].max().to_pydatetime().date()).days > 7:
                error_flags["statement_extracted_last_7_days"] = True
                print("Error: Upload a statement extracted within the last 7 days")

            df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d')
            json_data = df.to_json(orient='records')

            return json_data

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
