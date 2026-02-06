"""
Risk Detection and Scoring Engine
Analyzes contract clauses for legal and commercial risks
"""
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM" 
    HIGH = "HIGH"

@dataclass
class RiskFlag:
    """Represents a detected risk in contract"""
    clause_text: str
    risk_type: str
    risk_level: RiskLevel
    description: str
    business_impact: str
    who_it_favors: str
    sme_concern: str
    score: int  # 0-100

class ContractRiskEngine:
    """Engine for detecting and scoring contract risks"""
    
    def __init__(self):
        """Initialize risk detection patterns and rules"""
        
        # High-risk clause patterns with scoring
        self.risk_patterns = {
            "PENALTY_LIQUIDATED_DAMAGES": {
                "patterns": [
                    r"penalty.*₹?\s*[\d,]+",
                    r"liquidated damages.*₹?\s*[\d,]+", 
                    r"forfeit.*₹?\s*[\d,]+",
                    r"damages.*₹?\s*[\d,]+.*per day",
                    r"penalty.*percentage.*contract value"
                ],
                "base_score": 85,
                "description": "Penalty or liquidated damages clause",
                "business_impact": "Financial penalties for delays or breaches",
                "who_it_favors": "Other party (client/vendor)",
                "sme_concern": "Can result in significant unexpected costs"
            },
            
            "INDEMNITY": {
                "patterns": [
                    r"indemnify.*harmless",
                    r"indemnification.*losses",
                    r"hold.*harmless.*damages",
                    r"defend.*indemnify.*hold harmless",
                    r"unlimited.*indemnity"
                ],
                "base_score": 80,
                "description": "Indemnity clause requiring protection of other party",
                "business_impact": "Liability for third-party claims and damages",
                "who_it_favors": "Other party being indemnified",
                "sme_concern": "Unlimited liability exposure beyond your control"
            },
            
            "UNILATERAL_TERMINATION": {
                "patterns": [
                    r"terminate.*without cause",
                    r"terminate.*at will",
                    r"terminate.*sole discretion",
                    r"terminate.*without notice",
                    r"immediate termination.*breach"
                ],
                "base_score": 75,
                "description": "Unilateral termination rights",
                "business_impact": "Contract can be ended without mutual agreement",
                "who_it_favors": "Party with termination rights",
                "sme_concern": "Loss of business continuity and planning certainty"
            },
            
            "ARBITRATION_JURISDICTION": {
                "patterns": [
                    r"arbitration.*[A-Za-z\s]+(delhi|mumbai|bangalore|chennai|kolkata)",
                    r"jurisdiction.*courts.*[A-Za-z\s]+(delhi|mumbai|bangalore|chennai|kolkata)",
                    r"disputes.*resolved.*[A-Za-z\s]+(delhi|mumbai|bangalore|chennai|kolkata)",
                    r"exclusive jurisdiction.*[A-Za-z\s]+(delhi|mumbai|bangalore|chennai|kolkata)"
                ],
                "base_score": 60,
                "description": "Jurisdiction or arbitration location clause",
                "business_impact": "Legal disputes must be resolved in specific location",
                "who_it_favors": "Party in the specified jurisdiction",
                "sme_concern": "Additional travel and legal costs for dispute resolution"
            },
            
            "AUTO_RENEWAL": {
                "patterns": [
                    r"automatically.*renew",
                    r"auto.*renewal",
                    r"extend.*automatically",
                    r"renew.*unless.*notice.*\d+.*days",
                    r"evergreen.*clause"
                ],
                "base_score": 65,
                "description": "Automatic renewal clause",
                "business_impact": "Contract continues without active decision",
                "who_it_favors": "Service provider or vendor",
                "sme_concern": "Difficulty exiting unfavorable agreements"
            },
            
            "NON_COMPETE": {
                "patterns": [
                    r"non.compete.*\d+.*years?",
                    r"restraint.*trade.*\d+.*years?",
                    r"not.*compete.*business.*\d+.*years?",
                    r"solicit.*employees.*\d+.*years?",
                    r"solicit.*customers.*\d+.*years?"
                ],
                "base_score": 70,
                "description": "Non-compete or restraint clause",
                "business_impact": "Restrictions on business activities after contract ends",
                "who_it_favors": "Other party seeking protection",
                "sme_concern": "Limits future business opportunities and growth"
            },
            
            "IP_ASSIGNMENT": {
                "patterns": [
                    r"intellectual property.*assign",
                    r"work.*hire.*ownership",
                    r"copyright.*assign.*company",
                    r"inventions.*belong.*company",
                    r"waive.*moral rights"
                ],
                "base_score": 75,
                "description": "Intellectual property assignment",
                "business_impact": "Loss of ownership of created work or inventions",
                "who_it_favors": "Party receiving IP rights",
                "sme_concern": "Loss of valuable intellectual assets and future revenue"
            },
            
            "UNLIMITED_LIABILITY": {
                "patterns": [
                    r"unlimited.*liability",
                    r"liability.*not.*limited",
                    r"full.*liability.*damages",
                    r"liable.*all.*losses",
                    r"no.*cap.*liability"
                ],
                "base_score": 90,
                "description": "Unlimited liability clause",
                "business_impact": "No limit on financial exposure for damages",
                "who_it_favors": "Other party seeking compensation",
                "sme_concern": "Catastrophic financial risk beyond business capacity"
            },
            
            "EXCLUSIVE_DEALING": {
                "patterns": [
                    r"exclusive.*supplier",
                    r"sole.*vendor",
                    r"exclusively.*purchase",
                    r"not.*engage.*competitors",
                    r"exclusive.*distribution"
                ],
                "base_score": 65,
                "description": "Exclusive dealing arrangement",
                "business_impact": "Restriction to single supplier or customer",
                "who_it_favors": "Exclusive partner",
                "sme_concern": "Loss of negotiating power and market flexibility"
            },
            
            "PERSONAL_GUARANTEE": {
                "patterns": [
                    r"personal.*guarantee",
                    r"director.*guarantee",
                    r"personally.*liable",
                    r"individual.*guarantee",
                    r"personal.*surety"
                ],
                "base_score": 85,
                "description": "Personal guarantee requirement",
                "business_impact": "Personal assets at risk for business obligations",
                "who_it_favors": "Creditor or service provider",
                "sme_concern": "Personal financial exposure beyond business assets"
            }
        }
        
        # Favorable clause patterns (lower risk)
        self.favorable_patterns = {
            "LIMITATION_LIABILITY": {
                "patterns": [
                    r"liability.*limited.*₹?\s*[\d,]+",
                    r"maximum.*liability.*₹?\s*[\d,]+",
                    r"cap.*liability.*₹?\s*[\d,]+",
                    r"liability.*not.*exceed.*contract value"
                ],
                "score_reduction": 20,
                "description": "Liability limitation clause"
            },
            
            "MUTUAL_TERMINATION": {
                "patterns": [
                    r"either party.*terminate.*\d+.*days.*notice",
                    r"mutual.*termination",
                    r"terminate.*\d+.*days.*written notice"
                ],
                "score_reduction": 15,
                "description": "Mutual termination rights"
            },
            
            "FORCE_MAJEURE": {
                "patterns": [
                    r"force majeure",
                    r"act of god",
                    r"circumstances beyond.*control",
                    r"pandemic.*epidemic.*force majeure"
                ],
                "score_reduction": 10,
                "description": "Force majeure protection"
            }
        }

    def analyze_clause_risk(self, clause_text: str, clause_type: str) -> List[RiskFlag]:
        """Analyze a single clause for risks"""
        risks = []
        clause_lower = clause_text.lower()
        
        # Check for high-risk patterns
        for risk_type, risk_config in self.risk_patterns.items():
            for pattern in risk_config["patterns"]:
                if re.search(pattern, clause_lower, re.IGNORECASE):
                    # Calculate risk score
                    base_score = risk_config["base_score"]
                    
                    # Adjust score based on clause context
                    adjusted_score = self._adjust_risk_score(
                        base_score, clause_text, clause_type, risk_type
                    )
                    
                    # Determine risk level
                    if adjusted_score >= 71:
                        risk_level = RiskLevel.HIGH
                    elif adjusted_score >= 31:
                        risk_level = RiskLevel.MEDIUM
                    else:
                        risk_level = RiskLevel.LOW
                    
                    risk = RiskFlag(
                        clause_text=clause_text[:200] + "..." if len(clause_text) > 200 else clause_text,
                        risk_type=risk_type,
                        risk_level=risk_level,
                        description=risk_config["description"],
                        business_impact=risk_config["business_impact"],
                        who_it_favors=risk_config["who_it_favors"],
                        sme_concern=risk_config["sme_concern"],
                        score=adjusted_score
                    )
                    risks.append(risk)
                    break  # Only flag once per risk type per clause
        
        return risks

    def _adjust_risk_score(self, base_score: int, clause_text: str, clause_type: str, risk_type: str) -> int:
        """Adjust risk score based on context and mitigating factors"""
        adjusted_score = base_score
        clause_lower = clause_text.lower()
        
        # Check for mitigating factors
        for favorable_type, favorable_config in self.favorable_patterns.items():
            for pattern in favorable_config["patterns"]:
                if re.search(pattern, clause_lower, re.IGNORECASE):
                    adjusted_score -= favorable_config["score_reduction"]
        
        # Context-specific adjustments
        if risk_type == "PENALTY_LIQUIDATED_DAMAGES":
            # Check if penalty amount is reasonable
            amounts = re.findall(r'₹\s*([\d,]+)', clause_text)
            if amounts:
                amount_str = amounts[0].replace(',', '')
                try:
                    amount = int(amount_str)
                    if amount < 10000:  # Small penalty
                        adjusted_score -= 15
                    elif amount > 1000000:  # Very large penalty
                        adjusted_score += 10
                except ValueError:
                    pass
        
        elif risk_type == "NON_COMPETE":
            # Check duration of non-compete
            durations = re.findall(r'(\d+)\s*years?', clause_lower)
            if durations:
                try:
                    years = int(durations[0])
                    if years <= 1:
                        adjusted_score -= 20
                    elif years >= 3:
                        adjusted_score += 15
                except ValueError:
                    pass
        
        elif risk_type == "UNILATERAL_TERMINATION":
            # Check if notice period is provided
            if re.search(r'\d+\s*days?\s*notice', clause_lower):
                adjusted_score -= 10
            if re.search(r'without.*notice', clause_lower):
                adjusted_score += 15
        
        # Ensure score stays within bounds
        return max(0, min(100, adjusted_score))

    def calculate_contract_risk_score(self, all_risks: List[RiskFlag]) -> Tuple[int, str]:
        """Calculate overall contract risk score"""
        if not all_risks:
            return 20, "LOW"  # Base low risk for contracts with no major issues
        
        # Weight risks by severity
        high_risks = [r for r in all_risks if r.risk_level == RiskLevel.HIGH]
        medium_risks = [r for r in all_risks if r.risk_level == RiskLevel.MEDIUM]
        low_risks = [r for r in all_risks if r.risk_level == RiskLevel.LOW]
        
        # Calculate weighted score
        total_score = 0
        total_weight = 0
        
        for risk in high_risks:
            total_score += risk.score * 3  # High risks weighted 3x
            total_weight += 3
        
        for risk in medium_risks:
            total_score += risk.score * 2  # Medium risks weighted 2x
            total_weight += 2
        
        for risk in low_risks:
            total_score += risk.score * 1  # Low risks weighted 1x
            total_weight += 1
        
        if total_weight == 0:
            overall_score = 20
        else:
            overall_score = min(100, total_score // total_weight)
        
        # Determine overall risk level
        if overall_score >= 71:
            risk_level = "HIGH"
        elif overall_score >= 31:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return overall_score, risk_level

    def analyze_contract_risks(self, clauses: List) -> Dict:
        """Analyze all contract clauses for risks"""
        logger.info("Starting contract risk analysis")
        
        all_risks = []
        clause_risks = {}
        
        for i, clause in enumerate(clauses):
            clause_risk_flags = self.analyze_clause_risk(clause.text, clause.clause_type)
            all_risks.extend(clause_risk_flags)
            
            if clause_risk_flags:
                clause_risks[f"clause_{i}"] = clause_risk_flags
        
        # Calculate overall risk score
        overall_score, overall_level = self.calculate_contract_risk_score(all_risks)
        
        # Categorize risks by type
        risk_summary = {
            "HIGH": [r for r in all_risks if r.risk_level == RiskLevel.HIGH],
            "MEDIUM": [r for r in all_risks if r.risk_level == RiskLevel.MEDIUM],
            "LOW": [r for r in all_risks if r.risk_level == RiskLevel.LOW]
        }
        
        result = {
            "overall_score": overall_score,
            "overall_level": overall_level,
            "total_risks": len(all_risks),
            "risk_summary": risk_summary,
            "clause_risks": clause_risks,
            "high_risk_count": len(risk_summary["HIGH"]),
            "medium_risk_count": len(risk_summary["MEDIUM"]),
            "low_risk_count": len(risk_summary["LOW"])
        }
        
        logger.info(f"Risk analysis completed. Overall score: {overall_score}, Level: {overall_level}")
        return result

    def get_risk_recommendations(self, risks: List[RiskFlag]) -> Dict[str, List[str]]:
        """Generate recommendations for identified risks"""
        recommendations = {
            "immediate_attention": [],
            "negotiate_changes": [],
            "seek_legal_review": [],
            "monitor_compliance": []
        }
        
        for risk in risks:
            if risk.risk_level == RiskLevel.HIGH:
                if risk.risk_type in ["UNLIMITED_LIABILITY", "PERSONAL_GUARANTEE"]:
                    recommendations["immediate_attention"].append(
                        f"CRITICAL: {risk.description} - {risk.sme_concern}"
                    )
                    recommendations["seek_legal_review"].append(
                        f"Have lawyer review {risk.risk_type.lower().replace('_', ' ')} clause"
                    )
                else:
                    recommendations["negotiate_changes"].append(
                        f"Negotiate to modify or remove {risk.description.lower()}"
                    )
            
            elif risk.risk_level == RiskLevel.MEDIUM:
                recommendations["negotiate_changes"].append(
                    f"Consider negotiating {risk.description.lower()} terms"
                )
                
            else:  # LOW risk
                recommendations["monitor_compliance"].append(
                    f"Monitor compliance with {risk.description.lower()}"
                )
        
        return recommendations