import fitz  # PyMuPDF for PDFs
from docx import Document  # For Word files

class Utils:
    @staticmethod
    def extract_text_from_pdf(file):
        """
        Extract text from a PDF file using PyMuPDF.
        Args:
            file: A file-like object representing the PDF.
        Returns:
            str: Extracted text from the PDF.
        """
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in pdf:
            text += page.get_text()
        pdf.close()
        return text

    @staticmethod
    def extract_text_from_word(file):
        """
        Extract text from a Word document using python-docx.
        Args:
            file: A file-like object representing the Word document.
        Returns:
            str: Extracted text from the Word document.
        """
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
