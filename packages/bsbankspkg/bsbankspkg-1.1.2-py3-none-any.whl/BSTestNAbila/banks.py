
import numpy as np
import re
from datetime import datetime
from PIL import Image
from bsbankspkg.banks_utils import *
import fitz  # PyMuPDF library
import os
from pdf2image import convert_from_path
from unidecode import unidecode
import pandas as pd  
os.sys.path
from io import StringIO

class Banks:

    def __init__(self):
        pass
    # adcb_1
    def adcb_1(self,pdf_path):
        try:
            # Open the PDF file and read it as bytes
            with open(pdf_path, 'rb') as pdf_file:
                pdf_bytes = pdf_file.read()
            
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

            account_num = None
            name = None
            opening_balance = None
            closing_balance = None

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

            # Create a DataFrame with specific column names
            df = pd.DataFrame(split_data, columns=['timestamp', 'Value Date', 'description', 'Ref/Cheque No', 'debit', 'credit', 'running_balance'])
            df['debit'] = df['debit'].str.replace(',', '').astype(float)
            df['credit'] = df['credit'].str.replace(',', '').astype(float)
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y')
            df['running_balance'] = df['running_balance'].str.replace(',', '').astype(float)
            df['amount'] = df.apply(lambda row: -row['debit'] if row['debit'] != 0 else row['credit'], axis=1)
            for key, value in obj.items():
                df[key] = value
            df.drop(['debit', 'credit','Value Date','Ref/Cheque No'], axis=1, inplace = True)
            error_flags = {
                "data_cover_last_3_months": False,
                "statement_extracted_last_7_days": False,
                "outstanding_amount_match": False
            }

            #Check if the data covers the last 3 months
            if (df['timestamp'].max() - df['timestamp'].min()).days < 90:
                error_flags["data_cover_last_3_months"] = True
                print("Error: Upload a 3 months bank statement")
                return None

            #Check if the statement was extracted within the last 7 days of upload
            if (datetime.now().date() - df['timestamp'].max().to_pydatetime().date()).days > 7:
                error_flags["statement_extracted_last_7_days"] = True
                print("Error: Upload a statement extracted within the last 7 days")
                return None

            # Check if the outstanding amount matches the expected total
            if round(df['amount'].sum(), 2) != round(abs(opening_balance - closing_balance), 2):
                error_flags["outstanding_amount_match"] = True
                print("Error: Upload not edited bank statement")

            # If any condition failed (error flag is True), return None
            if any(error_flags.values()):
                return None
            
            df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d')
            json_data = df.to_json(orient='records')
            return json_data
        
        except Exception as e:
            print(f"Error during processing: {e}")
            return None
        
    def process_pdf(self, pdf_path):
        try:
            with open(pdf_path, 'rb') as pdf_file:
                pdf_bytes = pdf_file.read()
            doc = fitz.open(pdf_path)
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
                iban = temp[open_bracket_index + 1:close_bracket_index]  # Extract the text inside the brackets
                account_number = temp[:open_bracket_index]  # Extract the text outside the brackets

            obj = {
                "account_id": "",
                "name": name,
                "currency_code": currency_info,
                "type": account_type,
                "iban": iban,
                "account_number": account_number,
                "bank_name": "ENBD",
                "branch": branch,
                "credit": "",
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

            # Define the date pattern you want to match
            date_pattern = r'\d{2} \w{3} \d{4}'  # Matches the format '03 Mar 2022'

            # Initialize a list to store the indexes of matching sublists
            matching_indexes = []

            # Iterate through the sublists and find matching dates
            for idx, sublist in enumerate(split_data):
                if len(sublist) > 0 and re.match(date_pattern, sublist[0]):
                    matching_indexes.append(idx)

            # Initialize a list to store data for DataFrame
            data = []

            # Initialize variables for amount and running_balance
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
    
        
    