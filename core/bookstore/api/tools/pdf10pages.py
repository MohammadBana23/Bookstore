import io
from pypdf import PdfReader, PdfWriter

def save_ten_pages_pdf(data_bytes, data_name):
    input_pdf = PdfReader(io.BytesIO(data_bytes))
    output_pdf = PdfWriter()
    
    for page_num in range(min(10, len(input_pdf.pages))):
        output_pdf.add_page(input_pdf.pages[page_num])
    
    output_pdf_bytes = io.BytesIO()
    output_pdf.write(output_pdf_bytes)
    output_pdf_bytes.seek(0)  # Reset the stream position to the beginning
    
    data_name = data_name.replace(".", "-10pages.")
    output_pdf_size = len(output_pdf_bytes.getvalue())  # Get the correct size
    
    return output_pdf_bytes, data_name, output_pdf_size
