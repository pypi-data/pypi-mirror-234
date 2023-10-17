import Incom_expense
import BanksExtractor


def pdf_to_bytes(pdf_file_path):
    try:
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
        return pdf_bytes
    except FileNotFoundError:
        return None

pdf_file_path = 'abdalla.mharm@gmail.com.pdf'
pdf_bytes = pdf_to_bytes(pdf_file_path)

print('starting test')
res_json = BanksExtractor.BankExtractor().extract(pdf_bytes)
print(res_json)

