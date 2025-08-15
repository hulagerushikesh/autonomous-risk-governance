from agents.base import BaseAgent, AgentException
from typing import Dict, Any, List, Tuple
import json

class DecisionSupportAgent(BaseAgent):
    """Enhanced Decision Support Agent with sophisticated decision logic"""
    
    def __init__(self, name: str = "DecisionSupport"):
        super().__init__(name)
        self.decision_matrix = {
            'approve': {'min_score': 0.0, 'max_score': 0.3, 'conditions': ['low_risk', 'compliant']},
            'review': {'min_score': 0.3, 'max_score': 0.7, 'conditions': ['medium_risk']},
            'reject': {'min_score': 0.7, 'max_score': 1.0, 'conditions': ['high_risk', 'non_compliant']}
        }
        self.confidence_levels = {
            'high': 0.8,
            'medium': 0.6,
            'low': 0.4
        }
    
    def get_required_fields(self) -> list:
        """Return required input fields for decision support"""
        return ['risk_level']
    
    def _evaluate_logic(self, input_data: dict) -> dict:
        """Enhanced decision logic with confidence scoring and justification"""
        risk_level = input_data.get("risk_level", 1)
        risk_score = input_data.get("risk_score", 0.5)
        bias_score = input_data.get("bias_score", 0.0)
        features = input_data.get("features", [])
        
        # Validate risk level
        if not isinstance(risk_level, int) or risk_level not in [0, 1, 2]:
            raise AgentException(
                self.name,
                f"Risk level must be 0, 1, or 2, got {risk_level}"
            )
        
        # Primary decision logic
        primary_decision = self._make_primary_decision(risk_level)
        
        # Multi-factor decision analysis
        decision_analysis = self._analyze_decision_factors(
            risk_level, risk_score, bias_score, features
        )
        
        # Calculate confidence score
        confidence_score, confidence_level = self._calculate_confidence(decision_analysis)
        
        # Generate final recommendation
        final_decision = self._generate_final_decision(
            primary_decision, decision_analysis, confidence_score
        )
        
        # Create justification
        justification = self._create_justification(
            final_decision, decision_analysis, confidence_score
        )
        
        return {
            "decision": final_decision,
            "confidence_score": confidence_score,
            "confidence_level": confidence_level,
            "primary_decision": primary_decision,
            "decision_analysis": decision_analysis,
            "justification": justification,
            "alternative_options": self._get_alternative_options(decision_analysis),
            "escalation_required": self._check_escalation_needed(decision_analysis)
        }
    
    def _make_primary_decision(self, risk_level: int) -> str:
        """Make primary decision based on risk level"""
        decision_mapping = {0: "Approve", 1: "Review", 2: "Reject"}
        return decision_mapping.get(risk_level, "Review")
    
    def _analyze_decision_factors(self, risk_level: int, risk_score: float, 
                                bias_score: float, features: List[str]) -> Dict[str, Any]:
        """Analyze multiple factors affecting the decision"""
        analysis = {
            "risk_assessment": {
                "level": risk_level,
                "score": risk_score,
                "category": self._categorize_risk(risk_score)
            },
            "bias_assessment": {
                "score": bias_score,
                "acceptable": bias_score < 0.3,
                "impact": "high" if bias_score > 0.5 else "medium" if bias_score > 0.2 else "low"
            },
            "feature_analysis": {
                "count": len(features),
                "quality": self._assess_feature_quality(features),
                "completeness": len(features) >= 3
            },
            "compliance_factors": self._assess_compliance_factors(risk_score, bias_score),
            "business_impact": self._assess_business_impact(risk_level, risk_score)
        }
        
        return analysis
    
    def _categorize_risk(self, risk_score: float) -> str:
        """Categorize risk based on score"""
        if risk_score >= 0.7:
            return "high"
        elif risk_score >= 0.4:
            return "medium"
        else:
            return "low"
    
    def _assess_feature_quality(self, features: List[str]) -> str:
        """Assess quality of input features"""
        if len(features) >= 5:
            return "high"
        elif len(features) >= 3:
            return "medium"
        else:
            return "low"
    
    def _assess_compliance_factors(self, risk_score: float, bias_score: float) -> Dict[str, Any]:
        """Assess compliance-related factors"""
        return {
            "regulatory_compliance": risk_score < 0.7,
            "fairness_compliance": bias_score < 0.3,
            "overall_compliance": risk_score < 0.7 and bias_score < 0.3,
            "compliance_score": max(0, 1 - ((risk_score * 0.6) + (bias_score * 0.4)))
        }
    
    def _assess_business_impact(self, risk_level: int, risk_score: float) -> Dict[str, Any]:
        """Assess business impact of the decision"""
        return {
            "financial_impact": "high" if risk_level >= 2 else "medium" if risk_level == 1 else "low",
            "operational_impact": "significant" if risk_score > 0.8 else "moderate" if risk_score > 0.5 else "minimal",
            "reputational_risk": "high" if risk_score > 0.7 else "low",
            "customer_impact": self._assess_customer_impact(risk_level)
        }
    
    def _assess_customer_impact(self, risk_level: int) -> str:
        """Assess impact on customer experience"""
        impact_mapping = {
            0: "positive",
            1: "neutral", 
            2: "negative"
        }
        return impact_mapping.get(risk_level, "neutral")
    
    def _calculate_confidence(self, decision_analysis: Dict[str, Any]) -> Tuple[float, str]:
        """Calculate confidence score and level for the decision"""
        # Factor weights
        weights = {
            'risk_consistency': 0.3,
            'bias_acceptability': 0.25,
            'feature_quality': 0.2,
            'compliance': 0.25
        }
        
        # Calculate individual scores
        risk_score = 1.0 if decision_analysis['risk_assessment']['category'] != 'high' else 0.5
        bias_score = 1.0 if decision_analysis['bias_assessment']['acceptable'] else 0.3
        feature_score = {'high': 1.0, 'medium': 0.7, 'low': 0.4}[decision_analysis['feature_analysis']['quality']]
        compliance_score = decision_analysis['compliance_factors']['compliance_score']
        
        # Weighted confidence calculation
        confidence = (
            risk_score * weights['risk_consistency'] +
            bias_score * weights['bias_acceptability'] +
            feature_score * weights['feature_quality'] +
            compliance_score * weights['compliance']
        )
        
        # Determine confidence level
        if confidence >= 0.8:
            level = "high"
        elif confidence >= 0.6:
            level = "medium"
        else:
            level = "low"
        
        return round(confidence, 3), level
    
    def _generate_final_decision(self, primary_decision: str, analysis: Dict[str, Any], 
                               confidence: float) -> str:
        """Generate final decision considering all factors"""
        # Override logic for high-risk scenarios
        if (analysis['bias_assessment']['score'] > 0.5 or 
            analysis['risk_assessment']['score'] > 0.8):
            return "Reject"
        
        # Override for low confidence
        if confidence < 0.4:
            return "Review"
        
        return primary_decision
    
    def _create_justification(self, decision: str, analysis: Dict[str, Any], 
                            confidence: float) -> Dict[str, Any]:
        """Create detailed justification for the decision"""
        justification = {
            "decision_rationale": self._get_decision_rationale(decision, analysis),
            "key_factors": self._identify_key_factors(analysis),
            "risk_mitigation": self._suggest_risk_mitigation(analysis),
            "confidence_explanation": self._explain_confidence(confidence),
            "regulatory_considerations": self._get_regulatory_considerations(analysis)
        }
        
        return justification
    
    def _get_decision_rationale(self, decision: str, analysis: Dict[str, Any]) -> str:
        """Generate rationale for the decision"""
        risk_level = analysis['risk_assessment']['category']
        bias_acceptable = analysis['bias_assessment']['acceptable']
        
        rationales = {
            "Approve": f"Low risk profile ({risk_level}) and acceptable bias levels support approval",
            "Review": f"Medium risk profile or moderate concerns require additional review",
            "Reject": f"High risk profile ({risk_level}) or unacceptable bias levels mandate rejection"
        }
        
        return rationales.get(decision, "Decision based on comprehensive risk analysis")
    
    def _identify_key_factors(self, analysis: Dict[str, Any]) -> List[str]:
        """Identify key factors influencing the decision"""
        factors = []
        
        if analysis['risk_assessment']['score'] > 0.6:
            factors.append(f"High risk score: {analysis['risk_assessment']['score']}")
        
        if not analysis['bias_assessment']['acceptable']:
            factors.append(f"Bias concerns: {analysis['bias_assessment']['score']}")
        
        if not analysis['compliance_factors']['overall_compliance']:
            factors.append("Compliance issues detected")
        
        if analysis['feature_analysis']['quality'] == 'low':
            factors.append("Insufficient feature quality")
        
        return factors if factors else ["All factors within acceptable ranges"]
    
    def _suggest_risk_mitigation(self, analysis: Dict[str, Any]) -> List[str]:
        """Suggest risk mitigation strategies"""
        suggestions = []
        
        if analysis['risk_assessment']['score'] > 0.5:
            suggestions.append("Implement additional risk controls")
        
        if not analysis['bias_assessment']['acceptable']:
            suggestions.append("Apply bias mitigation techniques")
        
        if analysis['feature_analysis']['quality'] == 'low':
            suggestions.append("Enhance data collection and feature engineering")
        
        return suggestions
    
    def _explain_confidence(self, confidence: float) -> str:
        """Explain the confidence level"""
        if confidence >= 0.8:
            return "High confidence based on consistent risk indicators and quality data"
        elif confidence >= 0.6:
            return "Medium confidence with some uncertainty in risk assessment"
        else:
            return "Low confidence due to conflicting indicators or data quality issues"
    
    def _get_regulatory_considerations(self, analysis: Dict[str, Any]) -> List[str]:
        """Get regulatory considerations for the decision"""
        considerations = []
        
        if not analysis['compliance_factors']['regulatory_compliance']:
            considerations.append("Regulatory compliance review required")
        
        if not analysis['compliance_factors']['fairness_compliance']:
            considerations.append("Fairness assessment documentation needed")
        
        if analysis['business_impact']['reputational_risk'] == 'high':
            considerations.append("Reputational risk assessment required")
        
        return considerations
    
    def _get_alternative_options(self, analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Get alternative decision options"""
        alternatives = [
            {
                "option": "Conditional Approval",
                "description": "Approve with additional monitoring and conditions",
                "applicability": "Medium risk cases with good compliance"
            },
            {
                "option": "Escalated Review",
                "description": "Escalate to senior decision maker",
                "applicability": "High complexity or borderline cases"
            },
            {
                "option": "Request Additional Data",
                "description": "Request more information before deciding",
                "applicability": "Cases with insufficient data quality"
            }
        ]
        
        return alternatives
    
    def _check_escalation_needed(self, analysis: Dict[str, Any]) -> bool:
        """Check if escalation is required"""
        return (
            analysis['risk_assessment']['score'] > 0.8 or
            analysis['bias_assessment']['score'] > 0.5 or
            not analysis['compliance_factors']['overall_compliance'] or
            analysis['business_impact']['reputational_risk'] == 'high'
        )
    
    def report(self) -> dict:
        """Enhanced reporting with decision-specific metrics"""
        base_report = super().report()
        base_report.update({
            "decision_matrix": self.decision_matrix,
            "confidence_levels": self.confidence_levels,
            "agent_type": "decision_support"
        })
        return base_report
