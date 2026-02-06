"""
Configuration settings for the Legal Contract Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables with override to ensure fresh loading
load_dotenv(override=True)

# LLM Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DEFAULT_LLM_MODEL = "gemini-2.5-flash"  # or "gpt-4", "claude-3-opus-20240229"

# Risk Scoring Thresholds
RISK_THRESHOLDS = {
    "LOW": (0, 30),
    "MEDIUM": (31, 70),
    "HIGH": (71, 100)
}

# Supported File Types
SUPPORTED_FILE_TYPES = [".pdf", ".docx", ".txt"]
MAX_FILE_SIZE_MB = 10

# Contract Types
CONTRACT_TYPES = [
    "Employment Agreement",
    "Vendor/Supplier Contract", 
    "Lease & Rental Agreement",
    "Partnership Deed",
    "Service Agreement",
    "NDA/Confidentiality Agreement"
]

# High-Risk Clause Keywords
HIGH_RISK_KEYWORDS = [
    "penalty", "liquidated damages", "indemnity", "indemnification",
    "unilateral termination", "auto-renewal", "non-compete", 
    "exclusive", "irrevocable", "unconditional", "unlimited liability"
]

# Audit Configuration
ENABLE_AUDIT_LOGGING = True
AUDIT_LOG_PATH = "logs/audit.log"
DOCUMENT_RETENTION_DAYS = 0  # 0 means no retention unless user opts in

# UI Configuration
APP_TITLE = "Legal Contract Assistant for Indian SMEs"
APP_DESCRIPTION = "Understand contracts, identify risks, get plain-language explanations"

# Disclaimers
LEGAL_DISCLAIMER = """
⚠️ IMPORTANT DISCLAIMER:
This system is NOT a lawyer and does NOT provide legal advice. 
It is designed for educational and risk awareness purposes only.
Always consult qualified legal professionals for legal matters.
"""

RISK_DISCLAIMER = """
Risk assessments are based on general business considerations and 
should not be considered as legal opinions or guarantees.
"""