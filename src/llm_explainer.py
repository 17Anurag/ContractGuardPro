"""
LLM-powered Plain Language Explanation Generator
Converts complex legal clauses into business-friendly explanations
Uses Google Gemini API (free), with OpenAI and Anthropic as fallbacks
"""
import logging
from typing import Dict, List, Optional
from config import GEMINI_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, DEFAULT_LLM_MODEL

logger = logging.getLogger(__name__)

class LegalExplainer:
    """Generates plain-language explanations of legal clauses using Gemini AI"""
    
    def __init__(self, model: str = DEFAULT_LLM_MODEL):
        """Initialize the LLM explainer with Gemini as primary"""
        self.model = model
        
        # Initialize clients in order of preference: Gemini -> OpenAI -> Anthropic
        self.gemini_client = None
        self.openai_client = None
        self.anthropic_client = None
        
        # Try Gemini first (free and reliable)
        if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=GEMINI_API_KEY)
                self.gemini_client = genai.GenerativeModel('gemini-2.5-flash')
                logger.info("✅ Gemini AI client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {str(e)}")
        
        # OpenAI as fallback
        if OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here":
            try:
                import openai
                self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
                logger.info("✅ OpenAI client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {str(e)}")
        
        # Anthropic as second fallback
        if ANTHROPIC_API_KEY and ANTHROPIC_API_KEY != "your_anthropic_api_key_here":
            try:
                import anthropic
                self.anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
                logger.info("✅ Anthropic client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Anthropic client: {str(e)}")
        
        if not any([self.gemini_client, self.openai_client, self.anthropic_client]):
            logger.info("No LLM clients available. Using fallback explanations.")
        
        # System prompts for different explanation types
        self.system_prompts = {
            "clause_explanation": """You are a business mentor helping small business owners in India understand contract clauses. 

CRITICAL RULES:
- Never provide legal advice or guarantees
- Explain like a business mentor, not a lawyer
- Use simple, business-friendly language
- Avoid legal jargon
- Focus on practical business impact
- Always include disclaimer that this is not legal advice

Your role is to:
1. Explain what the clause means in simple terms
2. Identify who benefits from this clause
3. Explain potential business risks or benefits
4. Suggest what to watch out for
5. Indicate if it's standard, aggressive, or unfavorable

Always end with: "This explanation is for educational purposes only and is not legal advice. Consult a qualified lawyer for legal matters."
""",
            
            "risk_explanation": """You are a business risk advisor helping SME owners understand contract risks.

CRITICAL RULES:
- Focus on business impact, not legal technicalities
- Explain risks in terms of money, time, and business operations
- Use examples relevant to Indian SMEs
- Never provide legal advice
- Be clear about who the risk favors

Explain:
1. What this risk means for the business
2. How it could impact operations or finances
3. Why it matters for SMEs specifically
4. What typically happens if this risk materializes

Always include: "This is a business risk assessment, not legal advice. Consult legal professionals for legal guidance."
""",
            
            "negotiation_suggestions": """You are a business negotiation advisor helping SME owners prepare for contract discussions.

CRITICAL RULES:
- Provide business negotiation strategies, not legal advice
- Focus on practical alternatives and compromises
- Consider SME constraints (limited resources, bargaining power)
- Label all suggestions as "negotiation ideas, not legal advice"

Provide:
1. Alternative clause wording that's more balanced
2. Compromise positions that protect SME interests
3. Questions to ask the other party
4. Fallback positions if negotiation fails

Always prefix with: "Suggested negotiation language — not legal advice. Have any changes reviewed by a lawyer before agreeing."
"""
        }

    def _call_llm(self, prompt: str, system_prompt: str) -> str:
        """Make LLM API call - tries Gemini first, then OpenAI, then Anthropic"""
        try:
            # Try Gemini first (free and reliable)
            if self.gemini_client:
                full_prompt = f"{system_prompt}\n\nUser Request: {prompt}"
                response = self.gemini_client.generate_content(full_prompt)
                return response.text
            
            # Fallback to OpenAI
            elif self.model.startswith("gpt") and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.3
                )
                return response.choices[0].message.content
            
            # Fallback to Anthropic
            elif self.model.startswith("claude") and self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    temperature=0.3,
                    system=system_prompt,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            
            else:
                logger.error("No valid LLM client available")
                return self._fallback_explanation()
                
        except Exception as e:
            logger.error(f"LLM API call failed: {str(e)}")
            return self._fallback_explanation()

    def _fallback_explanation(self) -> str:
        """Fallback explanation when LLM is unavailable"""
        return """
        AI explanation service is currently unavailable. This clause requires manual review.
        
        To enable AI-powered explanations:
        1. Get a free Google Gemini API key from: https://makersuite.google.com/app/apikey
        2. Add it to your .env file as: GEMINI_API_KEY=your_key_here
        3. Restart the application
        
        Please consult with a qualified lawyer to understand the implications of this clause for your business.
        
        This system cannot provide legal advice. All explanations are for educational purposes only.
        """

    def explain_clause(self, clause_text: str, clause_type: str, contract_type: str) -> Dict[str, str]:
        """Generate plain-language explanation of a contract clause"""
        
        prompt = f"""
        Contract Type: {contract_type}
        Clause Type: {clause_type}
        
        Clause Text:
        "{clause_text}"
        
        Please provide a business-friendly explanation of this clause for an Indian SME owner. Include:
        
        1. SIMPLE EXPLANATION: What does this clause mean in plain business terms?
        2. WHO BENEFITS: Which party does this clause favor?
        3. BUSINESS IMPACT: How could this affect day-to-day operations?
        4. WATCH OUT FOR: What should the SME owner be careful about?
        5. STANDARD/AGGRESSIVE: Is this typical, aggressive, or unfavorable?
        
        Keep the language simple and practical. Focus on business implications, not legal technicalities.
        """
        
        explanation = self._call_llm(prompt, self.system_prompts["clause_explanation"])
        
        # Parse the response into structured format
        sections = {
            "simple_explanation": "",
            "who_benefits": "",
            "business_impact": "",
            "watch_out_for": "",
            "assessment": ""
        }
        
        # Try to extract sections from the response
        lines = explanation.split('\n')
        current_section = "simple_explanation"
        
        for line in lines:
            line = line.strip()
            if "WHO BENEFITS" in line.upper():
                current_section = "who_benefits"
            elif "BUSINESS IMPACT" in line.upper():
                current_section = "business_impact"
            elif "WATCH OUT" in line.upper():
                current_section = "watch_out_for"
            elif "STANDARD" in line.upper() or "AGGRESSIVE" in line.upper():
                current_section = "assessment"
            elif line and not line.startswith(('1.', '2.', '3.', '4.', '5.')):
                sections[current_section] += line + " "
        
        # Clean up sections
        for key in sections:
            sections[key] = sections[key].strip()
        
        # If parsing failed, put everything in simple_explanation
        if not any(sections.values()):
            sections["simple_explanation"] = explanation
        
        return sections

    def explain_risk(self, risk_flag, clause_text: str) -> Dict[str, str]:
        """Generate business-focused risk explanation"""
        
        prompt = f"""
        Risk Type: {risk_flag.risk_type}
        Risk Level: {risk_flag.risk_level.value}
        Risk Score: {risk_flag.score}/100
        
        Clause Text:
        "{clause_text}"
        
        Risk Description: {risk_flag.description}
        Business Impact: {risk_flag.business_impact}
        SME Concern: {risk_flag.sme_concern}
        
        Explain this risk in business terms for an Indian SME owner:
        
        1. WHAT THIS MEANS: Explain the risk in simple business language
        2. FINANCIAL IMPACT: How could this cost money or affect cash flow?
        3. OPERATIONAL IMPACT: How could this disrupt business operations?
        4. REAL EXAMPLE: Give a realistic example of how this could play out
        5. URGENCY: How urgent is it to address this risk?
        
        Focus on practical business consequences, not legal theory.
        """
        
        explanation = self._call_llm(prompt, self.system_prompts["risk_explanation"])
        
        # Structure the response
        return {
            "risk_explanation": explanation,
            "severity": risk_flag.risk_level.value,
            "score": risk_flag.score
        }

    def suggest_negotiations(self, clause_text: str, risk_flags: List, clause_type: str) -> Dict[str, List[str]]:
        """Generate negotiation suggestions for problematic clauses"""
        
        risk_descriptions = [f"{rf.risk_type}: {rf.description}" for rf in risk_flags]
        
        prompt = f"""
        Clause Type: {clause_type}
        
        Original Clause:
        "{clause_text}"
        
        Identified Risks:
        {chr(10).join(risk_descriptions)}
        
        Provide negotiation suggestions for an Indian SME to make this clause more balanced:
        
        1. ALTERNATIVE WORDING: Suggest more SME-friendly language
        2. COMPROMISE POSITIONS: What middle-ground options exist?
        3. QUESTIONS TO ASK: What should the SME ask the other party?
        4. FALLBACK OPTIONS: If negotiation fails, what are the alternatives?
        5. DEAL BREAKERS: When should the SME walk away?
        
        Consider that SMEs have limited bargaining power but need to protect their interests.
        """
        
        suggestions = self._call_llm(prompt, self.system_prompts["negotiation_suggestions"])
        
        # Parse suggestions into categories
        suggestion_categories = {
            "alternative_wording": [],
            "compromise_positions": [],
            "questions_to_ask": [],
            "fallback_options": [],
            "deal_breakers": []
        }
        
        # Simple parsing - in production, use more sophisticated NLP
        lines = suggestions.split('\n')
        current_category = "alternative_wording"
        
        for line in lines:
            line = line.strip()
            if "ALTERNATIVE WORDING" in line.upper():
                current_category = "alternative_wording"
            elif "COMPROMISE" in line.upper():
                current_category = "compromise_positions"
            elif "QUESTIONS" in line.upper():
                current_category = "questions_to_ask"
            elif "FALLBACK" in line.upper():
                current_category = "fallback_options"
            elif "DEAL BREAKER" in line.upper():
                current_category = "deal_breakers"
            elif line and not line.startswith(('1.', '2.', '3.', '4.', '5.')):
                suggestion_categories[current_category].append(line)
        
        return suggestion_categories

    def generate_executive_summary(self, contract_analysis: Dict, risk_analysis: Dict) -> str:
        """Generate executive summary of contract analysis"""
        
        prompt = f"""
        Contract Type: {contract_analysis.get('contract_type', 'Unknown')}
        Overall Risk Score: {risk_analysis.get('overall_score', 0)}/100
        Risk Level: {risk_analysis.get('overall_level', 'Unknown')}
        
        High Risks: {risk_analysis.get('high_risk_count', 0)}
        Medium Risks: {risk_analysis.get('medium_risk_count', 0)}
        Low Risks: {risk_analysis.get('low_risk_count', 0)}
        
        Total Clauses Analyzed: {len(contract_analysis.get('clauses', []))}
        
        Create a 1-page executive summary for an Indian SME business owner:
        
        1. CONTRACT OVERVIEW: What type of agreement is this?
        2. RISK ASSESSMENT: Overall risk level and key concerns
        3. TOP 3 PRIORITIES: Most important issues to address
        4. RECOMMENDED ACTIONS: What should the business owner do next?
        5. TIMELINE: How urgent are these actions?
        
        Write in a supportive, business-mentor tone. Focus on actionable insights.
        """
        
        summary = self._call_llm(prompt, self.system_prompts["clause_explanation"])
        return summary

    def detect_compliance_concerns(self, contract_text: str, contract_type: str) -> List[str]:
        """Detect potential compliance red flags for Indian commercial context"""
        
        prompt = f"""
        Contract Type: {contract_type}
        
        Contract Text (excerpt):
        "{contract_text[:2000]}..."
        
        Identify potential compliance concerns relevant to Indian commercial law and business practices. 
        
        Look for clauses that might raise concerns regarding:
        - Employment law compliance
        - GST and tax implications  
        - Foreign exchange regulations
        - Data protection and privacy
        - Industry-specific regulations
        - Consumer protection
        
        For each concern, provide:
        1. The specific clause or provision
        2. Why it might be a compliance concern
        3. Recommendation to seek legal review
        
        Use this format: "This clause may raise compliance concerns in India and should be reviewed by a qualified lawyer."
        
        Only flag genuine potential issues - don't be overly cautious.
        """
        
        response = self._call_llm(prompt, self.system_prompts["risk_explanation"])
        
        # Extract compliance concerns from response
        concerns = []
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and ("compliance concern" in line.lower() or "should be reviewed" in line.lower()):
                concerns.append(line)
        
        return concerns