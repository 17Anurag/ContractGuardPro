"""
Demo script for Legal Contract Assistant
Shows the system working without the web interface
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def demo_contract_analysis():
    """Demo the contract analysis functionality"""
    print("🚀 Legal Contract Assistant - Demo")
    print("=" * 50)
    
    # Import modules
    from src.document_processor import DocumentProcessor
    from src.nlp_pipeline import LegalNLPPipeline
    from src.risk_engine import ContractRiskEngine
    from src.llm_explainer import LegalExplainer
    from src.contract_templates import ContractTemplateManager
    
    # Sample contract text
    sample_contract = """
    EMPLOYMENT AGREEMENT
    
    This Employment Agreement is entered into between TechCorp India Pvt Ltd ("Company") 
    and Rajesh Kumar ("Employee").
    
    1. POSITION AND DUTIES
    The Employee shall serve as Senior Software Developer and shall perform duties 
    as assigned by the Company.
    
    2. COMPENSATION
    The Employee shall receive a monthly salary of ₹75,000 (Seventy-Five Thousand Rupees).
    Payment shall be made on the last working day of each month.
    
    3. TERMINATION
    Either party may terminate this agreement with 60 days written notice.
    The Company may terminate immediately for cause including misconduct or breach of confidentiality.
    
    4. CONFIDENTIALITY
    The Employee agrees to maintain strict confidentiality of all proprietary information
    and trade secrets of the Company. This obligation shall survive termination.
    
    5. INDEMNIFICATION
    The Employee shall indemnify and hold harmless the Company from any and all damages,
    losses, or expenses arising from Employee's breach of this agreement.
    
    6. NON-COMPETE
    For a period of 2 years after termination, Employee shall not engage in any business
    that competes with the Company within India.
    """
    
    print("📄 Sample Contract:")
    print("-" * 30)
    print(sample_contract[:200] + "...")
    print()
    
    # Initialize components
    print("🔧 Initializing components...")
    nlp_pipeline = LegalNLPPipeline()
    risk_engine = ContractRiskEngine()
    template_manager = ContractTemplateManager()
    
    # Analyze contract
    print("🔍 Analyzing contract...")
    contract_analysis = nlp_pipeline.process_contract(sample_contract)
    risk_analysis = risk_engine.analyze_contract_risks(contract_analysis['clauses'])
    
    # Display results
    print("\n📊 ANALYSIS RESULTS")
    print("=" * 50)
    
    print(f"📋 Contract Type: {contract_analysis['contract_type']}")
    print(f"🎯 Confidence: {contract_analysis['type_confidence']:.1%}")
    print(f"📝 Clauses Found: {len(contract_analysis['clauses'])}")
    print(f"🏷️  Entities Extracted: {len(contract_analysis['entities'])}")
    
    print(f"\n⚠️ RISK ASSESSMENT")
    print("-" * 30)
    print(f"Overall Risk Score: {risk_analysis['overall_score']}/100")
    print(f"Risk Level: {risk_analysis['overall_level']}")
    print(f"🔴 High Risks: {risk_analysis['high_risk_count']}")
    print(f"🟡 Medium Risks: {risk_analysis['medium_risk_count']}")
    print(f"🟢 Low Risks: {risk_analysis['low_risk_count']}")
    
    # Show high-risk issues
    if risk_analysis['high_risk_count'] > 0:
        print(f"\n🚨 HIGH-RISK ISSUES:")
        print("-" * 30)
        for risk in risk_analysis['risk_summary']['HIGH']:
            print(f"• {risk.risk_type.replace('_', ' ').title()}")
            print(f"  Score: {risk.score}/100")
            print(f"  Concern: {risk.sme_concern}")
            print()
    
    # Show entities
    print("🏷️  EXTRACTED ENTITIES:")
    print("-" * 30)
    entity_types = {}
    for entity in contract_analysis['entities']:
        if entity.label not in entity_types:
            entity_types[entity.label] = []
        entity_types[entity.label].append(entity.text)
    
    for entity_type, entities in entity_types.items():
        print(f"{entity_type}: {', '.join(set(entities))}")
    
    # Show clause types
    print(f"\n📝 CLAUSE BREAKDOWN:")
    print("-" * 30)
    clause_types = {}
    for clause in contract_analysis['clauses']:
        clause_type = clause.clause_type
        if clause_type not in clause_types:
            clause_types[clause_type] = 0
        clause_types[clause_type] += 1
    
    for clause_type, count in clause_types.items():
        print(f"{clause_type.replace('_', ' ').title()}: {count}")
    
    # Show templates
    print(f"\n📋 AVAILABLE TEMPLATES:")
    print("-" * 30)
    templates = template_manager.get_template_summary()
    for template_name, template_info in templates.items():
        print(f"• {template_info['name']}")
        print(f"  Use case: {template_info['use_case']}")
    
    print(f"\n✅ RECOMMENDATIONS:")
    print("-" * 30)
    if risk_analysis['overall_score'] >= 71:
        print("🔴 HIGH RISK CONTRACT - Immediate attention required!")
        print("• Have a lawyer review this contract before signing")
        print("• Negotiate to reduce high-risk clauses")
        print("• Consider liability limitations")
    elif risk_analysis['overall_score'] >= 31:
        print("🟡 MEDIUM RISK CONTRACT - Review recommended")
        print("• Review identified risks carefully")
        print("• Consider negotiating problematic clauses")
        print("• Ensure you understand all obligations")
    else:
        print("🟢 LOW RISK CONTRACT - Generally acceptable")
        print("• Standard business terms detected")
        print("• Review for completeness")
        print("• Ensure all details are correct")
    
    print(f"\n⚠️  DISCLAIMER:")
    print("-" * 30)
    print("This analysis is for educational purposes only and does not constitute legal advice.")
    print("Always consult qualified legal professionals for legal matters.")
    
    print(f"\n🎉 Demo completed successfully!")
    print("To run the full web application: python run.py")

if __name__ == "__main__":
    demo_contract_analysis()