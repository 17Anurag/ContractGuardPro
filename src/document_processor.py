"""
Document Processing Module
Handles extraction of text from various document formats
"""
import PyPDF2
import pdfplumber
from docx import Document
import hashlib
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Processes various document formats for contract analysis"""
    
    def __init__(self, max_file_size_mb: int = 10):
        """Initialize document processor"""
        self.max_file_size_bytes = max_file_size_mb * 1024 * 1024
        self.supported_formats = ['.pdf', '.docx', '.txt']

    def validate_file(self, file_path: str) -> Tuple[bool, str]:
        """Validate file format and size"""
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > self.max_file_size_bytes:
            return False, f"File size ({file_size/1024/1024:.1f}MB) exceeds maximum allowed size"
        
        # Check file extension
        _, ext = os.path.splitext(file_path.lower())
        if ext not in self.supported_formats:
            return False, f"Unsupported file format. Supported formats: {', '.join(self.supported_formats)}"
        
        return True, "File validation passed"

    def extract_text_from_pdf(self, file_path: str) -> Tuple[str, Dict]:
        """Extract text from PDF file"""
        text = ""
        metadata = {"pages": 0, "extraction_method": ""}
        
        try:
            # Try pdfplumber first (better for complex layouts)
            with pdfplumber.open(file_path) as pdf:
                pages_text = []
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        pages_text.append(page_text)
                
                if pages_text:
                    text = "\n\n".join(pages_text)
                    metadata["pages"] = len(pages_text)
                    metadata["extraction_method"] = "pdfplumber"
                    logger.info(f"Extracted text from {len(pages_text)} pages using pdfplumber")
                    return text, metadata
        
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {str(e)}, trying PyPDF2")
        
        try:
            # Fallback to PyPDF2
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pages_text = []
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        pages_text.append(page_text)
                
                text = "\n\n".join(pages_text)
                metadata["pages"] = len(pages_text)
                metadata["extraction_method"] = "PyPDF2"
                logger.info(f"Extracted text from {len(pages_text)} pages using PyPDF2")
        
        except Exception as e:
            logger.error(f"PDF extraction failed with both methods: {str(e)}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
        
        return text, metadata

    def extract_text_from_docx(self, file_path: str) -> Tuple[str, Dict]:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            paragraphs = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    paragraphs.append(paragraph.text)
            
            text = "\n\n".join(paragraphs)
            
            metadata = {
                "paragraphs": len(paragraphs),
                "extraction_method": "python-docx"
            }
            
            logger.info(f"Extracted text from DOCX with {len(paragraphs)} paragraphs")
            return text, metadata
        
        except Exception as e:
            logger.error(f"DOCX extraction failed: {str(e)}")
            raise Exception(f"Failed to extract text from DOCX: {str(e)}")

    def extract_text_from_txt(self, file_path: str) -> Tuple[str, Dict]:
        """Extract text from TXT file"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        text = file.read()
                    
                    metadata = {
                        "encoding": encoding,
                        "extraction_method": "text_file"
                    }
                    
                    logger.info(f"Extracted text from TXT file using {encoding} encoding")
                    return text, metadata
                
                except UnicodeDecodeError:
                    continue
            
            raise Exception("Could not decode text file with any supported encoding")
        
        except Exception as e:
            logger.error(f"TXT extraction failed: {str(e)}")
            raise Exception(f"Failed to extract text from TXT: {str(e)}")

    def process_document(self, file_path: str) -> Dict:
        """Main document processing function"""
        logger.info(f"Processing document: {file_path}")
        
        # Validate file
        is_valid, validation_message = self.validate_file(file_path)
        if not is_valid:
            raise ValueError(validation_message)
        
        # Generate document hash for audit trail
        doc_hash = self.generate_document_hash(file_path)
        
        # Extract text based on file type
        _, ext = os.path.splitext(file_path.lower())
        
        if ext == '.pdf':
            text, extraction_metadata = self.extract_text_from_pdf(file_path)
        elif ext == '.docx':
            text, extraction_metadata = self.extract_text_from_docx(file_path)
        elif ext == '.txt':
            text, extraction_metadata = self.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
        
        # Validate extracted text
        if not text or len(text.strip()) < 100:
            raise ValueError("Insufficient text extracted from document. Please ensure the document contains readable text.")
        
        # Prepare result
        result = {
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
            "file_size_bytes": os.path.getsize(file_path),
            "file_type": ext,
            "document_hash": doc_hash,
            "extracted_text": text,
            "text_length": len(text),
            "word_count": len(text.split()),
            "extraction_metadata": extraction_metadata,
            "processed_at": datetime.now().isoformat()
        }
        
        logger.info(f"Document processing completed. Text length: {len(text)} characters")
        return result

    def generate_document_hash(self, file_path: str) -> str:
        """Generate SHA-256 hash of document for audit trail"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.error(f"Failed to generate document hash: {str(e)}")
            return "hash_generation_failed"

    def extract_document_metadata(self, text: str) -> Dict:
        """Extract basic metadata from document text"""
        import re
        
        metadata = {
            "parties": [],
            "dates": [],
            "monetary_amounts": [],
            "key_terms": []
        }
        
        # Extract potential party names (basic pattern matching)
        party_patterns = [
            r"between\s+([A-Z][A-Za-z\s&.,]+?)\s+and\s+([A-Z][A-Za-z\s&.,]+?)(?:\s|,|\.|;)",
            r"party of the first part[:\s]+([A-Z][A-Za-z\s&.,]+?)(?:\s|,|\.|;)",
            r"party of the second part[:\s]+([A-Z][A-Za-z\s&.,]+?)(?:\s|,|\.|;)"
        ]
        
        for pattern in party_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    metadata["parties"].extend([m.strip() for m in match if m.strip()])
                else:
                    metadata["parties"].append(match.strip())
        
        # Extract dates
        date_patterns = [
            r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
            r"\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{2,4}"
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            metadata["dates"].extend(matches)
        
        # Extract monetary amounts
        money_patterns = [
            r"₹\s*[\d,]+(?:\.\d{2})?",
            r"Rs\.?\s*[\d,]+(?:\.\d{2})?",
            r"rupees?\s+[\d,]+",
            r"\$\s*[\d,]+(?:\.\d{2})?"
        ]
        
        for pattern in money_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            metadata["monetary_amounts"].extend(matches)
        
        # Extract key terms (basic)
        key_term_patterns = [
            r"term(?:s)?\s*:?\s*(\d+\s+(?:days?|weeks?|months?|years?))",
            r"duration\s*:?\s*(\d+\s+(?:days?|weeks?|months?|years?))",
            r"notice\s+period\s*:?\s*(\d+\s+(?:days?|weeks?|months?))"
        ]
        
        for pattern in key_term_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            metadata["key_terms"].extend(matches)
        
        # Remove duplicates and clean up
        for key in metadata:
            if isinstance(metadata[key], list):
                metadata[key] = list(set([item.strip() for item in metadata[key] if item.strip()]))
        
        return metadata

    def preprocess_text_for_analysis(self, text: str) -> str:
        """Preprocess extracted text for better analysis"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers/footers (basic patterns)
        text = re.sub(r'Page\s+\d+\s+of\s+\d+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        
        # Normalize common legal abbreviations
        abbreviations = {
            r'\bvs?\.\b': 'versus',
            r'\betc\.\b': 'etcetera',
            r'\bi\.e\.\b': 'that is',
            r'\be\.g\.\b': 'for example',
            r'\bw\.r\.t\.\b': 'with respect to'
        }
        
        for abbrev, full_form in abbreviations.items():
            text = re.sub(abbrev, full_form, text, flags=re.IGNORECASE)
        
        return text.strip()