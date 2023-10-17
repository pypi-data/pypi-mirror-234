import time
import ast
from scipy import stats
import difflib
import keyword
import warnings
import datetime
import json
import os
import warnings
from nltk.tokenize import word_tokenize
import numpy as np
import pandas as pd
import calendar
import re
import pkg_resources
pd.set_option('display.max_columns', None)

start = time.time()

from scipy.stats import pearsonr
from tqdm import tqdm
import tensorflow as tf
from nltk.tokenize import word_tokenize
from pickle import load
from sklearn.preprocessing import QuantileTransformer
from pandas.core.indexes.multi import MultiIndex
from collections import OrderedDict

from numpy import linalg
from pickle import dump

#for downloading BERT
from sentence_transformers import SentenceTransformer

#for finding most similar text vectors
from sklearn.metrics.pairwise import cosine_similarity

# Get the directory of the current script
script_dir = os.path.dirname(__file__)
# Construct the path to the CSV file
csv_file_path = os.path.join(script_dir, 'models')

labels = pd.read_csv(csv_file_path+'/lean/labels')['0']
model_path = pkg_resources.resource_filename('bankstatementextractor', 'models/best.pt')

class Incom_expense:   
    def __init__(self):
        pass

    def clean_text(self,text):

        text = re.sub(
            r'(https?(:\/\/)? ?)(www[\.]*)?', '',
            flags=re.IGNORECASE,
            string=re.sub(
                r'[^A-Za-z0-9&%\(\) .]+', '',
                re.sub(
                    r'[\*;:,\-\/\\\[\]_]+', ' ',
                    re.sub(
                        r'-?\d*\.?([\dA-Z]*)?\d+(?!TH|th|ND|nd|ST|st)', '',
                        string=re.sub(
                            r'(^|(?<=[^A-Za-z]))al ', '',
                            flags=re.IGNORECASE,
                            string=re.sub(
                                r'AE *\d[\dA-Z]*', '',
                                re.sub(
                                    r'DMCC', '',
                                    re.sub(
                                        r'LLC', '',
                                        re.sub(
                                            r'NFC[^A-Za-z]', '',
                                            re.sub(
                                                r'SMARTDXBGOV-', '',
                                                flags=re.IGNORECASE,
                                                string=re.sub(
                                                    r'^FAB -', '',
                                                    re.sub(
                                                        r'BNK REF\.', '',
                                                        re.sub(
                                                            r'TXNID\.', '',
                                                            re.sub(
                                                                r'DEBIT', '',
                                                                re.sub(
                                                                    r'V DEBIT', '',
                                                                    re.sub(
                                                                        r'Card Ending with', '',
                                                                        re.sub(
                                                                            r'Visa Purchase', '',
                                                                            re.sub(
                                                                                r'Visa Refund', '',
                                                                                re.sub(
                                                                                    r'Value Date', '',
                                                                                    re.sub(
                                                                                        r'PURCHASE TRXN', '',
                                                                                        re.sub(
                                                                                            r'INTERNET BANKING', '',
                                                                                            re.sub(
                                                                                                r'OUTWARD TT', '',
                                                                                                re.sub(
                                                                                                    r'CARD NO', '',
                                                                                                    re.sub(
                                                                                                        r'PUR ', '',
                                                                                                        re.sub(
                                                                                                            r'CARD TRANSACTION', '',
                                                                                                            re.sub(
                                                                                                                r'DR ATM TRANSACTION', '',
                                                                                                                re.sub(
                                                                                                                    r'OUTWARD UAE FUNDS TRANSFER - IPI', '',
                                                                                                                    re.sub(
                                                                                                                        r'ELECTRON DEBIT CARD TRANSACTION', '',
                                                                                                                        re.sub(
                                                                                                                            r'POS-PURCHASE;CARD NO', '',
                                                                                                                            re.sub(
                                                                                                                                r':AE', '',
                                                                                                                                re.sub(
                                                                                                                                    r'RAK:AE', '',
                                                                                                                                    re.sub(
                                                                                                                                        r'AJMAN', '',
                                                                                                                                        flags=re.IGNORECASE,
                                                                                                                                        string=re.sub(
                                                                                                                                            r'DUBAI', '',
                                                                                                                                            flags=re.IGNORECASE,
                                                                                                                                            string=re.sub(
                                                                                                                                                r'DUBAI:AE', '',
                                                                                                                                                re.sub(
                                                                                                                                                    r'DUBAI ARE', '',
                                                                                                                                                    re.sub(
                                                                                                                                                        r'DXB ARE', '',
                                                                                                                                                        re.sub(
                                                                                                                                                            r'DUBAI *(AE)|(UAE)|(ARE)|(DXB)', '',
                                                                                                                                                            re.sub(
                                                                                                                                                                r'AL AIN', '',
                                                                                                                                                                re.sub(
                                                                                                                                                                    r'AL AIN ARE', '',
                                                                                                                                                                    re.sub(
                                                                                                                                                                        r'AL AIN *(AE)|(UAE)|(ARE)', '',
                                                                                                                                                                        re.sub(
                                                                                                                                                                            r'AL AIN:AE', '',
                                                                                                                                                                            re.sub(
                                                                                                                                                                                r'Ras Al Khaima *(AE)|(UAE)|(ARE)|(RAK)', '',
                                                                                                                                                                                flags=re.IGNORECASE,
                                                                                                                                                                                string=re.sub(
                                                                                                                                                                                    r'FUJAIRAH', '',
                                                                                                                                                                                    re.sub(
                                                                                                                                                                                        r'FUJAIRAH *(AE)|(UAE)|(ARE)|(FUJ)', '',
                                                                                                                                                                                        flags=re.IGNORECASE,
                                                                                                                                                                                        string=re.sub(
                                                                                                                                                                                            r'SHARJAH', '',
                                                                                                                                                                                            flags=re.IGNORECASE,
                                                                                                                                                                                            string=re.sub(
                                                                                                                                                                                                r'SHARJAH ARE', '',
                                                                                                                                                                                                re.sub(
                                                                                                                                                                                                    r'SHARJAH:AE', '',
                                                                                                                                                                                                    re.sub(
                                                                                                                                                                                                        r'SHARJAH *(AE)|(UAE)|(ARE)|(SHJ)', '',
                                                                                                                                                                                                        re.sub(
                                                                                                                                                                                                            r'ABU *DHABI', '',
                                                                                                                                                                                                            flags=re.IGNORECASE,
                                                                                                                                                                                                            string=re.sub(
                                                                                                                                                                                                                r'ABU *DHABI ARE', '',
                                                                                                                                                                                                                re.sub(
                                                                                                                                                                                                                    r'ABU *DHABI:AE', '',
                                                                                                                                                                                                                    re.sub(
                                                                                                                                                                                                                        r'ABU *DHABI *(AE)|(UAE)|(ARE)|(AUH)', '',

                                                                                                                                                                                                                        re.sub(
                                                                                                                                                                                                                            r'BHD', '',
                                                                                                                                                                                                                            re.sub(
                                                                                                                                                                                                                                r'BHD ARE', '',
                                                                                                                                                                                                                                re.sub(
                                                                                                                                                                                                                                    r'BHD', '',
                                                                                                                                                                                                                                    re.sub(
                                                                                                                                                                                                                                        r'AED', '',
                                                                                                                                                                                                                                        str(text).strip(
                                                                                                                                                                                                                                        )
                                                                                                                                                                                                                                    )))))))))))))))))))))))))))))))))))))))))))))))))))))))
        ).strip()

        words = word_tokenize(text)
        result = ' '.join(words)
        return result


    def month_bound(self,x):
        return min(calendar.monthrange(x.year, x.month)[1] - x.day, x.day)

    def consecutive(self,numbers):
        #     numbers = pd.to_datetime(numbers)
        numbers = numbers.drop_duplicates().sort_values()
        max, count_ = 1, 1
        start_idx, end_idx = 0, 0
        for i in range(len(numbers) - 1):
            # if difference between number and his follower is 1,they are in sequence
            if numbers.iloc[i + 1] - numbers.iloc[i] == 1:
                #             print(i)
                count_ = count_ + 1
            else:
                if count_ > max:
                    max = count_
                    end_idx = i
                    start_idx = i + 1 - max
                # Reset counter
                count_ = 1
        return (
            (numbers.iloc[i + 2 - count_], numbers.iloc[i + 1], count_)
            if (max == 1 and count_ != 1)
            else None
            if (max == 1 and count_ == 1)
            else (numbers.iloc[start_idx], numbers.iloc[end_idx], max)
        )


     
    def get_category(self,x):
        global labels
        argmax = np.argmax(x)
        if argmax >= 0 and argmax < len(labels):
            return labels[argmax]
        else:
            return 'Unknown'


    def contains_salary(self,keyword_set):
        return 'salary' in keyword_set   


    def income_detection(self,res_json):
            salary=0
            average_income=0
            model_name = 'places'
            #models
            id = pd.Series(pd.to_numeric(os.listdir(csv_file_path+'/'+model_name), errors='coerce'),).dropna(

            ).sort_values(ascending=False).iloc[0]  
            #models
            places_categories = pd.read_csv(csv_file_path+'/categories.csv',)['0']
            # categories
            places_model = tf.keras.models.load_model(csv_file_path+'/'+model_name+'/'+str(id))

            model_name = 'words'
            id = pd.Series(pd.to_numeric(os.listdir(csv_file_path+'/'+model_name), errors='coerce'),).dropna(

            ).sort_values(ascending=False).iloc[0] 
            # .sort_values()
            words_categories = pd.read_csv(csv_file_path+'/categories.csv',)['0']
            # categories
            words_model = tf.keras.models.load_model(csv_file_path+'/'+model_name+'/'+str(id))

        # try:
            transactions = pd.DataFrame.from_records(ast.literal_eval(res_json))
            transactions_ = transactions[[
                'account_id','name','type', 'iban', 'account_number', 'currency_code', 'bank_name', 'branch', 'address']].drop_duplicates()
            transactions = transactions.rename(columns={
                'name': 'email',
                'account_number': 'account',
            }).drop(['type', 'iban','currency_code', 'bank_name'], axis=1)

            for col in ['description', 'amount', 'currency_code', 
                        'pending',
                        'timestamp', 'account', 'email', 'running_balance',]:
                if(not col in transactions.columns):
                    transactions[col] = pd.Series()
            transactions['timestamp']=transactions['timestamp'].apply(str)
            txs = transactions[(transactions['amount'] < 0)]
            credit = transactions[(transactions['amount'] > 0)]

            transactions_ = transactions_.rename(
                columns={
                    'name':'email'
                }
            )
            accounts = transactions_

            transactions_['account_id'] = transactions_['account_number']
            for col in ['account_id', 'name', 'currency_code', 'type', 'iban', 'account_number',
                        'credit', 'email', 'credit/next_payment_due_amount',
                        'credit/next_payment_due_date']:
                if(not col in transactions_.columns):
                    transactions_[col] = pd.Series()

            accounts['name']=accounts['name'].fillna('')
            accounts["credit"] = accounts["credit"].abs()
            accounts["credit/next_payment_due_amount"] = accounts[
                "credit/next_payment_due_amount"
            ].abs()


            txs['description']=txs['description'].str.strip('#')



            #TODO SmartDXB should be here too
            for prefix in '''GOOGLE \*
            GOOGLE\*
            Microsoft\*
            MICROSOFT\*
            PAYPAL \*
            Payup\*'''.split('\n'):
                txs.loc[#(txs['prefix2'].isna()) &
                        (
                    txs['description'].str.contains(prefix)), 'prefix2'] = prefix


            ## ;
            txs.loc[txs['prefix2'].isna(), 'prefix2'] = txs['description'].apply(lambda x: x.split(';')[0].strip() if (x.split(';')[0]).strip() in '''POS-PURCHASE
            \"POS-PURCHASE
            ONLINE BANKING TRANSFER
            SERVICE CHGS-ATM
            UAE SWITCH WDL
            Transfer between own accounts
            TRANSFER
            DR ATM TRANSACTION
            TELEGRAPHIC TRF
            CREDIT CARD PAYMENT
            DIRECTREMIT
            ATM WITHDRAWAL
            ONLINE BANKING PYMT-TEL
            ONLINE BANKING PYMT
            SALIK PAYMENT
            CLEARING CHEQUE
            INWARD REJECT
            OUTWARD REMITTANCE
            DEWA PAYMENT
            BANKNET TRANSFER
            DIRECT REMITTANCE
            SEWA PAYMENT
            SERVICE CHARGES
            UAE SWITCH ATM WITHDRAWAL
            TELECOM PAYMENT
            Cardless Withdrawal
            INTEREST COLLECTION
            INWARD CLEARING
            UAE SWITCH ENQUIRY CHRG
            Cheque Book Charges
            Online Acct to Acct transfer
            Corr.Bank.Charges
            Funds Transfer
            Charges
            PRINCIPAL DB. TO RETAIL
            INTEREST DB. TO RETAIL
            SUKUK FIN. INSTALLMENT PAYMENT
            INSTALLMENT PLAN EM
            OVERLIMIT FEE CHARGE
            CLEARING CHEQUES
            CHEQUE RETURNED
            LOAN DRAWDOWN
            STANDING ORDER
            WESTERN UNION MOBILE APPS
            INWARD CHQ RETURN
            PURCHASE
            CLEARING CHQ
            ONLINE NOQODI TOP UP
            CHARGE NOQODI TOP UP
            VALUE ADDED TAX
            CASH ADVANCE FEE
            LIV TRANSFER
            EIP INSTALLMENT
            INSTALLMENT PLAN PROCESSING FEE
            FORECLOSURE DEBIT TRANSACTION
            REPLACEMENT CARD FEE
            LOAN CHARGES
            LOAN SETTLEMENT
            LOAN PAYMENT
            LOAN ON CARD PROCESSING FEE
            LOAN ON CARD
            ITM CHEQUE ENCASHMENT
            INTEREST
            COUNTER CHEQUE
            ACCOUNT TRANSFER
            OUTWARD REJECT
            TRANSFER BETWEEN OWN ENBD ACCOUNTS'''.split('\n')
                                                                else np.nan)


            ## *
            #TODO: allow for whee GOOGLE* is not at the beginning
            txs.loc[txs['prefix2'].isna(), 'prefix2'] = txs[txs['prefix2'].isna()
                                                            ]['description'].apply(lambda x: x.split('*')[0].strip() if x.split('*')[0].strip() in '''REVOLUT
            MS
            SharePay
            SHAREPAY
            PayUp
            PAYUP
            MAMO PAY
            FBPAY
            JPAY
            Payex
            ADVANCED MPAY
            PAY
            PAYMOB
            PSP
            PTB
            GOOGLE'''.split('\n') else np.nan)


            ## :

            txs.loc[txs['prefix2'].isna(),'prefix2'] = txs[txs['prefix2'].isna()
                                                        ]['description'].apply(lambda x: x.split(':')[0].strip() if x.split(':')[0].strip() in '''Visa Purchase
            Value Added Tax - Output
            ATM Cash Withdrawal
            ATM Usage Fees
            Online Local Fund Transfer
            Transfer to other FAB account
            Credit Card Payment
            ATM-SWITCH-WITHDRAWAL-CHARGE
            Funds Transfer Charges
            ATM CASH WDL CHG AT UAE SWITCH MEMBER BK
            ATM Withdrawal - FAB ATM
            \"PAYMENT RECEIVED, THANK YOU\"
            AED TRF Within UAE Charges Incl VAT
            DDS Payment
            DU PAYMENT MBA
            Acct to Acct transfer
            Inward Clearing Cheque
            MB BILL DR DU
            MB DR
            Fall Below Fees
            Cardless Cash withdrawal
            Interest
            Breach of Min Balance
            Inward Clearing Return Cheque
            QuickRemit
            QuickRemit Charges
            ONLINE BANKING NOL TOP UP
            DIRECT DEBIT CENTRAL BANK UAEPGS
            Cheque Book Charges
            PRINCIPAL DB. TO RETAIL
            INTEREST DB. TO RETAIL
            SUKUK FIN. INSTALLMENT PAYMENT
            Inward Remittance
            Online International Money Transfer
            Corr.Bank.Charges
            WESTERN UNION MOBILE APPS
            Etisalat Bills
            Du Bills
            DEWA Payment
            MB BILL DR
            MBBILL DR
            IB BILL DR
            Relationship Fee
            ETISALAT PAYMENT MBA
            Inward Clearing Return Charges
            Principal Recovery
            Loan Recovery
            DEWA PAYMENT MBA
            SEWA PAYMENT MBA
            Card Auto Payment
            Standing Orders
            FEWA PAYMENT MBA
            DEWA PAYMENT WWW
            MRTA Insurance Charges
            Statement Charges
            Thank you.Card Payment
            Online Salik Payment
            Sharjah Electricity & Water Auth
            FTS CHARGES
            Instant Card Payment
            LOANRECOVERY-EMI
            #LOANRECOVERY-EMI
            DDS Rejection
            ETISALAT PAYMENT WWW
            Inward posting of cheque
            FEWA BILL PAYMENT
            AJMAN SEWERAGE PAYMENT MBA
            SALIK RECHARGE WWW
            Online Acct to Acct transfer
            Late Payment Fee Charges
            Abu Dhabi Distribution Company MBA
            Cheque Transaction
            FEWA PAYMENT WWW
            SEWA PAYMENT WWW
            Ma'an Donation
            Cash Advance
            Cheque Withdrawal
            Cheque
            Outward Clearing Return Cheque
            Cheque Return Charges
            Misc Charges
            Miscellaneous Charges
            NDRF Loan Recovery
            Profit Recovery
            Cover Account Transaction
            TELEGRAPHIC TRANSFER CHARGES
            Visa Card FEE
            Prepayment Charges
            IB BILL DR DU
            Card Payment by branch
            EMI Postponement Charges
            Al-Ain Payments'''.split('\n') else np.nan)





            for prefix in '''GOOGLE *
            GOOGLE*
            Microsoft*
            MICROSOFT*
            PAYPAL *
            Payup*
            INSTALLMENT PLAN EMI
            Local Transfer
            ELECTRON DEBIT CARD TRANSACTION
            OUTWARD UAE FUNDS
            Value Added Tax
            SWITCH ATM CASH WITHDRAWAL
            ATM CASH WITHDRAWAL
            Electron-Ref
            Social Transfer
            ATM WDL 
            PUR 
            POS-PURCHASE
            POS-
            POS Purchase
            POS 
            PURCHASE TRXN.
            Cash Withdrawal 
            SERVICE CHGS-ATM
            UAE SWITCH WDL
            Transfer to
            International Transfer to
            BILLED FINANCE CHARGES
            Cheque Paid
            Transfer 
            Debit Card Purchase
            \"PAYMENT RECEIVED, THANK YOU\"
            PAYMENT RECEIVED, THANK YOU
            VISA CARD PAYMENT
            MONTHLY ACCOUNT MAINTENANCE FEE
            SMS CHARGES
            SW WDL Chgs
            MB Fund Transfer Debit
            CARD TRANSACTION
            Charges Receivable Recovery
            General AE
            General S
            ATM-
            ATM withdrawal - Other Bank ATM
            LATE PAYMENT
            SWITCH FEE
            SMARTDXBGOV
            SmartDXBGov
            SMARTGOV
            SmartGov
            DIRECT DEBIT TXN - DUBAI EGOV
            VAT 
            \"Loan Transaction,
            Loan Transaction
            ATM BALANCE ENQUIRY CHARGE
            CHEQUE BOOK ISSUANCE
            CHARGE COLLECTION
            \"CHARGE COLLECTION
            ONLINE BANKING
            PAYROLL ACCOUNT MAINTENANCE FEES
            OUTWARD T/T
            STATEMENT CHARGES
            Profit earned
            Correspondent Bank Charges
            Corr.Bank.Charges
            FAB - FUND TRANSFER
            India Online Funds Transfer
            SMART DUBAI GOVERNMENT
            Smart Dubai Government
            OVERLIMIT FEE CHARGE
            OVERLIMIT CHARGE
            PAYMENT TO OWN CREDIT CARD
            CREDIT CARD PAYMNT
            Overlimit Fee
            UAEPGS Transaction
            SALIK RECHARGE MBA
            INTEREST 
            Minimum Balance Charge-
            CREDIT CARD PAYMENT
            Installment Recovery-
            LOAN RECOVERY
            Account Maintenance Fee
            IB FUNDS TRANSFER DEBIT
            UTILITY BILL PAYMENT
            CREDIT CARD RECOVERY
            MOB-CRDPAY
            Credit Card Payment
            CREDIT CARD AUTO PYMT
            OUTWARD TT
            TELEGRAPHIC TRF
            CASH MGMT. SERVICE CHARGES
            EXPRESS TRANSFER
            SwitchATM Withdrawal
            MOBN TRANSFER
            MOBN - INTERNAL TRANSFER
            MOBN - Card Payment
            Standing Order - Utility Bill Payment
            Standing Order
            Instant Transfer
            DEBIT CARD FEE
            TRANSFER International Payment
            TRANSFER AE
            Processing Fees
            PROCESSING FEES
            ATM DECLINE TRANSACTION CHARGE
            RETURNED CHEQUE
            Etisalat PAYMENT
            DU PAYMENT
            CLEARING CHEQUES
            INWARD DIRECT DEBIT
            Utility Bill Payment
            ATM Withdrawal
            PURCHASE 
            CORRESPONDENT BANK CHARGES
            OUTGOING CROSS BORDER TRANSFER
            Red Crescent
            Ma'an Donation
            MB BILL DR
            FUNDS TRANSFER BETWEEN OWN ACCOUNTS
            UAEDDS RTN CHARGES
            FUNDS TRANSFER
            BNKNT UTLTY PYMNT
            LOAN ON CALL EMI
            TFR REV IW IPI PAY REVERSAL
            ATM withdrawal
            ATM ADU Donation
            ATM 
            EPP Booking
            Outward Cheque Returned
            ES Fees
            PAYMENT TO OTHER RAKBANK CREDIT CARD
            Miscellaneous 
            TRANSFER REVERSAL 
            CHEQUE RETURN CHARGE
            DEWA PAYMENT
            ETISALAT PAYMENT
            LOANRECOVERY
            FINANCE CHARGES
            FINANCE CHARGE
            I/W CLEARING CHEQUE
            BILLED PROFIT
            Fund Transfer Charges
            Switch Charge-Txn
            TRANSFER TO 
            TRANSFER To
            Balance Enquiry-ATM
            Fees on Fund transfer 
            Fund transfer 
            DIRECT DEBIT RETURN FEE
            OVER CREDIT LIMIT FEES
            LEDGER FEES
            CBD ATM
            TRANSFER BETWEEN OWN
            ELECTRON CARD REPLACEMENT CHARGES
            Cheque Return Charge
            Utility Payment'''.split('\n'):
                txs.loc[(txs['prefix2'].isna())&(txs['description'].str.startswith(prefix)),'prefix2']=prefix




            for prefix in '''MBTRF
            TRF CORR CHARGE
            TRF :CORR CHARGE
            _IPI_
            ACCOUNT MAINTENANCE
            TEMPORARY HOLD
            TEMPORARYHOLD
            OUTGOING DOMESTIC FUND TRANSFER
            FUND TRANSFER
            Funds Transfer
            FTI-UAE-
            TOC-MAE-
            Payment - 
            TELEX TRANSFER
            CASH WITHDRAWAL
            CC Payment
            Sukuk Processing Fee
            ATM CASH TRANSFER
            Card Replacement
            Domestic Outward Remittance Charges
            PF Processing Fee
            IBTRF
            Domestic Outward Corr.Bank Charges
            GOOGLE \*
            GOOGLE\*'''.split('\n'):
                txs.loc[(txs['prefix2'].isna())&(txs['description'].str.contains(prefix)),'prefix2']=prefix


            txs['stem']=txs['description']
            txs.loc[~txs['prefix2'].isna(),'stem']=txs[~txs['prefix2'].isna()][['description','prefix2']].apply(
                lambda x:x['description'].replace(x['prefix2'].replace('\*','*'),'') ,axis=1)

            text_raw = txs['stem']
            text_BERT = text_raw.apply(self.clean_text)
            txs['clean'] = text_BERT


            purchases=txs[txs['prefix2'].isin([
                'Debit Card Purchase',
                'ELECTRON DEBIT CARD TRANSACTION',
                'POS-PURCHASE',
                'POS-',
                # 'POS-PURCHASE',
                'POS Purchase',
                'POS ',
                'PUR ',
                'PURCHASE TRXN.',
                'Visa Purchase',
                'GOOGLE*',
                'GOOGLE',
                'GOOGLE *',
                'SMARTDXBGOV',
                'SmartDXBGov',
                'SMARTGOV',
                'Smart Dubai Government',
            'SmartGov',
            'SMART DUBAI GOVERNMENT',
            'DIRECT DEBIT TXN - DUBAI EGOV',
            # 'OUTGOING DOMESTIC FUND TRANSFER',
            'FTI-UAE-',
                'TOC-MAE-',
                'Funds Transfer',
                'POS-',
                'Standing Orders',
                'STANDING ORDER',
                'IB FUNDS TRANSFER DEBIT',
                'Payment - ',
                'Microsoft*',
                'MICROSOFT*',
                'PAYPAL *',
                'Payup*',
                'REVOLUT',
                'Instant Transfer',
                'TRANSFER International Payment',
                'TRANSFER AE',
                'MS',
                'Standing Order',
                'PURCHASE',
                'SharePay',
            'SHAREPAY',
            'PayUp',
            'PAYUP',
            'MAMO PAY',
            'FBPAY',
            'JPAY',
            'Payex',
            'ADVANCED MPAY',
            'PAY',
            'PAYMOB',
                'PURCHASE ',

            'PSP',
            'PTB',
                'ACCOUNT TRANSFER',
                'TRANSFER TO ',
                'IBTRF',
                'TRANSFER To',
                'Fund transfer ',
                'GOOGLE \*',
                'GOOGLE\*',
                np.nan
            ])]


            purchases['month_year'] = purchases['timestamp'].apply(
                lambda x: str(x)[:7])

            more_cat = txs.drop(purchases.index)
            more_cat['category'] = more_cat['prefix2'].apply(lambda x: {

            }.get(x, 'Others'))

            purchases['merchant'] = purchases['clean'].dropna().str.lower(
            )
            purchases['words'] = purchases['merchant'].str.split(' ')

            data_dict = pd.DataFrame()
            data_dict['description'] = purchases['merchant'].unique()

            ## Lighter 
            bert_input = data_dict['description'].str.lower().tolist()
            model = SentenceTransformer('paraphrase-mpnet-base-v2')
            embeddings = model.encode(bert_input, show_progress_bar=True)
            embedding_BERT = np.array(embeddings)   

            X = pd.DataFrame(embedding_BERT, index=data_dict['description'])

            test_x = X
            y_pred = words_model.predict(test_x)

            y_pred_binary = (y_pred > 0.5).astype(int)
            y_pred_binary = pd.DataFrame(
                y_pred_binary, columns=places_categories, index=test_x.index).drop(['Others'], axis=1)


            pred = pd.DataFrame(y_pred, columns=words_categories, index=test_x.index).apply(lambda x: places_categories[np.argmax(x)] if np.max(x) > 0.5 else np.nan  # 'Others'  # np.nan
                                                                                            , axis=1)

            purchases['category'] = purchases['merchant'].apply(
                lambda x: pred.loc[x])

            test_x = X
            y_pred = places_model.predict(test_x)

            y_pred_binary = (y_pred > 0.5).astype(int)
            y_pred_binary = pd.DataFrame(
                y_pred_binary, columns=places_categories, index=test_x.index).drop(['Others'], axis=1)


            pred = pd.DataFrame(y_pred, columns=places_categories, index=test_x.index).apply(lambda x: places_categories[np.argmax(x)] if np.max(x) > 0.7 else np.nan  # 'Others'  # np.nan
                                                                                            , axis=1)

            purchases.loc[purchases['category'].isna(), 'category'] = purchases[purchases['category'].isna()]['merchant'].apply(
                lambda x: pred.loc[x])

            purchases['category'] = purchases['category'].fillna('Others')



            txs = credit.rename(columns={'amount_x': 'amount'}).copy()

            accounts_bytheemail = (
                accounts.groupby("email")
                .agg(
                    {
                        "credit": [
                            "sum",
                            #                   'count','mean','min','max'
                        ],
                        "credit/next_payment_due_amount": "sum",
                        "account_number": "nunique",
                        "type": "nunique",
                        "iban": "nunique",
                        "credit/next_payment_due_date": lambda x: (
                            pd.to_datetime(x.dropna(), errors="coerce")
                            .dropna()
                            .apply(self.month_bound)
                            .mean()
                        ),
                        "name": [
                            lambda x: 1 if x.str.lower()
                            .str.contains("liv |neo basic|no min balance")
                            .sum()>0 else 0,
                            lambda x: 1 if x.str.lower().str.contains("neo ").sum()>0 else 0,
                            lambda x: 1 if x.str.lower()
                            .str.contains("platinum|titanium|prime|gold|club|elite|infinite")
                            .sum()>0 else 0,
                            lambda x: 1 if x.str.lower().str.contains("special|classic").sum()>0 else 0,
                            lambda x: 1 if x.str.lower().str.contains("credit").sum()>0 else 0,
                            lambda x: 1 if x.str.lower().str.contains("cashback").sum()>0 else 0,
                            lambda x: 1 if x.str.lower().str.contains("standard").sum()>0 else 0,
                            lambda x: 1 if x.str.lower().str.contains("salary|salaried|pay roll").sum()>0 else 0,
                            lambda x: 1 if x.str.lower().str.contains("current").sum()>0 else 0,
                            lambda x: 1 if x.str.lower().str.contains("investment|trader|trading").sum()>0 else 0,
                            lambda x: 1 if x.str.lower().str.contains("savings|save |saver|s@ver").sum()>0 else 0,
                        ],
                    }
                )
                .reset_index()#.astype('float')
            )
            try:

                accounts_bytheemail["credit_ratio"] = (
                accounts_bytheemail[("credit/next_payment_due_amount", "sum")]
                / accounts_bytheemail[("credit", "sum")]
                ).abs()

            except: 
                accounts_bytheemail["credit_ratio"] = ''

            accounts_bytheemail[("credit_ratio")] = accounts_bytheemail[("credit_ratio")].replace(
                np.inf, 0
            )
            accounts_bytheemail[("credit_ratio")] = accounts_bytheemail[("credit_ratio")].fillna(0)




            txs['timestamp'] = txs['timestamp'].astype('str')

            recalculate = True
            txs["abs_amount"] = txs["amount"].abs()

            all_dup = txs[
                txs.duplicated(
                    subset=["abs_amount", "email", "timestamp", "description"], keep=False
                )
            ]
            txs.drop("abs_amount", axis=1, inplace=True)
            zero_sum = all_dup.drop(
                txs[
                    txs.duplicated(
                        subset=["amount", "email", "timestamp", "description"], keep=False
                    )
                ].index
            )
            zero_sum  # .head(20)

            txs = txs.drop(zero_sum.index)
            txs
            list_of_months = [
                "january",
                "february",
                "march",
                "april",
                "may",
                "june",
                "july",
                "august",
                "september",
                "october",
                "november",
                "december",
            ]
            list_of_months.extend([m[:3] for m in list_of_months])

            list_of_local = [
                "AE",
            ]
            list_of_foreign = ["UK", "US"]  # clashes with us(e.g HOMES R US)
            recent_years = ["2021", "2022", "2023"]

            list_of_online = [r"\.com", "www", "http"]


            keywords = pd.DataFrame(index=txs.index)
            description = txs["description"].str.replace(";", "").str.lower()

            tags = {
                "wage": description.str.contains("wage"),
                "compensation": description.str.contains("compensat"),
                "salary": description.str.contains("salary")
                | (txs["description"].str.contains("WPS|HR") & description.str.contains("sal"))
                | txs["description"].str.contains(
                    r"(?:^|[^a-zA-Z])({})(?=[^a-zA-Z]|$)".format("|".join(["SAL"]))
                ),

                "HR": txs["description"].str.contains(
                    r"(?:^|[^a-zA-Z])({})(?=[^a-zA-Z]|$)".format("|".join(["HR", "HRD"]))
                ),  # ).apply(len)>0,
                "allowance": description.str.contains("allowance")
                | (txs["description"].str.contains("HR") & description.str.contains("allow")),
                "advance": description.str.contains("advance([^a-zA-Z]|$)")
                | (txs["description"].str.contains("HR") & description.str.contains("adv")),
            "bill": description.str.contains(
                    r"(?:^|[^a-zA-Z])({})(?=[^a-zA-Z]|$)".format("|".join(["bill"]))
                ),  # ).apply(len)>0,
                "goods_services": description.str.contains("goods")
                & description.str.contains("bought|sold")
                | (description.replace(" ", "").str.contains("supplier payment")),
                "professional": description.str.contains("professional"),
                "bonus": description.str.contains("bonus")
                & description.str.contains(
                    "performance|hr|payment"
                ),  # TODO: specifically Perfomance buns only
                "overtime": description.str.contains("overtime"),
                "govt": description.str.contains("(gov(?=[^a-zA-Z]|$))|government|govt|ministry"),
                "incentive": description.str.contains("incentive"),
                "deposit": description.str.contains("deposit"),
                "IPI": txs["description"].str.contains("IPI transaction"),
                "cheque": description.str.contains("cheque") | description.str.contains("chq"),
                "cash": description.str.contains("cash") & (~description.str.contains("cashback")),
                "purchase": description.str.contains("purchase")
                | (
                    (txs["description"].str.slice(0, 4) == "PUR ")
                    & (description.str.contains("amazon"))
                ),
                "return": description.str.contains("return")
                | (
                    txs["description"].str.contains("DDS")
                    & (txs["description"].str.contains("DDR|NSF"))
                ),
                "refund": description.str.contains("refund")
                | (
                    (txs["description"].str.slice(0, 4) == "REF ")
                    & (description.str.contains("amazon"))
                ),
                "reversal": description.str.contains("reverse|reversal"),
                "reimburse": description.str.contains("reimburse|reimurse"),
                "claim": description.str.contains("claim"),
                "adjust": description.str.contains("adjustment|credit adj"),
                "card_tx": description.str.contains("card")
                & description.str.contains("transaction|txn|settlement"),
                "electron": description.str.contains(
                    r"(?:^|[^a-zA-Z])({})(?=[^a-zA-Z]|$)".format("|".join(["electron"])))
                & description.str.contains("ref|debit|card|visa"),
                "transfer": description.str.contains("transfer")
                | txs["description"].str.contains("/REF/"),
                "remittance": description.str.contains("remittance"),
                "inward": description.str.contains("inward")
                & (~description.str.contains("remittance")),
                # TODO: add not remittance
                "outward": description.str.contains("outward"),
                "commission": description.str.contains("commission"),
                "payment": description.str.contains("paymen|pymt"),
                "installment": description.str.contains("installment"),
                "rent": description.str.contains("rent") | txs["description"].str.contains("RNT"),
                "transport": description.str.contains("transport"),
                #             |txs['description'].str.contains('RNT'),
                "closure": description.str.contains("closure"),
                "fee": description.str.contains("fee"),
                "interest": description.str.contains("interest"),
                "profit": description.str.contains("profit"),
                "investment": description.str.contains("investm|invest "),
                "financial": description.str.contains("financ|cashback"),
                "saving": description.str.contains("saving|rainy day"),
                "pension": description.str.contains("pension"),
                "verification": description.str.contains("verif"),
                "stand_order": description.str.contains("standing order"),
                "temporary": description.str.contains("temporary")
                | (description.str.contains("temp") & description.str.contains("credit|adj")),
                "insufficient": description.str.contains("insufficient funds"),
                "maid": description.str.contains("maid |maids"),
                "company": description.str.contains(
                    "fze|fzc|llc|fzllc|fz.llc|llc.fz|l l c|l\.l\.c|dmcc|gmbh|ltd|limited|inc([^a-zA-Z]|$)"
                ),
                "benefit": description.str.contains("end.*service.*benefit")
                | description.str.contains("benefits"),
                "family": description.str.contains("family")
                | txs["description"].str.contains(
                    r"(?:^|[^a-zA-Z])({})(?=[^a-zA-Z]|$)".format("|".join(["FAM"]))
                ),
                "loan": description.str.contains("loan|lend|borrow"),
                "credit": description.str.contains("credit"),
                "drawdown": description.str.contains("drawdown"),
                "support": description.str.contains("support"),
                "educ": description.str.contains("education")
                | description.str.contains(
                    r"(?:^|[^a-zA-Z])({})(?=[^a-zA-Z]|$)".format("|".join(["educ", "edu"]))
                ),
                #     'B/O':txs['description'].str.slice(0,3)=='B/O',
                "bonds": description.str.contains("bonds.*redemption"),
                "withdraw": description.str.contains("withdraw")
                | (txs["description"].str.contains("SWITCH WDL")),
                "charge": description.str.contains("charge|corr chg")
                | (txs["description"].str.contains("SERVICE CHG")),
                "brought_over": txs["description"].str.contains(
                    "(^|[^a-zA-Z0-9])B/O([^a-zA-Z0-9])"
                ),
                "FTS": txs["description"].str.contains("FTS"),
                "ATM": txs["description"].str.contains("ATM"),
                "CDM": txs["description"].str.contains("CDM"),
                "telegraphic": txs["description"].str.contains("T/T"),
                "IPI": txs["description"].str.contains(
                    "IPI"
                ),  # TODO: watch out, there's something called IPI payment
                "DDS": txs["description"].str.contains(
                    r"(?:^|[^a-zA-Z])({})(?=[^a-zA-Z]|$)".format("|".join(["DDS"]))
                ),
                #     .str.contains('DDS'),
                #     &(~(txs['description'].str.contains('DDR|NSF'))),
                "invoice": txs["description"].str.contains(
                    r"(?:^|[^a-zA-Z])({})(?=[^a-zA-Z\.][^$a-zA-Z])".format("|".join(["INV"]))
                )
                | description.str.contains("invoice"),
                "POS": txs["description"].str.contains(
                    r"(?:^|[^a-zA-Z])({})(?=[^a-zA-Z]|$)".format("|".join(["POS"]))
                ),  # ).apply(len)>0,
                #     str.contains('POS'),
                "VAT": txs["description"].str.contains(
                    r"(?:^|[^a-zA-Z])({})(?=[^a-zA-Z]|$)".format("|".join(["VAT"]))
                )
                | description.str.contains("value added tax"),
                "UAEFTS": txs["description"].str.contains("UAEFTS"),
                "DIBFTS": txs["description"].str.contains("DIBFTS"),
                #     'DISB':txs['description'].str.contains('DISB')|description.str.contains('disbursement'),
                "disburse":
                #      txs['description'].str.contains('DISB')|
                description.str.contains("disburs"),
                # TODO: watch this
                "mktplace_payer": description.str.contains(
                    "noon e commerce|noonfood|zomato online sales|facebook payout"
                ),
                "gig_payer": description.str.contains("airbnb|booking\.com|souq\.com"),
                "GPSSA": txs["description"].str.contains("GPSSA"),
                "wallet_cash_out": txs["description"].str.contains("MOBILE WALLET CASH OUT"),
                "self": description.str.contains("myself|own acc|my acc")
                | (txs["description"].str.contains("OAT")),
                "local": txs["description"].str.contains(
                    r"(?:^|[^a-zA-Z])({})(?=[^a-zA-Z]|$)".format("|".join(list_of_local))
                ),
                # ).apply(len)>0,
                "foreign": txs["description"].str.contains(
                    r"(?:^|[^a-zA-Z])({})(?=[^a-zA-Z]|$)".format("|".join(list_of_foreign))
                ),
                # ).apply(len)>0,
                "online": description.str.contains(r"({})".format("|".join(list_of_online))),
                # ).apply(len)>0,
                "month": description.str.contains(
                    r"(?:^|[^a-zA-Z0-9])({})(?=[^a-zA-Z]|$)".format("|".join(list_of_months))
                )
                # ).apply(len)>0)
                | description.str.contains(
                    r"((?:^|[^0-9-\/])([0-1][0-9])(-|\/)?(2023|2022))|((2023|2022)(-|\/)?([0-1][0-9])(?=[^0-9-\/]|$))".format(
                        "|".join(recent_years)
                    )
                )
                # ).apply(len)>0)
            } if recalculate else {}
            for tag in tags:
                keywords.loc[tags[tag], tag] = tag

            if(recalculate):
                keywords.loc[(~keywords["purchase"].isna()) & (
                    txs["amount"] > 0), "refund"] = "refund"
                keywords.loc[
                    (~keywords["DIBFTS"].isna()) & (
                        txs["description"].str.slice(0, 5) == "Bonus"),
                    "bonus",
                ] = "bonus"
                keywords.loc[
                    (~keywords["DIBFTS"].isna()) & (
                        txs["description"].str.slice(0, 9) == "Allowance"),
                    "allowance",
                ] = "allowance"

                keywords.loc[txs["description"].str.slice(
                    0, 4) == "REF ", "refund"] = "refund"
                keywords.loc[txs["description"].str.slice(
                    0, 4) == "PUR ", "purchase"] = "purchase"
                keywords.loc[(~keywords["saving"].isna()) &
                            keywords["transfer"], "self"] = "self"

                keywords.to_csv('keywords.csv', index=False)
            else:

                keywords = pd.read_csv('/keywords.csv')

            keywords

            txs["keywords"] = keywords.agg(
                lambda x: ",".join(x.dropna()), axis=1).fillna('')


            # for tag in tqdm(tags):
            #     txs[txs["keywords"].str.contains(tag)][txs["amount"] > 0].to_csv(
            #         "keywords/" + tag + ".csv"
            #     )

            # txs[(txs["keywords"] == "") | txs["keywords"].isna()][txs["amount"] > 0].to_csv(
            #     "no_keywords.csv"
            # )


            txs["month"] = txs["timestamp"].str.slice(5, 7).astype("int")
            txs["day"] = txs["timestamp"].str.slice(8, 10).astype("int")
            txs["date"] = txs["timestamp"].str.slice(0, 10)  # .astype('int')

            # txs[txs['tags']>1]
            txs["keywords"] = txs["keywords"].fillna('')
            txs[txs["keywords"].str.contains("foreign")][txs["amount"] > 0]
            txs[txs["keywords"].str.contains("local")][
                ~txs["keywords"].str.contains(
                    "|".join(
                        [
                            "transfer",
                            "purchase",
                            "withdraw",
                            "salary",
                            "IPI",
                            "fee",
                            "ATM",
                            "self",
                            "refund",
                        ]
                    )
                )
            ][txs["amount"] > 0]

            txs[txs["keywords"].str.contains("online")]["description"].values
            txs[(txs["email"] == "ralzaabi555@gmail.com") & (txs["amount"] > 0)]


            spend = (
                txs[
                    txs["amount"]
                    < 0
                    #           &txs['purchase']
                ]
                .groupby(["email", "month"])["amount"]
                .sum()
            )
            # spend
            credit = txs[
                (txs["amount"] > 0)
                #              & (~txs['refund']) & (~txs['payment']) & (~txs['interest'])
            ]  
            throw_away = credit[
                credit["keywords"].str.contains("purchase")
                | (
                    credit["keywords"].str.contains("return")
                    & credit["keywords"].str.contains("outward|cheque|DDS")
                )
                | credit["keywords"].str.contains("refund")
                | credit["keywords"].str.contains("reversal")
                | credit["keywords"].str.contains("adjust")
                | credit["keywords"].str.contains("card_tx")
                | credit["keywords"].str.contains("electron")
                | (
                    credit["keywords"].str.contains("outward")
                    & credit["keywords"].str.contains("remittance|cheque")
                )
                | (credit["keywords"].str.contains("rent") & credit["keywords"].str.contains("IPI"))
                | (credit["keywords"].str.contains("closure"))
                | (
                    credit["keywords"].str.contains("financial")
                    & (
                        credit["keywords"].str.contains("disburse|charge")
                        | credit["description"].str.lower().str.contains("cashback")
                    )
                )
                | (credit["keywords"].str.contains("verification"))
                | (
                    credit["keywords"].str.contains("temporary")
                    & credit["keywords"].str.contains("credit")
                )
                | (credit["keywords"].str.contains("insufficient"))
                | (
                    credit["keywords"].str.contains("loan")
                    & credit["keywords"].str.contains("IPI|deposit")
                )
                | (credit["keywords"].str.contains("drawdown"))
                | (credit["keywords"].str.contains("withdraw"))
                | (credit["keywords"].str.contains("charge"))
                | (
                    credit["keywords"].str.contains("VAT")
                    #       &credit['keywords'].str.contains('charge|reversal')
                )
                | (
                    credit["keywords"].str.contains("disburse")
                    & credit["keywords"].str.contains("loan|financial")
                )
                | (credit["keywords"].str.contains("self"))
                | (
                    credit["keywords"].str.contains("online")
                    & credit["keywords"].str.contains("card_tx|refund|return|reversal|electron")
                )
            ]

            throw_away.to_csv("throw_away.csv", index=False)
            credit = credit.drop(throw_away.index, axis=0)

            credit["index"] = credit.index


            credit = credit.merge(spend.reset_index(), on=["email", "month"], how="left")
            credit.index = credit["index"]

            credit["perc"] = (credit["amount_x"] / credit["amount_y"].abs() * 100).round(1)



            emails = credit["email"].unique()
            len(emails)

            credit['date'] = pd.to_datetime(credit["date"])

            credit["index"] = credit.index
            samples = []
            groups = []
            counter = 0
            for email in (emails[:] if recalculate else []):
                #     ['zuraimaan@gmail.com']:#
                counter += 1

                sample = credit[credit["email"] == email]
                match = pd.DataFrame()
                for i in sample.index:
                    if i in sample.index:
                        sample["matcher"] = sample.apply(
                            lambda x: difflib.SequenceMatcher(
                                None,
                                re.sub(r"[0-9]+", "", sample.loc[i]
                                    ["description"].lower().replace(";", "")),
                                re.sub(r"[0-9]+", "",
                                    x["description"].lower().replace(";", "")),
                            ),
                            axis=1,
                        )
                        sample["score"] = sample["matcher"].apply(
                            difflib.SequenceMatcher.ratio)

                        matches = pd.concat(
                            [
                                (sample.head(1)),
                                sample.drop(i)[
                                    sample.drop(i).apply(
                                        lambda x: (x["score"] > 0.5  # 0.6#TODO: 0.5
                                                )  # and (abs((sample.loc[i]['day'] +(30 if sample.loc[i]['day']<15 else 0))
                                        #                             -(x['day'] +(30 if x['day']<15 else 0)))%30)<5
                                        ,
                                        axis=1,
                                    )
                                ],
                            ]
                        )          

                        sample = sample.drop(
                            matches.index
                            #                                ,inplace=True
                        )
                        if len(matches) == 1:
                            tx = matches.iloc[0]
                            tx['match_common'] = tx['description']
                            tx["group"] = i
                            tx["month_bound"] = (min(
                                calendar.monthrange(tx["date"].year, tx["date"].month)[
                                    1] - tx["date"].day, tx["date"].day
                            )
                            )
                            samples.append(
                                tx
                                #matches

                            )
                            continue

                        consistency = (
                            pd.to_datetime(matches["date"])
                            .sort_values()
                            .diff()
                            .apply(lambda x: x.days)
                        )
                        #             amt_consistency = (matches['amount_x']).sort_values().diff()#.apply(lambda x:x.days)
                        if len(matches["month"].unique()) > 1 or consistency.sum() >= 25:

                            matches["match_common"] = matches.apply(
                                lambda x: matches.loc[i]["description"][
                                    sorted(
                                        x["matcher"].get_matching_blocks(),
                                        key=lambda y: y[2],
                                        reverse=True,
                                    )[0][0]: sorted(
                                        x["matcher"].get_matching_blocks(),
                                        key=lambda y: y[2],
                                        reverse=True,
                                    )[
                                        0
                                    ][
                                        0
                                    ]
                                    + sorted(
                                        x["matcher"].get_matching_blocks(),
                                        key=lambda y: y[2],
                                        reverse=True,
                                    )[0][2]
                                ],
                                axis=1,
                            )
                            matches["match_diff"] = matches.apply(
                                lambda x: x["description"][
                                    sorted(
                                        x["matcher"].get_matching_blocks(),
                                        key=lambda y: y[2],
                                        reverse=True,
                                    )[0][1]
                                    + sorted(
                                        x["matcher"].get_matching_blocks(),
                                        key=lambda y: y[2],
                                        reverse=True,
                                    )[0][2]:
                                ],
                                axis=1,
                            )

                            matches["group"] = i
                            matches["month_bound"] = (matches["date"]).apply(
                                lambda x: min(
                                    calendar.monthrange(x.year, x.month)[1] - x.day, x.day
                                )
                            )
                            matches["consistency"] = consistency
                            groups.append(matches)


            print(groups)
            if len(groups) > 0 and groups:
                income = pd.concat([pd.concat(groups),
                                    # pd.concat(samples, axis=1).T
                                    ])
                income['iban'] = ''
                income['account_number'] = ''
                income['name'] = ''




                income["match_diff"].fillna("", inplace=True)
                income["keywords"].fillna("", inplace=True)
                # income['acc']=income['name'].str.join(income['bank'])
                income["bankid"] = income["iban"].str.slice(4, 7)

                # TODO: number of days to end of specific month
                income["months_ago"] = (income["date"]).apply(
                    lambda x: (
                        (datetime.datetime.today().year - x.year) * 12
                        + datetime.datetime.today().month
                        - x.month
                    )
                )
                income["months_ago"].value_counts()
                # income[['date','months_ago']]


                global_percentiles = []

                with open("global_percentiles.json", "r") as f:
                    # Write the dictionary to the file in JSON format
                    global_percentiles = json.load(f)

                income['rank'] = (pd.cut((income["amount_x"]), bins=[0]+global_percentiles+[1e23],
                                        labels=range(len([0]+global_percentiles)),#duplicates='raise'
                                        ).astype('int')/len(global_percentiles)
                                )

                income_streams = (
                    income.groupby(["email", "group"])
                    .agg(
                        {
                            "amount_x": [
                                'sum',
                                "mean",
                                "count",
                                "min",
                                "max",
                                "std",
                                "median",
                                #         lambda x: x.quantile(0.25),lambda x: x.quantile(0.75)
                            ],
                            "rank": [
                                #         'mean',
                                "median",
                                #         lambda x: x.quantile(0.25),lambda x: x.quantile(0.75),
                                #         'min','max'
                            ],
                            #     'amount_x':,
                            "day": [
                                "mean",
                                #            pd.Series.mode
                            ],
                            "account_number": "first",
                            "month_bound": [
                                "mean",
                                #                    pd.Series.mode
                            ],
                            #     'date':consecutive,
                            "month": "nunique",
                            "months_ago": [
                                "min",
                                "max",
                                self.consecutive
                                #             '|'.join,
                            ],
                            "consistency": [
                                'sum',
                                #         'mean','std',
                                "median",
                                "mean",
                                "std",
                            ],

                            "match_common": "first",  # ' \ '.join,
                            "match_diff": " \ ".join,
                            "keywords": lambda x: set(",".join(x).split(",")),
                            "name": set,
                            "perc": ["mean", "std", "median"],
                            "bankid": set,
                        }
                    )
                    .merge(accounts_bytheemail, on="email", suffixes=["", "_user"])
                )


                income_streams['amount'] = income_streams.apply(lambda x: x[('amount_x', 'sum')]/(
                    ((x[('consistency', 'sum')])/(365.25/12)+1)) if x[('consistency', 'mean')] > 30 else x[('amount_x', 'sum')]/(
                    x[('months_ago', 'max')]-x[('months_ago', 'min')]+1), axis=1)

                # income_streams[('months_ago','max')]-income_streams[('months_ago','min')]+1)
                income_streams.drop([('amount_x', 'sum')], axis=1, inplace=True)
                income_streams.drop([('consistency', 'sum')], axis=1, inplace=True)
                # income_streams

                income_streams[("credit", "sum")].fillna(0, inplace=True)
                income_streams[("credit_ratio", "")].fillna(0, inplace=True)
                income_streams[("amount_x", "dev")] = (
                    income_streams[("amount_x", "std")] /
                    income_streams[("amount_x", "median")] * 100
                )
                income_streams[("consistency", "dev")] = (
                    income_streams[("consistency", "std")]
                    / income_streams[("consistency", "mean")]
                    * 100
                )
                income_streams["stability"] = (
                    income_streams[("consistency", "dev")] +
                    income_streams[("amount_x", "dev")]
                )
                # income_streams_filtered = income_streams[
                #     #     :
                #     (
                #         ~income_streams[("keywords", "<lambda>")].apply(
                #             lambda x:
                #             ("refund" in x)
                #         )
                #     )
                #     &
                #     (
                #         (income_streams["stability"] <= 103)
                #         | (
                #             (
                #                 (income_streams[("consistency", "dev")] < 20)
                #                 & (
                #                     (income_streams[("month_bound", "mean")] <= 6)
                #                 )

                #             )
                #             | (
                #                 (income_streams[("amount_x", "dev")] <= 25)
                #                 | (
                #                     (income_streams[("amount_x", "dev")] <= 47)
                #                     & (income_streams[("month_bound", "mean")] <= 6)
                #                 )
                #             )
                #         )
                #         | income_streams[("keywords", "<lambda>")].apply(
                #             lambda x:

                #             ("month" in x)
                #         )
                #     )

                # ]  

                income_streams.columns = [
                    "_".join(col).strip() if type(col) is tuple else col
                    for col in income_streams.columns.values
                ]

                columns_to_convert = ['credit_ratio_', 'credit_sum']

                income_streams[columns_to_convert] = income_streams[columns_to_convert].apply(pd.to_numeric, errors='coerce')

                # income_with_auth = income_streams.rename(columns={'email': 'email_'})
                keywds = pd.DataFrame(index=income_streams.index, columns=keywords.columns)
                for key in keywords.columns:
                    keywds[key] = income_streams[("keywords_<lambda>")].apply(
                        lambda x: key in x)


                desc_tags = pd.DataFrame(index=income_streams.index, columns=keywords.columns)

                desc_tags[keywds] = 1
                desc_tags[~keywds] = 0

                # category = "Business"
                desc = desc_tags

                income_train = income_streams.drop(
                    [
                        'email_',
                        'match_common_first',
                        'match_diff_join',
                        'keywords_<lambda>',
                        'name_set',
                        'months_ago_consecutive',
                        'bankid_set',
                        'credit/next_payment_due_date_<lambda>',
                        'account_number_first'
                    ],

                    axis=1,
                )
                

                qt = load(open('qt.pkl', 'rb'))
                income_train = pd.DataFrame(
                    qt.fit_transform(income_train),
                    columns=income_train.columns, index=income_train.index)

                data_x_train = pd.concat(
                    [
                        income_train  
                        ,
                        desc.astype('int'),
                        # nfc_cat.astype('int'),
                    ],
                    ignore_index=False,
                    axis=1,
                )



                fill_with = data_x_train.median(axis=0)

                for c in data_x_train.columns:
                    data_x_train[c].fillna(fill_with[c], inplace=True)


                fill_with.index = [
                    "_".join(col).strip() if type(col) is tuple else col
                    for col in fill_with.index.values
                ]


                for c in data_x_train.columns:
                    data_x_train[c].fillna(fill_with[c], inplace=True)

                model = tf.keras.models.load_model(
                    csv_file_path+'/lean/0.9384675110399379')
                # labels = pd.read_csv('models/lean/labels')['0']


                income_streams['category'] = pd.DataFrame(model.predict(data_x_train)).apply(self.get_category, axis=1)
                #income grouped
                income_streams['type'] = income_streams['category'].apply(
                    lambda x: 'Primary' if x == 'Salary' or x == 'Pension' else 'Secondary')
                income_streams['contains_salary'] = income_streams['keywords_<lambda>'].apply(lambda x: self.contains_salary(x))

                # Check if 'salary' is found in any of the sets
                if income_streams['contains_salary'].any():
                    salary = income_streams[income_streams['contains_salary']]['amount_'].mean()
                    average_income = income_streams.amount_.mean()


            spend_categories = {
                'Food & Drink': 'Variable',
                'Shopping': 'Variable',
                'Groceries': 'Fixed',
                'Others': 'Variable',
                'Transportation': 'Fixed',
                'Subscriptions': 'Fixed',
                'Rent & Utilities': 'Fixed',
                'Medical': 'Variable',
                'Online shopping': 'Variable',
                'Travel':  'Variable',
                'Transfer': 'Variable',
                'Entertainment': 'Variable',
                'Services': 'Variable',
                'Investment': 'Variable',
                'Leisure': 'Variable',
                'Bank fees': 'Variable',
                'Loans': 'Variable',
                'Income': 'Variable',

            }

            #expenses grouped
            purchases['spend_type'] = purchases['category'].apply(
                lambda x: spend_categories[x])

            grouped = purchases.groupby('category')['amount'].sum().reset_index()
            grouped['amount'] = grouped['amount'] * -1
            grouped['percentage'] = grouped['amount'] / -purchases['amount'].sum() * 100

            dict1 = grouped.to_dict(orient='records')

            combined_json = json.dumps({'expenses': dict1, 'salary': salary, 'average_income': average_income}, indent=2)
            print( f"first check:{combined_json}")
            return combined_json

        # except:
        #     #transactions_test2=type(transactions_test2)
        #     print( f"second check:{transactions_test.columns.to_list()}")
           

        



            
