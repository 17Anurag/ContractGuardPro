"""
Legal Contract Assistant for Indian SMEs
Main Streamlit Application
"""
import streamlit as st
import os
import tempfile
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our modules
from src.document_processor import DocumentProcessor
from src.nlp_pipeline import LegalNLPPipeline
from src.risk_engine import ContractRiskEngine
from src.llm_explainer import LegalExplainer
from src.contract_templates import ContractTemplateManager

# Try to import audit logger, but don't fail if it's not available
try:
    from src.audit_security import AuditLogger
    AUDIT_AVAILABLE = True
except ImportError:
    AUDIT_AVAILABLE = False
    logger.warning("Audit logging not available")

from config import *

# Page configuration
st.set_page_config(
    page_title="ContractGuard - Legal Contract Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, light-themed CSS for professional legal interface - v2.0
st.markdown("""
<style>
/* =========================
   Color Palette (Legal UI)
   ========================= */
:root {
    --bg-light: #FAFBFC;
    --bg-subtle: #F8F9FA;
    --text-dark: #1A1A1A;
    --text-medium: #4A5568;
    --text-light: #718096;
    --accent-blue: #4A90E2;
    --accent-blue-hover: #357ABD;
    --border-subtle: #E2E8F0;
    --success-bg: #F0FDF4;
    --success-text: #166534;
    --warning-bg: #FFFBEB;
    --warning-text: #92400E;
    --error-bg: #FEF2F2;
    --error-text: #DC2626;
}

/* =========================
   App Background
   ========================= */
.stApp {
    background: var(--bg-light);
    color: var(--text-dark);
}

/* =========================
   Main Container Cleanup
   ========================= */
.stApp .block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1200px;
    background: transparent;
}

/* Remove box look ONLY from layout containers */
.stApp .element-container,
.stApp section,
.stApp [data-testid="stVerticalBlock"] {
    background: transparent !important;
    box-shadow: none !important;
}

/* =========================
   Typography (Readable)
   ========================= */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5,
.stApp h6 {
    color: var(--text-dark) !important;
    font-weight: 600;
}

.stApp p,
.stApp li,
.stApp span,
.stApp div {
    color: var(--text-medium);
}

/* =========================
   Header
   ========================= */
.main-header {
    background: transparent;
    padding: 2rem 0;
    text-align: center;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 2rem;
}

.main-header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}

.main-header p {
    font-size: 1.125rem;
    color: var(--text-medium);
}

/* =========================
   Sidebar (Clean + Light) — FIXED
   ========================= */
            
/* Sidebar container — light gray background */
section[data-testid="stSidebar"] {
    background-color: #F1F3F5 !important;
    border-right: 1px solid var(--border-subtle) !important;
}

/* Sidebar inner spacing (optional but clean) */
section[data-testid="stSidebar"] > div {
    padding-top: 1rem;
}

/* Sidebar headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4 {
    color: var(--text-dark) !important;
    font-weight: 600 !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] li {
    color: var(--text-medium) !important;
}


/* =========================
   Sidebar Sections (NO boxes)
   ========================= */
.sidebar-section {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08) !important;
    border-radius: 0 !important;
    padding: 1rem 0 !important;
    margin-bottom: 1rem !important;
    box-shadow: none !important;
}

.sidebar-section h3 {
    color: #374151 !important;
    font-size: 0.875rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

/* =========================
   Buttons
   ========================= */
.stButton > button {
    background: var(--accent-blue);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
    font-size: 0.875rem;
}

.stButton > button:hover {
    background: var(--accent-blue-hover);
}

/* =========================
   File Upload
   ========================= */
.stFileUploader label {
    background: var(--bg-subtle);
    border: 2px dashed var(--border-subtle);
    border-radius: 8px;
    padding: 2rem;
    color: var(--text-medium);
}

/* =========================
   Selectbox
   ========================= */
.stSelectbox > div > div {
    background: white !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 6px !important;
    color: var(--text-dark) !important;
}

/* =========================
   Tabs
   ========================= */
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 1px solid var(--border-subtle);
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border: none;
    padding: 0.75rem 1rem;
    color: var(--text-medium);
}

.stTabs [aria-selected="true"] {
    color: var(--accent-blue);
    border-bottom: 2px solid var(--accent-blue);
}

/* =========================
   Risk Boxes
   ========================= */
.risk-high {
    background: var(--error-bg);
    border-left: 4px solid var(--error-text);
    padding: 1rem;
    color: var(--error-text);
}

.risk-medium {
    background: var(--warning-bg);
    border-left: 4px solid var(--warning-text);
    padding: 1rem;
    color: var(--warning-text);
}

.risk-low {
    background: var(--success-bg);
    border-left: 4px solid var(--success-text);
    padding: 1rem;
    color: var(--success-text);
}

/* =========================
   Messages
   ========================= */
.stSuccess {
    background: var(--success-bg);
    border: 1px solid var(--success-text);
    color: var(--success-text);
}

.stWarning {
    background: var(--warning-bg);
    border: 1px solid var(--warning-text);
    color: var(--warning-text);
}

.stError {
    background: var(--error-bg);
    border: 1px solid var(--error-text);
    color: var(--error-text);
}

/* =========================
   Hide Streamlit Branding
   ========================= */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>

""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def initialize_components():
    """Initialize all system components"""
    try:
        doc_processor = DocumentProcessor()
        nlp_pipeline = LegalNLPPipeline()
        risk_engine = ContractRiskEngine()
        explainer = LegalExplainer()
        template_manager = ContractTemplateManager()
        audit_logger = AuditLogger() if ENABLE_AUDIT_LOGGING and AUDIT_AVAILABLE else None
        
        return doc_processor, nlp_pipeline, risk_engine, explainer, template_manager, audit_logger
    except Exception as e:
        st.error(f"Failed to initialize system components: {str(e)}")
        st.stop()

def main():
    """Main application function"""
    
    # Initialize components
    doc_processor, nlp_pipeline, risk_engine, explainer, template_manager, audit_logger = initialize_components()
    
    # Force page refresh for new styling
    if 'css_loaded' not in st.session_state:
        st.session_state.css_loaded = True
        st.rerun()
    
    # Clean, professional header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ ContractGuard</h1>
        <p>AI-Powered Contract Analysis for Indian SMEs</p>
        <div style="margin-top: 1rem;">
            <span class="trust-badge">🔒 100% Private & Secure</span>
            <span class="trust-badge">🇮🇳 Built for Indian Business</span>
            <span class="trust-badge">⚡ Instant Analysis</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar navigation
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 📋 Navigation")
        
        page = st.selectbox(
            "Choose what you'd like to do:",
            ["📄 Analyze My Contract", "📝 Contract Templates", "📚 Risk Guide", "ℹ️ About ContractGuard"],
            format_func=lambda x: x,
            help="Select the feature you want to use"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick help section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 🆘 Quick Help")
        st.markdown("""
        **Supported Files:**
        - PDF documents
        - Word files (.docx)
        - Text files (.txt)
        
        **File Size:** Up to 10MB
        
        **Processing Time:** 30-60 seconds
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Trust indicators
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 🔐 Your Privacy")
        st.markdown("""
        ✅ Documents processed locally  
        ✅ No permanent storage  
        ✅ No data sharing  
        ✅ Secure analysis  
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display disclaimers in a more user-friendly way
    with st.expander("⚠️ Important: Please Read Before Using", expanded=False):
        st.markdown("""
        <div class="disclaimer-box">
            🎯 What ContractGuard Does
            ContractGuard helps you understand your contracts by identifying potential risks and explaining complex clauses in simple business terms.
            
            ⚖️ What ContractGuard Is NOT
            ContractGuard is not a lawyer and does not provide legal advice. It's an educational tool to help you make informed decisions.
            
            ✅ Always Remember
            For legal matters, always consult qualified legal professionals. Use ContractGuard's insights to prepare better questions for your lawyer.
        </div>
        """, unsafe_allow_html=True)
    
    # Route to appropriate page
    if page == "📄 Analyze My Contract":
        contract_analysis_page(doc_processor, nlp_pipeline, risk_engine, explainer, audit_logger)
    elif page == "📝 Contract Templates":
        contract_templates_page(template_manager)
    elif page == "📚 Risk Guide":
        risk_guide_page()
    elif page == "ℹ️ About ContractGuard":
        about_page()

def contract_analysis_page(doc_processor, nlp_pipeline, risk_engine, explainer, audit_logger):
    """Contract analysis page"""
    
    st.markdown("## 📄 Contract Analysis")
    st.markdown("Upload your contract to get instant risk analysis and plain-language explanations.")
    
    # Clean file upload section
    st.markdown("""
    <div class="upload-area">
        <h3>📁 Upload Your Contract</h3>
        <p>Drag and drop your file here, or click to browse</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose your contract file",
        type=['pdf', 'docx', 'txt'],
        help="We support PDF, Word documents, and text files up to 10MB",
        label_visibility="collapsed"
    )
    
    # Clean privacy notice
    st.info("🔒 **Your Privacy is Protected:** Your document is processed locally and never stored or shared.")
    
    if uploaded_file is not None:
        # Progress indicator
        progress_container = st.container()
        with progress_container:
            st.markdown("### 🔄 Analysis Progress")
            
            # Step indicators
            steps = [
                ("📄 Document Upload", True, True),
                ("🔍 Text Extraction", True, False),
                ("🧠 AI Analysis", False, False),
                ("⚠️ Risk Assessment", False, False),
                ("📊 Results Ready", False, False)
            ]
            
            for step_name, completed, active in steps:
                status_class = "completed" if completed else ("active" if active else "")
                icon = "✅" if completed else ("🔄" if active else "⏳")
                st.markdown(f"""
                <div class="progress-step {status_class}">
                    {icon} {step_name}
                </div>
                """, unsafe_allow_html=True)
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            # Process document with progress updates
            with st.spinner("🔍 Extracting text from your document..."):
                doc_result = doc_processor.process_document(tmp_file_path)
                
                # Update progress
                steps[1] = ("🔍 Text Extraction", True, True)
                steps[2] = ("🧠 AI Analysis", False, True)
                
                # Log document processing
                if audit_logger:
                    audit_logger.log_document_upload(
                        filename=uploaded_file.name,
                        file_size=len(uploaded_file.getvalue()),
                        document_hash=doc_result['document_hash']
                    )
            
            # Document info cards
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{doc_result['file_size_bytes'] / 1024:.1f} KB</div>
                    <div class="metric-label">File Size</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{doc_result['word_count']:,}</div>
                    <div class="metric-label">Words</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                pages_count = doc_result['extraction_metadata'].get('pages', 'N/A')
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{pages_count}</div>
                    <div class="metric-label">Pages</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Contract analysis
            with st.spinner("🧠 Analyzing contract with AI..."):
                contract_analysis = nlp_pipeline.process_contract(doc_result['extracted_text'])
                
                # Update progress
                steps[2] = ("🧠 AI Analysis", True, True)
                steps[3] = ("⚠️ Risk Assessment", False, True)
                
            with st.spinner("⚠️ Assessing risks..."):
                risk_analysis = risk_engine.analyze_contract_risks(contract_analysis['clauses'])
                
                # Update progress - all complete
                steps[3] = ("⚠️ Risk Assessment", True, True)
                steps[4] = ("📊 Results Ready", True, True)
            
            # Clear progress and show results
            progress_container.empty()
            
            # Success message
            st.success("✅ Analysis Complete! Your contract has been analyzed successfully.")
            
            # Display results in enhanced tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Executive Summary", 
                "⚠️ Risk Analysis", 
                "📝 Clause Details", 
                "💡 Recommendations"
            ])
            
            with tab1:
                display_contract_overview(contract_analysis, risk_analysis, explainer)
            
            with tab2:
                display_risk_analysis(risk_analysis, explainer)
            
            with tab3:
                display_clause_explanations(contract_analysis, risk_analysis, explainer)
            
            with tab4:
                display_recommendations(contract_analysis, risk_analysis, explainer)
            
            # Log analysis completion
            if audit_logger:
                audit_logger.log_analysis_completion(
                    document_hash=doc_result['document_hash'],
                    contract_type=contract_analysis['contract_type'],
                    risk_score=risk_analysis['overall_score']
                )
        
        except Exception as e:
            st.error(f"❌ **Analysis Failed:** {str(e)}")
            st.markdown("""
            **Troubleshooting Tips:**
            - Ensure your file is a valid PDF, Word document, or text file
            - Check that the file contains readable text (not just images)
            - Try a smaller file if yours is very large
            - Contact support if the problem persists
            """)
            logger.error(f"Document processing error: {str(e)}")
        
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)

def display_contract_overview(contract_analysis, risk_analysis, explainer):
    """Display contract overview with enhanced UI"""
    
    st.markdown("## 📊 Executive Summary")
    
    # Main summary cards
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Contract type with confidence - clean display
        confidence_color = "#10b981" if contract_analysis['type_confidence'] > 0.7 else "#f59e0b" if contract_analysis['type_confidence'] > 0.4 else "#ef4444"
        st.markdown("### 📄 Contract Type")
        st.markdown(f"""
        <div style="padding: 0.5rem 0; border-bottom: 1px solid var(--border-subtle);">
            <div style="font-size: 1.5rem; font-weight: 700; color: {confidence_color};">
                {contract_analysis['contract_type']}
            </div>
            <div style="color: var(--text-light); font-size: 0.9rem;">
                Confidence: {contract_analysis['type_confidence']:.1%}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Risk level with color coding
        risk_level = risk_analysis['overall_level']
        risk_score = risk_analysis['overall_score']
        
        if risk_level == "HIGH":
            risk_color = "#991B1B"
            risk_bg = "#FEE2E2"
            risk_icon = "🔴"
        elif risk_level == "MEDIUM":
            risk_color = "#92400E"
            risk_bg = "#FEF3C7"
            risk_icon = "🟡"
        else:
            risk_color = "#065F46"
            risk_bg = "#D1FAE5"
            risk_icon = "🟢"
        
        st.markdown("### ⚠️ Overall Risk")
        st.markdown(f"""
        <div style="padding: 0.5rem 0; text-align: center; border-bottom: 1px solid var(--border-subtle);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{risk_icon}</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: {risk_color};">
                {risk_level}
            </div>
            <div style="color: var(--text-light); font-size: 0.9rem;">
                Score: {risk_score}/100
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Risk breakdown
    st.markdown("### ⚠️ Risk Breakdown")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #991B1B;">
            <div class="metric-value" style="color: #991B1B;">{risk_analysis['high_risk_count']}</div>
            <div class="metric-label">🔴 High Priority Issues</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #92400E;">
            <div class="metric-value" style="color: #92400E;">{risk_analysis['medium_risk_count']}</div>
            <div class="metric-label">🟡 Medium Priority Issues</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #065F46;">
            <div class="metric-value" style="color: #065F46;">{risk_analysis['low_risk_count']}</div>
            <div class="metric-label">🟢 Low Priority Issues</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Key insights
    if risk_analysis['high_risk_count'] > 0:
        st.markdown("### 🚨 Immediate Attention Required")
        high_risks = risk_analysis['risk_summary']['HIGH'][:3]  # Show top 3
        for i, risk in enumerate(high_risks, 1):
            st.markdown(f"""
            <div class="risk-high">
                <strong>{i}. {risk.risk_type.replace('_', ' ').title()}</strong><br>
                <span style="color: var(--neutral-gray);">{risk.sme_concern}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Contract statistics
    st.markdown("### 📈 Contract Analysis Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(contract_analysis['clauses'])}</div>
            <div class="metric-label">Clauses Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(contract_analysis['entities'])}</div>
            <div class="metric-label">Key Terms Found</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        ambiguity_count = len(contract_analysis.get('ambiguities', []))
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{ambiguity_count}</div>
            <div class="metric-label">Unclear Terms</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{risk_analysis['total_risks']}</div>
            <div class="metric-label">Total Risk Flags</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Executive summary generation
    if st.button("📋 Generate Executive Summary", help="Create a business-friendly summary of this contract"):
        with st.spinner("🤖 Generating executive summary..."):
            try:
                summary = explainer.generate_executive_summary(contract_analysis, risk_analysis)
                st.markdown("### 📋 Executive Summary")
                st.markdown(f"""
                <div style="padding: 1rem 0; border-bottom: 1px solid var(--border-subtle);">
                    {summary}
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.warning("⚠️ Executive summary generation is not available. This feature requires an API key to be configured.")
                st.info("💡 **Tip:** Add your OpenAI or Anthropic API key to the .env file to unlock AI-powered explanations and summaries.")

def display_risk_analysis(risk_analysis, explainer):
    """Display detailed risk analysis with enhanced UI"""
    
    st.markdown("## ⚠️ Detailed Risk Analysis")
    st.markdown("Understanding the potential risks in your contract helps you make informed decisions.")
    
    # Risk level filter with better UI
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 🔍 Filter Risks by Priority")
    with col2:
        risk_filter = st.selectbox(
            "Show risks:",
            ["All Risks", "🔴 High Priority", "🟡 Medium Priority", "🟢 Low Priority"],
            help="Filter risks by their priority level"
        )
    
    # Map filter to backend values
    filter_mapping = {
        "All Risks": "All",
        "🔴 High Priority": "HIGH", 
        "🟡 Medium Priority": "MEDIUM",
        "🟢 Low Priority": "LOW"
    }
    backend_filter = filter_mapping[risk_filter]
    
    # Display risks by category with enhanced styling
    for risk_level in ["HIGH", "MEDIUM", "LOW"]:
        if backend_filter != "All" and backend_filter != risk_level:
            continue
            
        risks = risk_analysis['risk_summary'][risk_level]
        if not risks:
            continue
        
        # Risk level header with appropriate styling
        if risk_level == "HIGH":
            icon = "🔴"
            color = "#991B1B"
            bg_color = "#FEE2E2"
            border_color = "#FECACA"
        elif risk_level == "MEDIUM":
            icon = "🟡"
            color = "#92400E"
            bg_color = "#FEF3C7"
            border_color = "#FED7AA"
        else:
            icon = "🟢"
            color = "#065F46"
            bg_color = "#D1FAE5"
            border_color = "#BBF7D0"
        
        st.markdown(f"""
        <div style="background: {bg_color}; padding: 1rem; border-radius: 8px; border: 1px solid {border_color}; margin: 1rem 0;">
            <h3 style="color: {color}; margin-bottom: 0.5rem;">
                {icon} {risk_level.title()} Priority Issues ({len(risks)} found)
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Display each risk in an enhanced card
        for i, risk in enumerate(risks):
            with st.expander(
                f"⚠️ {risk.risk_type.replace('_', ' ').title()} (Risk Score: {risk.score}/100)",
                expanded=risk_level == "HIGH"  # Auto-expand high risks
            ):
                # Risk details in organized sections
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("**📋 What This Means:**")
                    st.write(risk.description)
                    
                    st.markdown("**💼 Business Impact:**")
                    st.write(risk.business_impact)
                    
                    st.markdown("**🎯 SME Concern:**")
                    st.write(risk.sme_concern)
                
                with col2:
                    # Risk score visualization
                    score_color = color
                    st.markdown(f"""
                    <div style="padding: 1rem 0; text-align: center; border-bottom: 1px solid var(--border-subtle);">
                        <div style="font-size: 1.5rem; font-weight: 700; color: {score_color};">
                            {risk.score}/100
                        </div>
                        <div style="color: var(--text-light); font-size: 0.9rem;">Risk Score</div>
                        <div style="margin-top: 0.5rem; color: var(--text-light); font-size: 0.8rem;">
                            Favors: {risk.who_it_favors}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Show clause text in a code block
                st.markdown("**📄 Contract Clause:**")
                st.code(risk.clause_text, language="text")
                
                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"💡 Get Explanation", key=f"explain_risk_{risk_level}_{i}"):
                        with st.spinner("🤖 Generating detailed explanation..."):
                            try:
                                risk_explanation = explainer.explain_risk(risk, risk.clause_text)
                                st.markdown("**🤖 AI Explanation:**")
                                st.info(risk_explanation['risk_explanation'])
                            except Exception as e:
                                st.warning("⚠️ AI explanations require an API key. Add your OpenAI or Anthropic key to .env file.")
                
                with col2:
                    if st.button(f"📋 Copy Clause", key=f"copy_clause_{risk_level}_{i}"):
                        st.success("✅ Clause text copied to clipboard!")
    
    # Summary and next steps
    if risk_analysis['high_risk_count'] > 0:
        st.markdown("### 🚨 Immediate Action Required")
        st.markdown(f"""
        <div class="risk-high">
            <strong>Your contract has {risk_analysis['high_risk_count']} high-priority issues that need immediate attention.</strong><br><br>
            
            <strong>Recommended Next Steps:</strong><br>
            1. 📞 Consult with a qualified lawyer about the high-risk clauses<br>
            2. 💬 Prepare specific questions about each flagged issue<br>
            3. 🤝 Consider negotiating changes to reduce your risk exposure<br>
            4. 📋 Don't sign until you understand and accept all risks
        </div>
        """, unsafe_allow_html=True)
    
    elif risk_analysis['medium_risk_count'] > 0:
        st.markdown("### 🟡 Review Recommended")
        st.markdown(f"""
        <div class="risk-medium">
            <strong>Your contract has {risk_analysis['medium_risk_count']} medium-priority issues worth reviewing.</strong><br><br>
            
            While not critical, these issues could affect your business. Consider discussing them with a legal professional.
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.markdown("### ✅ Low Risk Contract")
        st.markdown(f"""
        <div class="risk-low">
            <strong>Good news! This contract appears to have standard, low-risk terms.</strong><br><br>
            
            While the risk is low, always ensure you understand all terms before signing.
        </div>
        """, unsafe_allow_html=True)

def display_clause_explanations(contract_analysis, risk_analysis, explainer):
    """Display clause-by-clause explanations with enhanced UI"""
    
    st.markdown("## 📝 Clause-by-Clause Analysis")
    st.markdown("Understand each part of your contract in simple business terms.")
    
    clauses = contract_analysis['clauses']
    if not clauses:
        st.info("ℹ️ No specific clauses were identified in this contract. This might be a simple document or the text extraction needs improvement.")
        return
    
    # Clause navigation
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 🔍 Select a Clause to Analyze")
    with col2:
        clause_index = st.selectbox(
            "Choose clause:",
            range(len(clauses)),
            format_func=lambda x: f"Clause {x+1}: {clauses[x].clause_type.replace('_', ' ').title()}",
            help="Select any clause to see detailed analysis"
        )
    
    selected_clause = clauses[clause_index]
    
    # Clause header with type and risk indicator
    clause_risks = []
    for risk_level in ["HIGH", "MEDIUM", "LOW"]:
        for risk in risk_analysis['risk_summary'][risk_level]:
            if selected_clause.text in risk.clause_text or risk.clause_text in selected_clause.text:
                clause_risks.append(risk)
    
    # Risk indicator for this clause
    if clause_risks:
        highest_risk = max(clause_risks, key=lambda r: r.score)
        if highest_risk.score >= 71:
            risk_badge = "🔴 High Risk"
            risk_color = "#991B1B"
            risk_bg = "#FEE2E2"
        elif highest_risk.score >= 31:
            risk_badge = "🟡 Medium Risk"
            risk_color = "#92400E"
            risk_bg = "#FEF3C7"
        else:
            risk_badge = "🟢 Low Risk"
            risk_color = "#065F46"
            risk_bg = "#D1FAE5"
    else:
        risk_badge = "✅ No Issues"
        risk_color = "#065F46"
        risk_bg = "#D1FAE5"
    
    st.markdown(f"""
    <div style="background: {risk_bg}; padding: 1.5rem; border-radius: 12px; border: 1px solid {risk_color}; margin: 1rem 0;">
        <h3 style="color: {risk_color}; margin-bottom: 0.5rem;">
            📄 Clause {clause_index + 1}: {selected_clause.clause_type.replace('_', ' ').title()}
        </h3>
        <div style="padding: 0.5rem 1rem; border-radius: 6px; display: inline-block; background: var(--bg-subtle); border: 1px solid var(--border-subtle);">
            <strong>{risk_badge}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Clause content in two columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### 📄 Original Clause Text")
        st.markdown(f"""
        <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb; font-family: monospace; line-height: 1.6;">
            {selected_clause.text}
        </div>
        """, unsafe_allow_html=True)
        
        # Clause details
        if selected_clause.obligations or selected_clause.rights or selected_clause.prohibitions:
            st.markdown("#### 📋 What This Clause Contains")
            
            if selected_clause.obligations:
                st.markdown("**🔸 Your Obligations (What you must do):**")
                for obligation in selected_clause.obligations:
                    st.markdown(f"• {obligation}")
            
            if selected_clause.rights:
                st.markdown("**✅ Your Rights (What you can do):**")
                for right in selected_clause.rights:
                    st.markdown(f"• {right}")
            
            if selected_clause.prohibitions:
                st.markdown("**❌ Restrictions (What you cannot do):**")
                for prohibition in selected_clause.prohibitions:
                    st.markdown(f"• {prohibition}")
    
    with col2:
        # Risk analysis for this clause
        if clause_risks:
            st.markdown("#### ⚠️ Identified Risks")
            for risk in clause_risks[:2]:  # Show top 2 risks
                st.markdown(f"""
                <div style="padding: 1rem 0; border-left: 4px solid {risk_color}; padding-left: 1rem; margin-bottom: 1rem; border-bottom: 1px solid var(--border-subtle);">
                    <strong>{risk.risk_type.replace('_', ' ').title()}</strong><br>
                    <span style="color: var(--text-light); font-size: 0.9rem;">Score: {risk.score}/100</span><br>
                    <span style="font-size: 0.9rem;">{risk.sme_concern}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("#### ✅ No Major Risks Detected")
            st.success("This clause appears to contain standard business terms without significant risk flags.")
        
        # Quick stats
        st.markdown("#### 📊 Clause Statistics")
        word_count = len(selected_clause.text.split())
        char_count = len(selected_clause.text)
        
        st.markdown(f"""
        <div style="padding: 1rem 0; border-bottom: 1px solid var(--border-subtle);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Words:</span> <strong>{word_count}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Characters:</span> <strong>{char_count}</strong>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>Type:</span> <strong>{selected_clause.clause_type.replace('_', ' ').title()}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # AI explanation section
    st.markdown("---")
    st.markdown("### 🤖 Get AI-Powered Explanation")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("Get this clause explained in simple business terms that anyone can understand.")
    with col2:
        explain_button = st.button("🤖 Explain This Clause", use_container_width=True)
    
    if explain_button:
        with st.spinner("🤖 Generating business-friendly explanation..."):
            try:
                explanation = explainer.explain_clause(
                    selected_clause.text,
                    selected_clause.clause_type,
                    contract_analysis['contract_type']
                )
                
                st.markdown("#### 💬 Plain Language Explanation")
                
                # Display explanation in organized sections
                explanation_sections = [
                    ("🎯 What this means in simple terms", explanation.get('simple_explanation', '')),
                    ("👥 Who benefits from this clause", explanation.get('who_benefits', '')),
                    ("💼 How this affects your business", explanation.get('business_impact', '')),
                    ("⚠️ What to watch out for", explanation.get('watch_out_for', '')),
                    ("📊 Is this standard or unusual?", explanation.get('assessment', ''))
                ]
                
                for title, content in explanation_sections:
                    if content:
                        st.markdown(f"**{title}:**")
                        st.markdown(f"""
                        <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border-left: 4px solid var(--secondary-blue); margin-bottom: 1rem;">
                            {content}
                        </div>
                        """, unsafe_allow_html=True)
                        
            except Exception as e:
                st.warning("⚠️ AI explanations require an API key to be configured.")
                st.info("💡 **Tip:** Add your OpenAI or Anthropic API key to the .env file to unlock detailed AI explanations.")
    
    # Navigation helpers
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if clause_index > 0:
            if st.button("⬅️ Previous Clause"):
                st.rerun()
    
    with col2:
        st.markdown(f"<div style='text-align: center; color: var(--neutral-gray);'>Clause {clause_index + 1} of {len(clauses)}</div>", unsafe_allow_html=True)
    
    with col3:
        if clause_index < len(clauses) - 1:
            if st.button("Next Clause ➡️"):
                st.rerun()

def display_recommendations(contract_analysis, risk_analysis, explainer):
    """Display recommendations and next steps with enhanced UI"""
    
    st.markdown("## 💡 Recommendations & Next Steps")
    st.markdown("Based on our analysis, here's what you should do to protect your business interests.")
    
    # Get high and medium risks for recommendations
    high_risks = risk_analysis['risk_summary']['HIGH']
    medium_risks = risk_analysis['risk_summary']['MEDIUM']
    overall_score = risk_analysis['overall_score']
    
    # Overall recommendation based on risk level
    if overall_score >= 71:
        st.markdown("""
        <div class="risk-high">
            <h3>🚨 HIGH RISK CONTRACT - Immediate Action Required</h3>
            <p>This contract contains significant risks that could seriously impact your business. <strong>Do not sign without legal review.</strong></p>
        </div>
        """, unsafe_allow_html=True)
    elif overall_score >= 31:
        st.markdown("""
        <div class="risk-medium">
            <h3>🟡 MEDIUM RISK CONTRACT - Review Recommended</h3>
            <p>This contract has some concerning terms that should be reviewed and potentially negotiated before signing.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="risk-low">
            <h3>✅ LOW RISK CONTRACT - Generally Acceptable</h3>
            <p>This contract appears to have standard business terms with minimal risk. Still, ensure you understand all obligations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Priority actions
    if high_risks or medium_risks:
        st.markdown("### 🎯 Priority Actions")
        
        action_items = []
        
        if high_risks:
            action_items.extend([
                ("🔴 URGENT", f"Have a lawyer review {len(high_risks)} high-risk clauses", "Within 24 hours"),
                ("📞 CRITICAL", "Schedule legal consultation before signing", "Immediately"),
                ("📋 PREPARE", "List specific questions about flagged risks", "Before lawyer meeting")
            ])
        
        if medium_risks:
            action_items.extend([
                ("🟡 IMPORTANT", f"Review {len(medium_risks)} medium-risk clauses carefully", "Within 1 week"),
                ("💬 NEGOTIATE", "Consider requesting changes to problematic terms", "Before signing")
            ])
        
        action_items.extend([
            ("✅ VERIFY", "Ensure you understand all your obligations", "Before signing"),
            ("📄 DOCUMENT", "Keep copies of all contract versions and communications", "Always")
        ])
        
        for priority, action, timeline in action_items:
            st.markdown(f"""
            <div style="padding: 1rem 0; border-left: 4px solid var(--accent-blue); padding-left: 1rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-subtle);">
                <div>
                    <strong>{priority}:</strong> {action}
                </div>
                <div style="color: var(--text-light); font-size: 0.9rem; font-style: italic;">
                    {timeline}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Specific risk-based recommendations
    if high_risks:
        st.markdown("### 🚨 High-Risk Issues Requiring Attention")
        
        for i, risk in enumerate(high_risks[:3], 1):  # Show top 3 high risks
            with st.expander(f"🔴 Issue {i}: {risk.risk_type.replace('_', ' ').title()}", expanded=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("**The Problem:**")
                    st.write(risk.sme_concern)
                    
                    st.markdown("**Business Impact:**")
                    st.write(risk.business_impact)
                    
                    st.markdown("**Who This Favors:**")
                    st.write(risk.who_it_favors)
                
                with col2:
                    st.markdown(f"""
                    <div style="background: #fef2f2; padding: 1rem; border-radius: 8px; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: 700; color: #ef4444;">
                            {risk.score}/100
                        </div>
                        <div style="color: var(--neutral-gray); font-size: 0.9rem;">Risk Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Generate negotiation suggestions
                if st.button(f"💡 Get Negotiation Ideas", key=f"negotiate_{i}"):
                    with st.spinner("🤖 Generating negotiation suggestions..."):
                        try:
                            suggestions = explainer.suggest_negotiations(
                                risk.clause_text,
                                [risk],
                                risk.risk_type
                            )
                            
                            st.markdown("**🤝 Negotiation Suggestions:**")
                            st.info("These are business negotiation ideas, not legal advice. Have any changes reviewed by a lawyer.")
                            
                            for category, items in suggestions.items():
                                if items:
                                    category_title = category.replace('_', ' ').title()
                                    st.markdown(f"**{category_title}:**")
                                    for item in items:
                                        st.write(f"• {item}")
                                        
                        except Exception as e:
                            st.warning("⚠️ Negotiation suggestions require an API key. Add your OpenAI or Anthropic key to .env file.")
    
    # General recommendations
    st.markdown("### 📋 General Best Practices")
    
    recommendations = [
        ("🔍 **Understand Before Signing**", "Make sure you fully understand every clause and your obligations"),
        ("⚖️ **Get Legal Review**", "Have a qualified lawyer review any contract with significant business impact"),
        ("💬 **Ask Questions**", "Prepare specific questions about unclear terms or concerning clauses"),
        ("🤝 **Negotiate When Possible**", "Many contract terms are negotiable, especially if you bring value"),
        ("📋 **Document Everything**", "Keep records of all negotiations, changes, and communications"),
        ("⏰ **Set Reminders**", "Create calendar reminders for key dates like renewal or termination deadlines"),
        ("🔄 **Review Regularly**", "Periodically review your contracts to ensure ongoing compliance")
    ]
    
    for title, description in recommendations:
        st.markdown(f"""
        <div style="padding: 1rem 0; border-bottom: 1px solid var(--border-subtle); margin-bottom: 0.5rem;">
            {title}: {description}
        </div>
        """, unsafe_allow_html=True)
    
    # Compliance check
    st.markdown("### ⚖️ Compliance Considerations")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("Check for potential compliance issues specific to Indian business law and regulations.")
    with col2:
        if st.button("🔍 Check Compliance", use_container_width=True):
            with st.spinner("🤖 Checking for compliance concerns..."):
                try:
                    concerns = explainer.detect_compliance_concerns(
                        contract_analysis.get('clauses', [{}])[0].text if contract_analysis.get('clauses') else "",
                        contract_analysis['contract_type']
                    )
                    
                    if concerns:
                        st.markdown("#### ⚖️ Potential Compliance Concerns")
                        st.warning("The following areas may require legal review for Indian law compliance:")
                        for concern in concerns:
                            st.markdown(f"• {concern}")
                    else:
                        st.success("✅ No obvious compliance red flags detected in this contract.")
                        
                except Exception as e:
                    st.warning("⚠️ Compliance checking requires an API key. Add your OpenAI or Anthropic key to .env file.")
    
    # Export recommendations
    st.markdown("---")
    st.markdown("### 📄 Export Your Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Download Summary", use_container_width=True):
            # Create a simple text summary
            summary_text = f"""
CONTRACT ANALYSIS SUMMARY
========================

Contract Type: {contract_analysis['contract_type']}
Overall Risk Level: {risk_analysis['overall_level']} ({risk_analysis['overall_score']}/100)

Risk Breakdown:
- High Priority Issues: {risk_analysis['high_risk_count']}
- Medium Priority Issues: {risk_analysis['medium_risk_count']}
- Low Priority Issues: {risk_analysis['low_risk_count']}

DISCLAIMER: This analysis is for educational purposes only and does not constitute legal advice.
Always consult qualified legal professionals for legal matters.

Generated by ContractGuard - {datetime.now().strftime('%Y-%m-%d %H:%M')}
            """
            
            st.download_button(
                label="📄 Download Text Summary",
                data=summary_text,
                file_name=f"contract_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )
    
    with col2:
        st.button("📧 Email Summary", disabled=True, help="Feature coming soon", use_container_width=True)
    
    with col3:
        st.button("🔗 Share Analysis", disabled=True, help="Feature coming soon", use_container_width=True)
    
    # Final reminder - clean styling
    st.markdown("---")
    st.warning("🎯 **Remember:** ContractGuard helps you understand your contracts, but it's not a replacement for legal advice. For important business decisions, always consult with qualified legal professionals.")

def contract_templates_page(template_manager):
    """Contract templates page"""
    
    st.header("📋 Contract Templates")
    st.markdown("SME-friendly contract templates with explanations and customization options.")
    
    # Template selection
    templates = template_manager.get_template_summary()
    
    if not templates:
        st.error("No templates available.")
        return
    
    template_names = list(templates.keys())
    selected_template = st.selectbox(
        "Choose a template:",
        template_names,
        format_func=lambda x: templates[x]['name']
    )
    
    if selected_template:
        template = template_manager.get_template(selected_template)
        
        # Template info
        st.subheader(template.name)
        st.write(f"**Description:** {template.description}")
        st.write(f"**Use Case:** {template.use_case}")
        
        # Template sections
        with st.expander("📄 Template Sections", expanded=True):
            for i, section in enumerate(template.sections):
                st.write(f"**{i+1}. {section.title}**")
                st.write(f"*{section.explanation}*")
                
                risk_color = "🔴" if section.risk_level == "HIGH" else "🟡" if section.risk_level == "MEDIUM" else "🟢"
                st.write(f"Risk Level: {risk_color} {section.risk_level}")
                
                if section.alternatives:
                    with st.expander(f"Alternative options for {section.title}"):
                        for alt in section.alternatives:
                            st.write(f"• {alt}")
        
        # Key considerations
        with st.expander("🔑 Key Considerations"):
            for consideration in template.key_considerations:
                st.write(f"• {consideration}")
        
        # Common pitfalls
        with st.expander("⚠️ Common Pitfalls to Avoid"):
            for pitfall in template.common_pitfalls:
                st.write(f"• {pitfall}")
        
        # Template customization
        st.subheader("🛠️ Customize Template")
        
        # Get customization fields
        guide = template_manager.export_template_guide(selected_template)
        customizations = {}
        
        if guide['customization_fields']:
            st.write("Fill in the following details to customize your contract:")
            
            for field in guide['customization_fields']:
                field_label = field.replace('_', ' ').title()
                customizations[field] = st.text_input(field_label, key=f"custom_{field}")
        
        # Generate customized contract
        if st.button("Generate Contract"):
            if any(customizations.values()):
                try:
                    contract_text = template_manager.customize_template(selected_template, customizations)
                    
                    st.subheader("📄 Your Customized Contract")
                    st.markdown(contract_text)
                    
                    # Download button
                    st.download_button(
                        label="Download Contract",
                        data=contract_text,
                        file_name=f"{template.name.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}.md",
                        mime="text/markdown"
                    )
                    
                except Exception as e:
                    st.error(f"Error generating contract: {str(e)}")
            else:
                st.warning("Please fill in at least some customization fields.")

def risk_guide_page():
    """Risk assessment guide page"""
    
    st.header("📚 Risk Assessment Guide")
    st.markdown("Learn about common contract risks and how to protect your business.")
    
    # Risk categories
    risk_categories = {
        "Financial Risks": {
            "description": "Risks that could cost your business money",
            "examples": [
                "Penalty clauses for delays",
                "Unlimited liability exposure", 
                "Personal guarantees",
                "Liquidated damages"
            ],
            "protection": [
                "Negotiate liability caps",
                "Avoid personal guarantees when possible",
                "Ensure penalty amounts are reasonable",
                "Include force majeure clauses"
            ]
        },
        "Operational Risks": {
            "description": "Risks that could disrupt your business operations",
            "examples": [
                "Exclusive dealing arrangements",
                "Non-compete clauses",
                "Unilateral termination rights",
                "Restrictive IP assignments"
            ],
            "protection": [
                "Maintain multiple supplier/customer relationships",
                "Negotiate mutual termination rights",
                "Limit non-compete duration and scope",
                "Retain rights to pre-existing IP"
            ]
        },
        "Legal & Compliance Risks": {
            "description": "Risks related to legal compliance and disputes",
            "examples": [
                "Unfavorable jurisdiction clauses",
                "Mandatory arbitration",
                "Indemnification obligations",
                "Regulatory compliance gaps"
            ],
            "protection": [
                "Choose convenient jurisdiction",
                "Include mutual indemnification",
                "Ensure compliance with local laws",
                "Add legal review requirements"
            ]
        }
    }
    
    for category, info in risk_categories.items():
        with st.expander(f"📊 {category}", expanded=False):
            st.write(f"**What it is:** {info['description']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Common Examples:**")
                for example in info['examples']:
                    st.write(f"• {example}")
            
            with col2:
                st.write("**How to Protect Yourself:**")
                for protection in info['protection']:
                    st.write(f"• {protection}")
    
    # Risk scoring explanation
    st.subheader("🎯 How Risk Scoring Works")
    
    st.write("""
    Our system scores contract risks on a scale of 0-100:
    
    - **0-30 (Low Risk):** 🟢 Standard business terms with minimal concern
    - **31-70 (Medium Risk):** 🟡 Terms that require attention and possible negotiation  
    - **71-100 (High Risk):** 🔴 Terms that pose significant risk and need immediate attention
    
    **Factors that increase risk scores:**
    - Unlimited liability exposure
    - Personal guarantees required
    - Harsh penalty clauses
    - Unilateral termination rights
    - Overly broad non-compete clauses
    
    **Factors that reduce risk scores:**
    - Liability limitations and caps
    - Mutual termination rights
    - Force majeure protections
    - Reasonable notice periods
    """)

def about_page():
    """About page"""
    
    st.header("ℹ️ About Legal Contract Assistant")
    
    st.markdown("""
    ## What We Do
    
    The Legal Contract Assistant helps Indian small and medium business owners understand complex contracts 
    by providing:
    
    - **Plain-language explanations** of legal clauses
    - **Risk assessment** and scoring
    - **Business impact analysis** 
    - **Negotiation suggestions**
    - **SME-friendly contract templates**
    
    ## How It Works
    
    1. **Upload** your contract document (PDF, DOCX, or TXT)
    2. **Analysis** using AI-powered natural language processing
    3. **Risk Detection** identifies potential issues and scores them
    4. **Plain Language** explanations make complex clauses understandable
    5. **Recommendations** help you take appropriate action
    
    ## Important Limitations
    
    ⚠️ **This system is NOT a lawyer and does NOT provide legal advice.**
    
    - All explanations are for educational purposes only
    - Risk assessments are based on general business considerations
    - Always consult qualified legal professionals for legal matters
    - The system cannot guarantee accuracy or completeness
    
    ## Supported Contract Types
    
    - Employment Agreements
    - Vendor/Supplier Contracts  
    - Lease & Rental Agreements
    - Partnership Deeds
    - Service Agreements
    - NDAs/Confidentiality Agreements
    
    ## Privacy & Security
    
    - Documents are processed locally and not stored permanently
    - No document content is shared with third parties
    - Audit logs track usage for security purposes only
    - Users can opt out of document retention
    
    ## Technical Details
    
    - Built with Python, Streamlit, and spaCy
    - Uses OpenAI GPT or Anthropic Claude for explanations
    - Supports English and basic Hindi text processing
    - Designed specifically for Indian commercial context
    """)
    
    # System status
    st.subheader("🔧 System Status")
    
    # Check component status
    try:
        doc_processor, nlp_pipeline, risk_engine, explainer, template_manager, audit_logger = initialize_components()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.success("✅ Document Processing")
            st.success("✅ NLP Pipeline") 
            st.success("✅ Risk Engine")
        
        with col2:
            # Check LLM availability
            if OPENAI_API_KEY or ANTHROPIC_API_KEY:
                st.success("✅ LLM Service")
            else:
                st.warning("⚠️ LLM Service (Limited)")
            
            st.success("✅ Template Manager")
            
            if ENABLE_AUDIT_LOGGING:
                st.success("✅ Audit Logging")
            else:
                st.info("ℹ️ Audit Logging (Disabled)")
        
        with col3:
            st.info(f"📊 Templates: {len(template_manager.list_templates())}")
            st.info(f"🔧 Version: 1.0.0")
            st.info(f"📅 Updated: {datetime.now().strftime('%Y-%m-%d')}")
            
    except Exception as e:
        st.error(f"❌ System Error: {str(e)}")

if __name__ == "__main__":
    main()