from agents.base import BaseAgent, AgentException
from typing import Dict, Any

class ComplianceAgent(BaseAgent):
    """Enhanced Compliance Agent with configurable thresholds and detailed reporting"""
    
    def __init__(self, name: str = "Compliance", risk_threshold: float = 0.7):
        super().__init__(name)
        self.risk_threshold = risk_threshold
        self.compliance_rules = {
            'max_risk_score': risk_threshold,
            'min_data_quality': 0.8,
            'required_documentation': True
        }
    
    def get_required_fields(self) -> list:
        """Return required input fields for compliance evaluation"""
        return ['risk_score']
    
    def _evaluate_logic(self, input_data: dict) -> dict:
        """Enhanced compliance evaluation with multiple checks"""
        risk_score = input_data.get("risk_score", 0)
        
        # Validate risk score range
        if not 0 <= risk_score <= 1:
            raise AgentException(
                self.name, 
                f"Risk score must be between 0 and 1, got {risk_score}"
            )
        
        # Primary compliance check
        compliant = risk_score < self.risk_threshold
        
        # Additional compliance checks
        compliance_details = {
            'risk_threshold_check': {
                'passed': compliant,
                'threshold': self.risk_threshold,
                'actual_score': risk_score,
                'margin': self.risk_threshold - risk_score
            }
        }
        
        # Determine compliance level
        if risk_score < 0.3:
            compliance_level = "high"
        elif risk_score < self.risk_threshold:
            compliance_level = "medium"
        else:
            compliance_level = "low"
        
        # Generate recommendations
        recommendations = self._generate_recommendations(risk_score, compliant)
        
        return {
            "compliant": compliant,
            "compliance_level": compliance_level,
            "risk_score": risk_score,
            "compliance_details": compliance_details,
            "recommendations": recommendations,
            "regulatory_notes": self._get_regulatory_notes(risk_score)
        }
    
    def _generate_recommendations(self, risk_score: float, compliant: bool) -> list:
        """Generate actionable recommendations based on compliance status"""
        recommendations = []
        
        if not compliant:
            recommendations.extend([
                "Immediate review required due to high risk score",
                "Consider additional risk mitigation measures",
                "Document justification for proceeding with this risk level"
            ])
        elif risk_score > 0.5:
            recommendations.extend([
                "Monitor closely for risk escalation",
                "Review risk factors quarterly"
            ])
        else:
            recommendations.append("Risk level acceptable, standard monitoring applies")
        
        return recommendations
    
    def _get_regulatory_notes(self, risk_score: float) -> str:
        """Provide regulatory context based on risk score"""
        if risk_score >= 0.8:
            return "High-risk classification may require additional regulatory approval"
        elif risk_score >= 0.5:
            return "Medium-risk classification requires enhanced due diligence"
        else:
            return "Low-risk classification allows standard processing"
    
    def update_threshold(self, new_threshold: float):
        """Update risk threshold for compliance evaluation"""
        if not 0 <= new_threshold <= 1:
            raise AgentException(
                self.name,
                f"Threshold must be between 0 and 1, got {new_threshold}"
            )
        
        old_threshold = self.risk_threshold
        self.risk_threshold = new_threshold
        self.compliance_rules['max_risk_score'] = new_threshold
        
        self.logger.info(f"Compliance threshold updated from {old_threshold} to {new_threshold}")
    
    def report(self) -> dict:
        """Enhanced reporting with compliance-specific metrics"""
        base_report = super().report()
        base_report.update({
            "compliance_threshold": self.risk_threshold,
            "compliance_rules": self.compliance_rules,
            "agent_type": "compliance_verification"
        })
        return base_report
