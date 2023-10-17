#from bsbankspkg import Incom_expense
import Incom_expense


def pdf_to_bytes(pdf_file_path):
    try:
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
        return pdf_bytes
    except FileNotFoundError:
        return None

pdf_file_path = '/Users/nabilalasri/Downloads/Anjali_BS_Extract/ajinsv11@gmail.com.pdf'
pdf_bytes = pdf_to_bytes(pdf_file_path)

result = Incom_expense.Incom_expense().income_detection(pdf_path=pdf_file_path)

