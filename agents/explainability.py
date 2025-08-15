from agents.base import BaseAgent, AgentException
from typing import Dict, Any, List, Tuple
import json

class ExplainabilityAgent(BaseAgent):
    """Enhanced Explainability Agent with comprehensive model interpretation"""
    
    def __init__(self, name: str = "Explainability"):
        super().__init__(name)
        self.feature_importance_weights = {
            'credit_score': 0.25,
            'income': 0.20,
            'age': 0.15,
            'employment_status': 0.15,
            'debt_ratio': 0.10,
            'payment_history': 0.15
        }
        self.explanation_templates = {
            'high_risk': "High risk primarily due to {primary_factors}. Key concerns: {concerns}",
            'medium_risk': "Medium risk based on {primary_factors}. Monitor: {watch_factors}",
            'low_risk': "Low risk assessment supported by {positive_factors}"
        }
    
    def get_required_fields(self) -> list:
        """Return required input fields for explainability"""
        return ['features']
    
    def _evaluate_logic(self, input_data: dict) -> dict:
        """Enhanced explainability with detailed feature analysis"""
        features = input_data.get("features", [])
        risk_score = input_data.get("risk_score", 0.5)
        bias_score = input_data.get("bias_score", 0.0)
        decision = input_data.get("decision", "Review")
        
        # Validate features
        if not features:
            raise AgentException(
                self.name,
                "At least one feature is required for explanation generation"
            )
        
        # Generate comprehensive explanation
        explanation_components = self._generate_explanation_components(
            features, risk_score, bias_score, decision
        )
        
        # Feature importance analysis
        feature_analysis = self._analyze_feature_importance(features, risk_score)
        
        # Generate natural language explanations
        natural_explanations = self._generate_natural_explanations(
            explanation_components, feature_analysis, risk_score
        )
        
        # Create SHAP-like explanations
        shap_explanations = self._generate_shap_explanations(features, risk_score)
        
        # Generate counterfactual explanations
        counterfactuals = self._generate_counterfactual_explanations(
            features, risk_score, decision
        )
        
        return {
            "explanation": natural_explanations['primary'],
            "detailed_explanation": natural_explanations['detailed'],
            "feature_importance": feature_analysis,
            "explanation_components": explanation_components,
            "shap_explanations": shap_explanations,
            "counterfactual_explanations": counterfactuals,
            "confidence_in_explanation": self._calculate_explanation_confidence(features),
            "alternative_interpretations": self._generate_alternative_interpretations(
                features, risk_score
            )
        }
    
    def _generate_explanation_components(self, features: List[str], risk_score: float, 
                                       bias_score: float, decision: str) -> Dict[str, Any]:
        """Generate structured explanation components"""
        return {
            "model_decision": {
                "decision": decision,
                "risk_score": risk_score,
                "confidence": self._calculate_decision_confidence(risk_score)
            },
            "feature_contributions": self._calculate_feature_contributions_list(features, risk_score),
            "bias_factors": {
                "bias_score": bias_score,
                "bias_impact": "significant" if bias_score > 0.3 else "minimal",
                "affected_groups": self._identify_affected_groups(features, bias_score)
            },
            "decision_boundary": self._explain_decision_boundary(risk_score),
            "uncertainty_factors": self._identify_uncertainty_factors(features, risk_score)
        }
    
    def _analyze_feature_importance(self, features: List[str], risk_score: float) -> Dict[str, Any]:
        """Analyze importance of each feature"""
        feature_importance = {}
        
        for feature in features:
            # Get base importance from weights
            base_importance = self.feature_importance_weights.get(feature.lower(), 0.05)
            
            # Adjust based on risk score
            adjusted_importance = self._adjust_importance_by_risk(base_importance, risk_score)
            
            # Calculate contribution direction
            contribution = self._calculate_feature_contribution(feature, risk_score)
            
            feature_importance[feature] = {
                "importance_score": adjusted_importance,
                "contribution": contribution,
                "impact": self._categorize_impact(adjusted_importance),
                "explanation": self._explain_feature_impact(feature, contribution)
            }
        
        # Sort by importance
        sorted_features = sorted(
            feature_importance.items(), 
            key=lambda x: x[1]['importance_score'], 
            reverse=True
        )
        
        return {
            "ranked_features": dict(sorted_features),
            "top_3_features": dict(sorted_features[:3]),
            "feature_summary": self._summarize_feature_importance(sorted_features)
        }
    
    def _adjust_importance_by_risk(self, base_importance: float, risk_score: float) -> float:
        """Adjust feature importance based on overall risk score"""
        # Higher risk scores amplify importance of risk-contributing features
        risk_multiplier = 1 + (risk_score * 0.5)
        return min(1.0, base_importance * risk_multiplier)
    
    def _calculate_feature_contributions_list(self, features: List[str], risk_score: float) -> Dict[str, Any]:
        """Calculate contributions for a list of features"""
        contributions = {}
        for feature in features:
            contributions[feature] = self._calculate_feature_contribution(feature, risk_score)
        return contributions
    
    def _calculate_feature_contribution(self, feature: str, risk_score: float) -> Dict[str, Any]:
        """Calculate how a feature contributes to the final score"""
        # Simplified contribution calculation
        base_weight = self.feature_importance_weights.get(feature.lower(), 0.05)
        
        # Determine contribution direction based on feature type
        if feature.lower() in ['credit_score', 'income', 'employment_status']:
            direction = "risk_reducing" if risk_score < 0.5 else "risk_neutral"
        elif feature.lower() in ['age', 'debt_ratio']:
            direction = "risk_increasing" if risk_score > 0.5 else "risk_neutral"
        else:
            direction = "risk_neutral"
        
        magnitude = base_weight * (2 if direction == "risk_increasing" else 1)
        
        return {
            "direction": direction,
            "magnitude": magnitude,
            "normalized_contribution": magnitude / sum(self.feature_importance_weights.values())
        }
    
    def _categorize_impact(self, importance_score: float) -> str:
        """Categorize the impact level of a feature"""
        if importance_score >= 0.3:
            return "high"
        elif importance_score >= 0.15:
            return "medium"
        else:
            return "low"
    
    def _explain_feature_impact(self, feature: str, contribution: Dict[str, Any]) -> str:
        """Generate explanation for individual feature impact"""
        direction = contribution['direction']
        magnitude = contribution['magnitude']
        
        explanations = {
            "risk_increasing": f"{feature} contributes to increased risk assessment",
            "risk_reducing": f"{feature} helps reduce the overall risk profile",
            "risk_neutral": f"{feature} has minimal impact on risk assessment"
        }
        
        return explanations.get(direction, f"{feature} influences the model decision")
    
    def _generate_natural_explanations(self, components: Dict[str, Any], 
                                     feature_analysis: Dict[str, Any], 
                                     risk_score: float) -> Dict[str, str]:
        """Generate human-readable explanations"""
        # Primary explanation
        top_features = list(feature_analysis['top_3_features'].keys())
        risk_level = "high" if risk_score > 0.7 else "medium" if risk_score > 0.3 else "low"
        
        primary = f"The model's {risk_level} risk assessment is primarily based on {', '.join(top_features[:2])}."
        
        # Detailed explanation
        detailed_parts = [
            f"Risk Score: {risk_score:.2f} ({risk_level} risk)",
            f"Primary factors: {', '.join(top_features)}",
            f"Decision confidence: {components['model_decision']['confidence']:.2f}"
        ]
        
        if components['bias_factors']['bias_score'] > 0.3:
            detailed_parts.append(f"Bias concerns identified (score: {components['bias_factors']['bias_score']:.2f})")
        
        detailed = ". ".join(detailed_parts) + "."
        
        return {
            "primary": primary,
            "detailed": detailed
        }
    
    def _generate_shap_explanations(self, features: List[str], risk_score: float) -> Dict[str, Any]:
        """Generate SHAP-like explanations"""
        base_value = 0.5  # Baseline risk score
        
        shap_values = {}
        for feature in features:
            # Simplified SHAP value calculation
            contribution = self._calculate_feature_contribution(feature, risk_score)
            
            if contribution['direction'] == "risk_increasing":
                shap_value = contribution['magnitude'] * 0.3
            elif contribution['direction'] == "risk_reducing":
                shap_value = -contribution['magnitude'] * 0.3
            else:
                shap_value = 0.0
            
            shap_values[feature] = shap_value
        
        return {
            "base_value": base_value,
            "shap_values": shap_values,
            "predicted_value": base_value + sum(shap_values.values()),
            "explanation": f"Starting from baseline risk of {base_value}, features collectively adjust the score"
        }
    
    def _generate_counterfactual_explanations(self, features: List[str], 
                                            risk_score: float, 
                                            decision: str) -> Dict[str, Any]:
        """Generate counterfactual explanations"""
        counterfactuals = []
        
        # If high risk, suggest what would make it lower
        if risk_score > 0.6:
            counterfactuals.extend([
                "If credit score was higher, risk would be reduced",
                "If debt ratio was lower, the decision might change to approval",
                "With better employment status, the risk assessment would improve"
            ])
        
        # If low risk, explain what would make it higher
        elif risk_score < 0.4:
            counterfactuals.extend([
                "If payment history was poor, risk would increase significantly",
                "Higher debt levels would change the risk category",
                "Unstable employment would elevate the risk score"
            ])
        
        return {
            "what_if_scenarios": counterfactuals,
            "threshold_analysis": self._analyze_decision_thresholds(risk_score, decision),
            "minimal_changes": self._suggest_minimal_changes(features, risk_score)
        }
    
    def _analyze_decision_thresholds(self, risk_score: float, decision: str) -> Dict[str, Any]:
        """Analyze how close the decision is to threshold boundaries"""
        thresholds = {"Approve": 0.3, "Review": 0.7, "Reject": 1.0}
        
        current_threshold = 0.3 if decision == "Approve" else 0.7 if decision == "Review" else 1.0
        distance_to_next = abs(risk_score - current_threshold)
        
        return {
            "current_decision": decision,
            "risk_score": risk_score,
            "threshold": current_threshold,
            "distance_to_threshold": distance_to_next,
            "stability": "stable" if distance_to_next > 0.1 else "borderline"
        }
    
    def _suggest_minimal_changes(self, features: List[str], risk_score: float) -> List[str]:
        """Suggest minimal changes that would affect the decision"""
        suggestions = []
        
        if 0.25 < risk_score < 0.35:
            suggestions.append("Small improvement in credit score could change decision to approval")
        elif 0.65 < risk_score < 0.75:
            suggestions.append("Minor reduction in debt ratio might avoid rejection")
        
        if 'income' in [f.lower() for f in features]:
            suggestions.append("Income increase would positively impact the assessment")
        
        return suggestions
    
    def _calculate_decision_confidence(self, risk_score: float) -> float:
        """Calculate confidence in the decision based on risk score"""
        # Higher confidence when score is clearly in one category
        if risk_score <= 0.2 or risk_score >= 0.8:
            return 0.9
        elif risk_score <= 0.35 or risk_score >= 0.65:
            return 0.7
        else:
            return 0.5
    
    def _identify_affected_groups(self, features: List[str], bias_score: float) -> List[str]:
        """Identify groups potentially affected by bias"""
        affected = []
        
        if bias_score > 0.3:
            protected_attributes = ['age', 'gender', 'race', 'income']
            for attr in protected_attributes:
                if attr in [f.lower() for f in features]:
                    affected.append(f"Groups defined by {attr}")
        
        return affected
    
    def _explain_decision_boundary(self, risk_score: float) -> Dict[str, str]:
        """Explain decision boundaries"""
        if risk_score <= 0.3:
            return {
                "current_zone": "approval",
                "boundary_explanation": "Score is well within approval range",
                "next_boundary": "review zone starts at 0.3"
            }
        elif risk_score <= 0.7:
            return {
                "current_zone": "review",
                "boundary_explanation": "Score requires additional review",
                "next_boundary": "rejection zone starts at 0.7"
            }
        else:
            return {
                "current_zone": "rejection",
                "boundary_explanation": "Score exceeds acceptable risk threshold",
                "next_boundary": "no higher boundary"
            }
    
    def _identify_uncertainty_factors(self, features: List[str], risk_score: float) -> List[str]:
        """Identify factors contributing to prediction uncertainty"""
        uncertainty_factors = []
        
        if len(features) < 3:
            uncertainty_factors.append("Limited feature set increases prediction uncertainty")
        
        if 0.4 <= risk_score <= 0.6:
            uncertainty_factors.append("Risk score in borderline range increases uncertainty")
        
        return uncertainty_factors
    
    def _summarize_feature_importance(self, sorted_features: List[Tuple]) -> str:
        """Summarize overall feature importance"""
        if not sorted_features:
            return "No features provided for analysis"
        
        top_feature = sorted_features[0][0]
        top_importance = sorted_features[0][1]['importance_score']
        
        return f"'{top_feature}' is the most influential factor (importance: {top_importance:.2f})"
    
    def _calculate_explanation_confidence(self, features: List[str]) -> float:
        """Calculate confidence in the explanation quality"""
        # More features generally mean more confident explanations
        feature_factor = min(1.0, len(features) / 5)
        
        # Check if we have important features
        important_features = [f for f in features if f.lower() in self.feature_importance_weights]
        coverage_factor = len(important_features) / max(1, len(features))
        
        return round((feature_factor * 0.6) + (coverage_factor * 0.4), 2)
    
    def _generate_alternative_interpretations(self, features: List[str], 
                                            risk_score: float) -> List[Dict[str, str]]:
        """Generate alternative interpretations of the model decision"""
        alternatives = []
        
        # Conservative interpretation
        alternatives.append({
            "perspective": "conservative",
            "interpretation": "Focus on risk mitigation and regulatory compliance",
            "emphasis": "Prioritize false positive reduction"
        })
        
        # Business-focused interpretation
        alternatives.append({
            "perspective": "business_focused",
            "interpretation": "Balance risk with business opportunity",
            "emphasis": "Optimize for profitability while managing risk"
        })
        
        # Fairness-focused interpretation
        alternatives.append({
            "perspective": "fairness_focused",
            "interpretation": "Emphasize equitable treatment across all groups",
            "emphasis": "Minimize bias and ensure fair outcomes"
        })
        
        return alternatives
    
    def report(self) -> dict:
        """Enhanced reporting with explainability-specific metrics"""
        base_report = super().report()
        base_report.update({
            "feature_weights": self.feature_importance_weights,
            "explanation_templates": self.explanation_templates,
            "agent_type": "explainability"
        })
        return base_report
