import fitz
from PyPDF2 import PdfReader
import os
import re

class PDFExtractor:
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def extract_text(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        try:
            print("Extracting text from PDF...")
            text = self._extract_with_pymupdf(file_path)
            
            if not text.strip():
                text = self._extract_with_pypdf2(file_path)
            
            cleaned_text = self._clean_text(text)
            
            if not cleaned_text.strip():
                raise Exception("No readable text found in PDF")
            
            print(f"Extracted {len(cleaned_text)} characters")
            return cleaned_text
            
        except Exception as e:
            raise Exception(f"Could not extract text from PDF: {str(e)}")
    
    def _extract_with_pymupdf(self, file_path: str) -> str:
        text = ""
        try:
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception:
            return ""
    
    def _extract_with_pypdf2(self, file_path: str) -> str:
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except Exception:
            return ""
    
    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()
