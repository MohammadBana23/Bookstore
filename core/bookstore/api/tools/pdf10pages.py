import os
from pypdf import PdfReader, PdfWriter
from django.conf import settings

def save_ten_pages_pdf(pdf_path):
    input_pdf = PdfReader(pdf_path)

    output_pdf = PdfWriter()
    for page_num in range(min(10, len(input_pdf.pages))):
        output_pdf.add_page(input_pdf.pages[page_num])
        
    pdf_file_path = pdf_path.split("/")[-1]
    output_file_path = os.path.join(settings.MEDIA_ROOT, 'book_10pages', f'{pdf_file_path.split(".")[0]}-10pages.pdf')
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, 'wb') as output_file:
        output_pdf.write(output_file)

    return output_file_path
