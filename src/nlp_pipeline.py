"""
NLP Pipeline for Legal Contract Processing
Handles contract parsing, entity extraction, and clause analysis
"""
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import spaCy, but don't fail if it's not available
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    logger.warning("spaCy not available. Using basic NLP processing.")

@dataclass
class ContractEntity:
    """Represents an extracted entity from contract"""
    text: str
    label: str
    start: int
    end: int
    confidence: float = 0.0

@dataclass
class ContractClause:
    """Represents a contract clause with metadata"""
    text: str
    clause_type: str
    section: str
    risk_level: str
    obligations: List[str]
    rights: List[str]
    prohibitions: List[str]

class LegalNLPPipeline:
    """Main NLP pipeline for contract analysis"""
    
    def __init__(self):
        """Initialize the NLP pipeline"""
        self.nlp = None
        if SPACY_AVAILABLE:
            try:
                # Try to load spaCy model
                self.nlp = spacy.load("en_core_web_sm")
                logger.info("SpaCy model loaded successfully")
            except OSError:
                logger.warning("SpaCy model not found. Using basic NLP processing.")
        else:
            logger.info("SpaCy not available. Using basic NLP processing.")
        
        # Initialize NLTK as fallback if available
        if self.nlp is None:
            try:
                import nltk
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                nltk.download('averaged_perceptron_tagger', quiet=True)
                logger.info("NLTK initialized as fallback")
            except ImportError:
                logger.warning("Neither spaCy nor NLTK available. Using basic text processing.")
        
        # Contract type patterns
        self.contract_patterns = {
            "Employment Agreement": [
                r"employment agreement", r"employment contract", r"job offer",
                r"appointment letter", r"service agreement.*employee"
            ],
            "Vendor/Supplier Contract": [
                r"vendor agreement", r"supplier contract", r"purchase order",
                r"supply agreement", r"procurement contract"
            ],
            "Lease & Rental Agreement": [
                r"lease agreement", r"rental agreement", r"tenancy agreement",
                r"lease deed", r"rent agreement"
            ],
            "Partnership Deed": [
                r"partnership deed", r"partnership agreement", r"joint venture",
                r"collaboration agreement"
            ],
            "Service Agreement": [
                r"service agreement", r"consulting agreement", r"professional services",
                r"service contract", r"work order"
            ],
            "NDA/Confidentiality Agreement": [
                r"non.disclosure agreement", r"confidentiality agreement", r"nda",
                r"secrecy agreement", r"proprietary information"
            ]
        }
        
        # Legal entity patterns
        self.entity_patterns = {
            "PARTY": [
                r"party of the first part", r"party of the second part",
                r"the company", r"the employee", r"the contractor",
                r"the vendor", r"the client", r"the lessor", r"the lessee"
            ],
            "MONETARY": [
                r"₹\s*[\d,]+", r"rs\.?\s*[\d,]+", r"rupees?\s+[\d,]+",
                r"\$\s*[\d,]+", r"usd\s*[\d,]+", r"dollars?\s+[\d,]+"
            ],
            "DATE": [
                r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
                r"\d{1,2}\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{2,4}",
                r"(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{2,4}"
            ],
            "DURATION": [
                r"\d+\s+(days?|weeks?|months?|years?)",
                r"(one|two|three|four|five|six|seven|eight|nine|ten)\s+(days?|weeks?|months?|years?)"
            ]
        }
        
        # Clause type patterns
        self.clause_patterns = {
            "TERMINATION": [
                r"termination", r"terminate", r"end.*agreement",
                r"expiry", r"dissolution", r"breach.*terminate"
            ],
            "PAYMENT": [
                r"payment", r"salary", r"compensation", r"remuneration",
                r"fees?", r"amount", r"consideration"
            ],
            "LIABILITY": [
                r"liability", r"liable", r"responsible", r"damages",
                r"indemnity", r"indemnification", r"loss"
            ],
            "CONFIDENTIALITY": [
                r"confidential", r"proprietary", r"trade secret",
                r"non.disclosure", r"secrecy"
            ],
            "INTELLECTUAL_PROPERTY": [
                r"intellectual property", r"copyright", r"trademark",
                r"patent", r"trade mark", r"ip rights"
            ],
            "NON_COMPETE": [
                r"non.compete", r"restraint.*trade", r"competition",
                r"solicit.*employee", r"solicit.*client"
            ]
        }

    def normalize_hindi_text(self, text: str) -> str:
        """Convert Hindi text to English for processing"""
        # Basic transliteration - in production, use proper Hindi NLP
        # This is a placeholder for Hindi processing
        hindi_to_english = {
            "करार": "agreement",
            "अनुबंध": "contract", 
            "पार्टी": "party",
            "कंपनी": "company",
            "कर्मचारी": "employee"
        }
        
        for hindi, english in hindi_to_english.items():
            text = text.replace(hindi, english)
        
        return text

    def classify_contract_type(self, text: str) -> Tuple[str, float]:
        """Classify the type of contract"""
        text_lower = text.lower()
        scores = {}
        
        for contract_type, patterns in self.contract_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower, re.IGNORECASE))
                score += matches
            scores[contract_type] = score
        
        if not scores or max(scores.values()) == 0:
            return "Unknown", 0.0
        
        best_type = max(scores, key=scores.get)
        confidence = min(scores[best_type] / 10.0, 1.0)  # Normalize to 0-1
        
        return best_type, confidence

    def extract_entities(self, text: str) -> List[ContractEntity]:
        """Extract named entities from contract text"""
        entities = []
        
        # Use spaCy NER if available
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ["PERSON", "ORG", "MONEY", "DATE", "GPE"]:
                    entities.append(ContractEntity(
                        text=ent.text,
                        label=ent.label_,
                        start=ent.start_char,
                        end=ent.end_char,
                        confidence=0.8
                    ))
        else:
            # Fallback to basic pattern matching
            logger.info("Using basic pattern matching for entity extraction")
        
        # Custom pattern matching for legal entities (always run)
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    entities.append(ContractEntity(
                        text=match.group(),
                        label=entity_type,
                        start=match.start(),
                        end=match.end(),
                        confidence=0.7
                    ))
        
        return entities

    def segment_clauses(self, text: str) -> List[str]:
        """Segment contract into individual clauses"""
        # Split by common clause indicators
        clause_separators = [
            r'\n\s*\d+\.',  # Numbered clauses
            r'\n\s*\([a-z]\)',  # Lettered sub-clauses
            r'\n\s*[A-Z][A-Z\s]+:',  # Section headers
            r'\n\s*WHEREAS',  # Whereas clauses
            r'\n\s*NOW THEREFORE',  # Therefore clauses
        ]
        
        # Combine all separators
        separator_pattern = '|'.join(clause_separators)
        clauses = re.split(separator_pattern, text, flags=re.IGNORECASE)
        
        # Clean and filter clauses
        cleaned_clauses = []
        for clause in clauses:
            clause = clause.strip()
            if len(clause) > 50:  # Filter out very short segments
                cleaned_clauses.append(clause)
        
        return cleaned_clauses

    def classify_clause_type(self, clause_text: str) -> str:
        """Classify the type of a contract clause"""
        clause_lower = clause_text.lower()
        scores = {}
        
        for clause_type, patterns in self.clause_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, clause_lower))
                score += matches
            if score > 0:
                scores[clause_type] = score
        
        if not scores:
            return "GENERAL"
        
        return max(scores, key=scores.get)

    def extract_obligations_rights_prohibitions(self, clause_text: str) -> Tuple[List[str], List[str], List[str]]:
        """Extract obligations, rights, and prohibitions from clause"""
        obligations = []
        rights = []
        prohibitions = []
        
        # Obligation patterns
        obligation_patterns = [
            r"shall\s+([^.]+)",
            r"must\s+([^.]+)",
            r"required to\s+([^.]+)",
            r"obligated to\s+([^.]+)"
        ]
        
        # Rights patterns  
        rights_patterns = [
            r"entitled to\s+([^.]+)",
            r"has the right to\s+([^.]+)",
            r"may\s+([^.]+)",
            r"permitted to\s+([^.]+)"
        ]
        
        # Prohibition patterns
        prohibition_patterns = [
            r"shall not\s+([^.]+)",
            r"must not\s+([^.]+)",
            r"prohibited from\s+([^.]+)",
            r"cannot\s+([^.]+)"
        ]
        
        for pattern in obligation_patterns:
            matches = re.findall(pattern, clause_text, re.IGNORECASE)
            obligations.extend([match.strip() for match in matches])
        
        for pattern in rights_patterns:
            matches = re.findall(pattern, clause_text, re.IGNORECASE)
            rights.extend([match.strip() for match in matches])
            
        for pattern in prohibition_patterns:
            matches = re.findall(pattern, clause_text, re.IGNORECASE)
            prohibitions.extend([match.strip() for match in matches])
        
        return obligations, rights, prohibitions

    def detect_ambiguity(self, text: str) -> List[str]:
        """Detect potentially ambiguous language in contract"""
        ambiguous_phrases = [
            r"reasonable\s+\w+", r"appropriate\s+\w+", r"satisfactory\s+\w+",
            r"as soon as possible", r"in due course", r"from time to time",
            r"best efforts", r"commercially reasonable", r"material\s+\w+",
            r"substantial\s+\w+", r"significant\s+\w+"
        ]
        
        ambiguities = []
        for pattern in ambiguous_phrases:
            matches = re.findall(pattern, text, re.IGNORECASE)
            ambiguities.extend(matches)
        
        return list(set(ambiguities))  # Remove duplicates

    def process_contract(self, text: str) -> Dict:
        """Main processing function for contract analysis"""
        logger.info("Starting contract processing")
        
        # Normalize Hindi text if present
        normalized_text = self.normalize_hindi_text(text)
        
        # Contract classification
        contract_type, type_confidence = self.classify_contract_type(normalized_text)
        
        # Entity extraction
        entities = self.extract_entities(normalized_text)
        
        # Clause segmentation and analysis
        clause_texts = self.segment_clauses(normalized_text)
        clauses = []
        
        for clause_text in clause_texts:
            clause_type = self.classify_clause_type(clause_text)
            obligations, rights, prohibitions = self.extract_obligations_rights_prohibitions(clause_text)
            
            clause = ContractClause(
                text=clause_text,
                clause_type=clause_type,
                section="",  # Will be populated by document structure analysis
                risk_level="",  # Will be populated by risk analysis
                obligations=obligations,
                rights=rights,
                prohibitions=prohibitions
            )
            clauses.append(clause)
        
        # Ambiguity detection
        ambiguities = self.detect_ambiguity(normalized_text)
        
        result = {
            "contract_type": contract_type,
            "type_confidence": type_confidence,
            "entities": entities,
            "clauses": clauses,
            "ambiguities": ambiguities,
            "processed_at": datetime.now().isoformat()
        }
        
        logger.info(f"Contract processing completed. Type: {contract_type}, Clauses: {len(clauses)}")
        return result