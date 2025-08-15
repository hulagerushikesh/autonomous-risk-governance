from agents.base import BaseAgent, AgentException
from typing import Dict, Any, List

class BiasAuditingAgent(BaseAgent):
    """Enhanced Bias Auditing Agent with detailed fairness analysis"""
    
    def __init__(self, name: str = "BiasAudit", bias_threshold: float = 0.3):
        super().__init__(name)
        self.bias_threshold = bias_threshold
        self.protected_attributes = ['age', 'gender', 'race', 'income_level']
        self.bias_metrics = {
            'demographic_parity': 0.8,
            'equal_opportunity': 0.8,
            'calibration': 0.8
        }
    
    def get_required_fields(self) -> list:
        """Return required input fields for bias evaluation"""
        return ['bias_score']
    
    def _evaluate_logic(self, input_data: dict) -> dict:
        """Enhanced bias evaluation with multiple fairness metrics"""
        bias_score = input_data.get("bias_score", 0.0)
        features = input_data.get("features", [])
        
        # Validate bias score range
        if not 0 <= bias_score <= 1:
            raise AgentException(
                self.name,
                f"Bias score must be between 0 and 1, got {bias_score}"
            )
        
        # Primary bias check
        flagged = bias_score > self.bias_threshold
        
        # Detailed bias analysis
        bias_analysis = self._analyze_bias_components(bias_score, features)
        
        # Risk level assessment
        risk_level = self._assess_bias_risk_level(bias_score)
        
        # Generate recommendations
        recommendations = self._generate_bias_recommendations(bias_score, flagged, features)
        
        return {
            "bias_flagged": flagged,
            "bias_score": bias_score,
            "bias_risk_level": risk_level,
            "bias_analysis": bias_analysis,
            "recommendations": recommendations,
            "fairness_metrics": self._calculate_fairness_metrics(bias_score),
            "protected_attributes_impact": self._assess_protected_attributes(features)
        }
    
    def _analyze_bias_components(self, bias_score: float, features: List[str]) -> Dict[str, Any]:
        """Analyze different components contributing to bias"""
        return {
            "overall_bias": {
                "score": bias_score,
                "threshold": self.bias_threshold,
                "status": "flagged" if bias_score > self.bias_threshold else "acceptable"
            },
            "feature_bias": self._assess_feature_bias(features),
            "demographic_impact": self._assess_demographic_impact(bias_score),
            "historical_comparison": {
                "trend": "stable",  # This would be calculated from historical data
                "variance": 0.05
            }
        }
    
    def _assess_feature_bias(self, features: List[str]) -> Dict[str, str]:
        """Assess potential bias from specific features"""
        feature_bias = {}
        
        for feature in features:
            if feature.lower() in ['age', 'gender', 'race', 'ethnicity']:
                feature_bias[feature] = "high_risk"
            elif feature.lower() in ['income', 'education', 'employment']:
                feature_bias[feature] = "medium_risk"
            else:
                feature_bias[feature] = "low_risk"
        
        return feature_bias
    
    def _assess_demographic_impact(self, bias_score: float) -> Dict[str, Any]:
        """Assess impact on different demographic groups"""
        return {
            "disparate_impact": bias_score > 0.4,
            "statistical_parity": bias_score < 0.2,
            "individual_fairness": bias_score < 0.25,
            "group_fairness": bias_score < 0.3
        }
    
    def _assess_bias_risk_level(self, bias_score: float) -> str:
        """Determine bias risk level"""
        if bias_score >= 0.7:
            return "critical"
        elif bias_score >= 0.5:
            return "high"
        elif bias_score >= self.bias_threshold:
            return "medium"
        else:
            return "low"
    
    def _generate_bias_recommendations(self, bias_score: float, flagged: bool, features: List[str]) -> List[str]:
        """Generate actionable recommendations for bias mitigation"""
        recommendations = []
        
        if flagged:
            recommendations.extend([
                "Immediate bias investigation required",
                "Review feature selection and model training data",
                "Consider bias mitigation techniques (reweighting, adversarial training)",
                "Conduct fairness-aware model evaluation"
            ])
            
            # Feature-specific recommendations
            protected_features = [f for f in features if f.lower() in self.protected_attributes]
            if protected_features:
                recommendations.append(f"Review use of protected attributes: {protected_features}")
        
        elif bias_score > 0.2:
            recommendations.extend([
                "Monitor bias metrics regularly",
                "Consider implementing bias monitoring dashboard",
                "Review model performance across demographic groups"
            ])
        
        else:
            recommendations.append("Bias levels acceptable, maintain current monitoring")
        
        return recommendations
    
    def _calculate_fairness_metrics(self, bias_score: float) -> Dict[str, float]:
        """Calculate various fairness metrics"""
        return {
            "demographic_parity": max(0, 1 - bias_score),
            "equal_opportunity": max(0, 1 - (bias_score * 1.2)),
            "calibration": max(0, 1 - (bias_score * 0.8)),
            "individual_fairness": max(0, 1 - (bias_score * 1.1))
        }
    
    def _assess_protected_attributes(self, features: List[str]) -> Dict[str, str]:
        """Assess impact of protected attributes"""
        impact_assessment = {}
        
        for attr in self.protected_attributes:
            if attr in [f.lower() for f in features]:
                impact_assessment[attr] = "direct_usage_detected"
            else:
                impact_assessment[attr] = "no_direct_usage"
        
        return impact_assessment
    
    def update_threshold(self, new_threshold: float):
        """Update bias threshold"""
        if not 0 <= new_threshold <= 1:
            raise AgentException(
                self.name,
                f"Threshold must be between 0 and 1, got {new_threshold}"
            )
        
        old_threshold = self.bias_threshold
        self.bias_threshold = new_threshold
        
        self.logger.info(f"Bias threshold updated from {old_threshold} to {new_threshold}")
    
    def report(self) -> dict:
        """Enhanced reporting with bias-specific metrics"""
        base_report = super().report()
        base_report.update({
            "bias_threshold": self.bias_threshold,
            "protected_attributes": self.protected_attributes,
            "bias_metrics": self.bias_metrics,
            "agent_type": "bias_auditing"
        })
        return base_report
