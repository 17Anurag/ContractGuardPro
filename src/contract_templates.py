"""
Contract Templates Module
Provides SME-friendly contract templates with explanations
"""
from typing import Dict, List
from dataclasses import dataclass
import json

@dataclass
class TemplateSection:
    """Represents a section in a contract template"""
    title: str
    content: str
    explanation: str
    customizable: bool
    risk_level: str
    alternatives: List[str]

@dataclass
class ContractTemplate:
    """Represents a complete contract template"""
    name: str
    description: str
    use_case: str
    sections: List[TemplateSection]
    key_considerations: List[str]
    common_pitfalls: List[str]

class ContractTemplateManager:
    """Manages contract templates for SMEs"""
    
    def __init__(self):
        """Initialize template manager with predefined templates"""
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, ContractTemplate]:
        """Load predefined contract templates"""
        templates = {}
        
        # Employment Agreement Template
        templates["employment_agreement"] = self._create_employment_template()
        
        # Vendor Agreement Template
        templates["vendor_agreement"] = self._create_vendor_template()
        
        # Service Agreement Template
        templates["service_agreement"] = self._create_service_template()
        
        # NDA Template
        templates["nda_agreement"] = self._create_nda_template()
        
        return templates
    
    def _create_employment_template(self) -> ContractTemplate:
        """Create employment agreement template"""
        sections = [
            TemplateSection(
                title="Employee Information",
                content="""
Employee Name: [EMPLOYEE_NAME]
Position: [POSITION_TITLE]
Department: [DEPARTMENT]
Reporting Manager: [MANAGER_NAME]
Start Date: [START_DATE]
""",
                explanation="Basic employee details. Ensure position title matches job responsibilities to avoid confusion later.",
                customizable=True,
                risk_level="LOW",
                alternatives=["Include employee ID number", "Add probation period details"]
            ),
            
            TemplateSection(
                title="Compensation and Benefits",
                content="""
Monthly Salary: ₹[AMOUNT] per month
Payment Date: [DAY] of each month
Benefits: [LIST_BENEFITS]
Annual Increment: Subject to performance review
""",
                explanation="Clear compensation terms prevent disputes. Specify gross vs net salary and include all benefits.",
                customizable=True,
                risk_level="MEDIUM",
                alternatives=[
                    "Add performance bonus structure",
                    "Include cost-to-company (CTC) breakdown",
                    "Specify increment criteria"
                ]
            ),
            
            TemplateSection(
                title="Working Hours and Leave",
                content="""
Working Hours: [START_TIME] to [END_TIME], Monday to Friday
Weekly Hours: 40 hours per week
Annual Leave: 21 days per year
Sick Leave: 12 days per year
Public Holidays: As per company calendar
""",
                explanation="Defines work expectations and leave entitlements. Ensure compliance with local labor laws.",
                customizable=True,
                risk_level="LOW",
                alternatives=[
                    "Add flexible working arrangements",
                    "Include overtime compensation",
                    "Specify work from home policy"
                ]
            ),
            
            TemplateSection(
                title="Confidentiality",
                content="""
The Employee agrees to maintain strict confidentiality of all company information, 
including but not limited to business strategies, customer data, financial information, 
and proprietary processes. This obligation continues even after employment ends.
""",
                explanation="Protects company secrets. Standard clause but ensure it's reasonable and not overly broad.",
                customizable=False,
                risk_level="LOW",
                alternatives=[
                    "Define what constitutes confidential information",
                    "Add exceptions for publicly available information"
                ]
            ),
            
            TemplateSection(
                title="Termination",
                content="""
Either party may terminate this agreement with [NOTICE_PERIOD] days written notice.
The company may terminate immediately for cause including misconduct, 
breach of confidentiality, or poor performance after due process.
""",
                explanation="Balanced termination clause. 30-60 days notice is standard for most positions.",
                customizable=True,
                risk_level="MEDIUM",
                alternatives=[
                    "Add severance pay provisions",
                    "Include garden leave option",
                    "Specify termination procedures"
                ]
            )
        ]
        
        return ContractTemplate(
            name="Employment Agreement",
            description="Standard employment contract for hiring employees in India",
            use_case="Use when hiring full-time employees. Covers salary, benefits, working hours, and basic terms.",
            sections=sections,
            key_considerations=[
                "Ensure compliance with local labor laws",
                "Include probation period if applicable",
                "Consider PF, ESI, and other statutory benefits",
                "Add non-compete clause only if necessary and reasonable"
            ],
            common_pitfalls=[
                "Vague job descriptions leading to scope disputes",
                "Unclear increment and promotion criteria",
                "Overly restrictive non-compete clauses",
                "Missing statutory compliance requirements"
            ]
        )
    
    def _create_vendor_template(self) -> ContractTemplate:
        """Create vendor/supplier agreement template"""
        sections = [
            TemplateSection(
                title="Vendor Details",
                content="""
Vendor Name: [VENDOR_NAME]
Address: [VENDOR_ADDRESS]
GST Number: [GST_NUMBER]
Contact Person: [CONTACT_NAME]
Phone: [PHONE_NUMBER]
Email: [EMAIL_ADDRESS]
""",
                explanation="Complete vendor identification for legal and tax purposes. GST number is mandatory for Indian businesses.",
                customizable=True,
                risk_level="LOW",
                alternatives=["Add PAN number", "Include bank account details"]
            ),
            
            TemplateSection(
                title="Scope of Supply",
                content="""
Products/Services: [DETAILED_DESCRIPTION]
Specifications: [TECHNICAL_SPECS]
Quantity: [QUANTITY_DETAILS]
Delivery Schedule: [DELIVERY_TIMELINE]
Quality Standards: [QUALITY_REQUIREMENTS]
""",
                explanation="Clear scope prevents disputes. Be specific about what you're buying and quality expectations.",
                customizable=True,
                risk_level="HIGH",
                alternatives=[
                    "Add acceptance criteria",
                    "Include sample approval process",
                    "Specify packaging requirements"
                ]
            ),
            
            TemplateSection(
                title="Pricing and Payment",
                content="""
Unit Price: ₹[PRICE] per [UNIT]
Total Contract Value: ₹[TOTAL_AMOUNT]
Payment Terms: [PAYMENT_SCHEDULE]
GST: As applicable (currently 18%)
Payment Method: Bank transfer within [DAYS] days of invoice
""",
                explanation="Clear pricing avoids billing disputes. Specify if prices include or exclude GST and other charges.",
                customizable=True,
                risk_level="MEDIUM",
                alternatives=[
                    "Add price escalation clause",
                    "Include advance payment terms",
                    "Specify penalty for late payment"
                ]
            ),
            
            TemplateSection(
                title="Delivery and Performance",
                content="""
Delivery Location: [DELIVERY_ADDRESS]
Delivery Timeline: [TIMELINE]
Risk of Loss: Passes to buyer upon delivery
Inspection Period: [DAYS] days from delivery
Rejection Rights: Buyer may reject non-conforming goods
""",
                explanation="Defines when ownership transfers and your rights to inspect and reject goods.",
                customizable=True,
                risk_level="MEDIUM",
                alternatives=[
                    "Add insurance requirements",
                    "Include force majeure clause",
                    "Specify delivery documentation"
                ]
            ),
            
            TemplateSection(
                title="Warranties and Liability",
                content="""
Vendor warrants that goods/services will:
- Meet specified requirements
- Be free from defects for [WARRANTY_PERIOD]
- Comply with applicable laws and standards

Vendor's liability is limited to replacement or refund of defective items.
""",
                explanation="Basic warranty protection. Ensure warranty period is reasonable for the type of goods/services.",
                customizable=True,
                risk_level="MEDIUM",
                alternatives=[
                    "Add performance guarantees",
                    "Include liability caps",
                    "Specify remedy procedures"
                ]
            )
        ]
        
        return ContractTemplate(
            name="Vendor/Supplier Agreement",
            description="Standard agreement for purchasing goods or services from vendors",
            use_case="Use when engaging suppliers for regular goods or services. Covers pricing, delivery, and quality terms.",
            sections=sections,
            key_considerations=[
                "Verify vendor's GST registration and compliance",
                "Include clear specifications to avoid quality issues",
                "Set reasonable payment terms (30-45 days is common)",
                "Add termination clause for non-performance"
            ],
            common_pitfalls=[
                "Vague product specifications leading to quality disputes",
                "No penalty clauses for delayed delivery",
                "Missing GST and tax compliance requirements",
                "Unclear warranty and return policies"
            ]
        )
    
    def _create_service_template(self) -> ContractTemplate:
        """Create service agreement template"""
        sections = [
            TemplateSection(
                title="Service Provider Details",
                content="""
Service Provider: [PROVIDER_NAME]
Business Type: [INDIVIDUAL/COMPANY/PARTNERSHIP]
Address: [PROVIDER_ADDRESS]
GST Number: [GST_NUMBER] (if applicable)
Contact: [CONTACT_DETAILS]
""",
                explanation="Complete service provider identification. GST registration depends on turnover and service type.",
                customizable=True,
                risk_level="LOW",
                alternatives=["Add professional certifications", "Include insurance details"]
            ),
            
            TemplateSection(
                title="Scope of Services",
                content="""
Services Description: [DETAILED_SERVICE_DESCRIPTION]
Deliverables: [SPECIFIC_DELIVERABLES]
Timeline: [PROJECT_TIMELINE]
Milestones: [KEY_MILESTONES]
Performance Standards: [QUALITY_METRICS]
""",
                explanation="Detailed scope prevents scope creep. Be specific about what's included and excluded.",
                customizable=True,
                risk_level="HIGH",
                alternatives=[
                    "Add change request process",
                    "Include acceptance criteria",
                    "Specify communication protocols"
                ]
            ),
            
            TemplateSection(
                title="Fees and Payment",
                content="""
Service Fee: ₹[AMOUNT] [per hour/fixed/milestone-based]
Payment Schedule: [PAYMENT_TERMS]
Expenses: [EXPENSE_POLICY]
Late Payment: [LATE_FEE_TERMS]
GST: As applicable
""",
                explanation="Clear fee structure and payment terms. Consider milestone-based payments for larger projects.",
                customizable=True,
                risk_level="MEDIUM",
                alternatives=[
                    "Add retainer fee structure",
                    "Include expense reimbursement limits",
                    "Specify currency and payment method"
                ]
            ),
            
            TemplateSection(
                title="Intellectual Property",
                content="""
Work Product: All work created under this agreement belongs to [CLIENT/PROVIDER]
Existing IP: Each party retains ownership of their pre-existing intellectual property
License: [SPECIFY_LICENSE_TERMS]
""",
                explanation="Critical clause determining who owns the work. Usually client owns custom work, provider retains general methodologies.",
                customizable=True,
                risk_level="HIGH",
                alternatives=[
                    "Add joint ownership provisions",
                    "Include IP indemnification",
                    "Specify derivative works rights"
                ]
            ),
            
            TemplateSection(
                title="Termination",
                content="""
Either party may terminate with [NOTICE_PERIOD] days written notice.
Immediate termination allowed for material breach after [CURE_PERIOD] days notice.
Upon termination: [TERMINATION_PROCEDURES]
""",
                explanation="Balanced termination rights. Include procedures for work handover and final payments.",
                customizable=True,
                risk_level="MEDIUM",
                alternatives=[
                    "Add termination fees",
                    "Include work product delivery requirements",
                    "Specify post-termination obligations"
                ]
            )
        ]
        
        return ContractTemplate(
            name="Service Agreement",
            description="Professional services contract for consultants, contractors, and service providers",
            use_case="Use when hiring consultants, freelancers, or professional service providers for specific projects.",
            sections=sections,
            key_considerations=[
                "Clearly define scope to prevent disputes",
                "Consider intellectual property ownership carefully",
                "Include confidentiality provisions if needed",
                "Set realistic timelines with buffer for delays"
            ],
            common_pitfalls=[
                "Vague scope leading to scope creep",
                "Unclear IP ownership causing future disputes",
                "No change management process",
                "Missing liability and indemnity provisions"
            ]
        )
    
    def _create_nda_template(self) -> ContractTemplate:
        """Create NDA/Confidentiality agreement template"""
        sections = [
            TemplateSection(
                title="Parties",
                content="""
Disclosing Party: [COMPANY_NAME]
Receiving Party: [RECIPIENT_NAME]
Purpose: [PURPOSE_OF_DISCLOSURE]
""",
                explanation="Identifies who is sharing information and who is receiving it. Can be mutual (both parties share) or one-way.",
                customizable=True,
                risk_level="LOW",
                alternatives=["Make it mutual NDA", "Add multiple receiving parties"]
            ),
            
            TemplateSection(
                title="Confidential Information",
                content="""
Confidential Information includes:
- Business plans and strategies
- Financial information
- Customer lists and data
- Technical specifications
- Proprietary processes
- Any information marked as confidential

Excludes information that is:
- Publicly available
- Already known to receiving party
- Independently developed
""",
                explanation="Defines what information is protected. Be specific but not overly broad to ensure enforceability.",
                customizable=True,
                risk_level="MEDIUM",
                alternatives=[
                    "Add specific industry information",
                    "Include oral disclosures",
                    "Specify marking requirements"
                ]
            ),
            
            TemplateSection(
                title="Obligations",
                content="""
The Receiving Party agrees to:
- Keep all confidential information strictly confidential
- Use information only for the stated purpose
- Not disclose to third parties without written consent
- Return or destroy information upon request
- Limit access to employees with need-to-know
""",
                explanation="Core obligations of the receiving party. Standard terms that are generally enforceable.",
                customizable=False,
                risk_level="LOW",
                alternatives=[
                    "Add specific security measures",
                    "Include employee notification requirements",
                    "Specify destruction procedures"
                ]
            ),
            
            TemplateSection(
                title="Duration",
                content="""
This agreement remains in effect for [DURATION] years from the date of signing.
Confidentiality obligations survive termination for [SURVIVAL_PERIOD] years.
""",
                explanation="Reasonable duration is key for enforceability. 2-5 years is typical for most business information.",
                customizable=True,
                risk_level="MEDIUM",
                alternatives=[
                    "Make it perpetual for trade secrets",
                    "Add different periods for different information types",
                    "Include automatic renewal provisions"
                ]
            ),
            
            TemplateSection(
                title="Remedies",
                content="""
Breach of this agreement may cause irreparable harm.
The disclosing party may seek:
- Injunctive relief
- Monetary damages
- Attorney fees and costs
""",
                explanation="Enforcement provisions. Injunctive relief is important because monetary damages alone may not be sufficient.",
                customizable=False,
                risk_level="LOW",
                alternatives=[
                    "Add liquidated damages clause",
                    "Include specific penalty amounts",
                    "Specify jurisdiction for disputes"
                ]
            )
        ]
        
        return ContractTemplate(
            name="Non-Disclosure Agreement (NDA)",
            description="Confidentiality agreement to protect sensitive business information",
            use_case="Use before sharing sensitive information with employees, vendors, partners, or potential investors.",
            sections=sections,
            key_considerations=[
                "Keep scope reasonable to ensure enforceability",
                "Consider mutual vs one-way disclosure",
                "Include clear exceptions for publicly available information",
                "Set appropriate duration based on information sensitivity"
            ],
            common_pitfalls=[
                "Overly broad definition of confidential information",
                "Unreasonably long duration making it unenforceable",
                "Missing exceptions for publicly available information",
                "No clear return or destruction procedures"
            ]
        )
    
    def get_template(self, template_name: str) -> ContractTemplate:
        """Get a specific contract template"""
        return self.templates.get(template_name)
    
    def list_templates(self) -> List[str]:
        """List all available template names"""
        return list(self.templates.keys())
    
    def get_template_summary(self) -> Dict[str, Dict]:
        """Get summary of all templates"""
        summary = {}
        for name, template in self.templates.items():
            summary[name] = {
                "name": template.name,
                "description": template.description,
                "use_case": template.use_case,
                "section_count": len(template.sections)
            }
        return summary
    
    def customize_template(self, template_name: str, customizations: Dict) -> str:
        """Generate customized contract from template"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        
        contract_text = f"# {template.name}\n\n"
        contract_text += f"**Purpose:** {template.description}\n\n"
        
        for section in template.sections:
            contract_text += f"## {section.title}\n\n"
            
            # Replace placeholders with customizations
            section_content = section.content
            for placeholder, value in customizations.items():
                section_content = section_content.replace(f"[{placeholder}]", str(value))
            
            contract_text += section_content + "\n\n"
            
            # Add explanation if requested
            if customizations.get("include_explanations", False):
                contract_text += f"*Explanation: {section.explanation}*\n\n"
        
        return contract_text
    
    def export_template_guide(self, template_name: str) -> Dict:
        """Export template with full guidance"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        
        guide = {
            "template_info": {
                "name": template.name,
                "description": template.description,
                "use_case": template.use_case
            },
            "sections": [],
            "key_considerations": template.key_considerations,
            "common_pitfalls": template.common_pitfalls,
            "customization_fields": []
        }
        
        for section in template.sections:
            section_info = {
                "title": section.title,
                "content": section.content,
                "explanation": section.explanation,
                "customizable": section.customizable,
                "risk_level": section.risk_level,
                "alternatives": section.alternatives
            }
            guide["sections"].append(section_info)
            
            # Extract customization fields
            import re
            fields = re.findall(r'\[([A-Z_]+)\]', section.content)
            guide["customization_fields"].extend(fields)
        
        # Remove duplicates
        guide["customization_fields"] = list(set(guide["customization_fields"]))
        
        return guide