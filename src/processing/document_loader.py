"""
Document Loader Module
Handles loading various document formats (PDF, DOCX, TXT, CSV)
"""
import os
from typing import Dict, List
from pathlib import Path
import PyPDF2
from docx import Document
import csv


class DocumentLoader:
    """Load and extract text from various document formats"""
    
    SUPPORTED_FORMATS = ['.pdf', '.docx', '.txt', '.doc', '.csv']
    
    def __init__(self):
        self.loaded_documents = {}
    
    def load_file(self, file_path: str) -> Dict[str, any]:
        """
        Load a document file and extract its text content
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Dictionary containing document metadata and text
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = file_path.suffix.lower()
        
        if file_extension not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Extract text based on file type
        if file_extension == '.pdf':
            text = self._load_pdf(file_path)
        elif file_extension in ['.docx', '.doc']:
            text = self._load_docx(file_path)
        elif file_extension == '.txt':
            text = self._load_txt(file_path)
        elif file_extension == '.csv':
            text = self._load_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Create metadata
        metadata = {
            'filename': file_path.name,
            'file_path': str(file_path),
            'file_type': file_extension,
            'file_size': file_path.stat().st_size,
            'text': text,
            'text_length': len(text),
            'word_count': len(text.split())
        }
        
        self.loaded_documents[file_path.name] = metadata
        return metadata
    
    def _load_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        text = []
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text.append(page.extract_text())
            
            return '\n\n'.join(text)
        except Exception as e:
            raise Exception(f"Error loading PDF: {str(e)}")
    
    def _load_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text.append(paragraph.text)
            
            return '\n\n'.join(text)
        except Exception as e:
            raise Exception(f"Error loading DOCX: {str(e)}")
    
    def _load_txt(self, file_path: Path) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
    
    def _load_csv(self, file_path: Path) -> str:
        """Extract text from CSV file"""
        try:
            text_parts = []
            
            with open(file_path, 'r', encoding='utf-8', newline='') as file:
                csv_reader = csv.reader(file)
                
                # Get headers
                try:
                    headers = next(csv_reader)
                    text_parts.append(f"CSV File: {file_path.name}")
                    text_parts.append(f"Columns: {', '.join(headers)}")
                    text_parts.append("\n" + "="*50 + "\n")
                    
                    # Process each row
                    for row_num, row in enumerate(csv_reader, start=1):
                        # Create structured text from row
                        row_text = []
                        for header, value in zip(headers, row):
                            if value.strip():  # Only include non-empty values
                                row_text.append(f"{header}: {value}")
                        
                        if row_text:
                            text_parts.append(f"Row {row_num}:\n" + "\n".join(row_text))
                            text_parts.append("")  # Empty line between rows
                    
                except StopIteration:
                    # Empty CSV file
                    return f"Empty CSV file: {file_path.name}"
            
            return "\n".join(text_parts)
            
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1', newline='') as file:
                csv_reader = csv.reader(file)
                headers = next(csv_reader)
                text_parts = [f"Columns: {', '.join(headers)}\n"]
                
                for row_num, row in enumerate(csv_reader, start=1):
                    row_text = [f"{h}: {v}" for h, v in zip(headers, row) if v.strip()]
                    if row_text:
                        text_parts.append(f"Row {row_num}:\n" + "\n".join(row_text) + "\n")
                
                return "\n".join(text_parts)
    
    def get_supported_formats(self) -> List[str]:
        """Return list of supported file formats"""
        return self.SUPPORTED_FORMATS
    
    def clear_cache(self):
        """Clear loaded documents cache"""
        self.loaded_documents = {}


