from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
import traceback
from agents.base import BaseAgent, AgentException
from utils.logger import RiskGovernanceLogger

class OrchestrationException(Exception):
    """Custom exception for orchestration-related errors"""
    pass

class AgentOrchestrator:
    """Enhanced Agent Orchestrator with error handling, parallel execution, and metrics"""
    
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
        self.logger = RiskGovernanceLogger().get_logger()
        self.execution_history: List[Dict[str, Any]] = []
        self.performance_metrics = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'average_execution_time': 0.0
        }
        self.agent_status = {agent.name: 'healthy' for agent in agents}
    
    def run(self, input_data: dict, parallel: bool = False, 
            continue_on_error: bool = True) -> dict:
        """Enhanced orchestration with options for parallel execution and error handling"""
        start_time = datetime.now()
        execution_id = f"exec_{int(start_time.timestamp())}"
        
        self.logger.info(f"Starting orchestration {execution_id} with {len(self.agents)} agents")
        
        try:
            # Validate input data
            self._validate_input_data(input_data)
            
            # Execute agents
            if parallel:
                results = self._run_parallel(input_data, continue_on_error)
            else:
                results = self._run_sequential(input_data, continue_on_error)
            
            # Calculate execution metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Generate orchestration summary
            orchestration_summary = self._generate_summary(results, execution_time, execution_id)
            
            # Update performance metrics
            self._update_performance_metrics(execution_time, success=True)
            
            # Store execution history
            self._store_execution_history(execution_id, input_data, results, execution_time, True)
            
            # Combine results with summary
            final_results = {
                'agent_results': results,
                'orchestration_summary': orchestration_summary,
                'execution_metadata': {
                    'execution_id': execution_id,
                    'execution_time': execution_time,
                    'timestamp': start_time.isoformat(),
                    'input_data': input_data
                }
            }
            
            self.logger.info(f"Orchestration {execution_id} completed successfully in {execution_time:.3f}s")
            return final_results
            
        except Exception as e:
            self.logger.error(f"Orchestration {execution_id} failed: {traceback.format_exc()}")
            self._update_performance_metrics(0, success=False)
            
            # Store failed execution
            self._store_execution_history(execution_id, input_data, {}, 0, False, str(e))
            
            raise OrchestrationException(f"Orchestration failed: {str(e)}") from e
    
    def _validate_input_data(self, input_data: dict):
        """Validate input data format and completeness"""
        if not isinstance(input_data, dict):
            raise OrchestrationException("Input data must be a dictionary")
        
        # Check for minimum required fields
        required_fields = ['risk_score', 'bias_score', 'risk_level', 'features']
        missing_fields = [field for field in required_fields if field not in input_data]
        
        if missing_fields:
            raise OrchestrationException(f"Missing required fields: {missing_fields}")
        
        # Validate data types and ranges
        self._validate_field_types(input_data)
    
    def _validate_field_types(self, input_data: dict):
        """Validate data types and value ranges"""
        validations = [
            ('risk_score', float, lambda x: 0 <= x <= 1),
            ('bias_score', float, lambda x: 0 <= x <= 1),
            ('risk_level', int, lambda x: x in [0, 1, 2]),
            ('features', list, lambda x: len(x) > 0)
        ]
        
        for field, expected_type, validator in validations:
            if field in input_data:
                value = input_data[field]
                
                # Type check
                if not isinstance(value, expected_type):
                    raise OrchestrationException(
                        f"Field '{field}' must be of type {expected_type.__name__}, got {type(value).__name__}"
                    )
                
                # Range/validation check
                if not validator(value):
                    raise OrchestrationException(f"Field '{field}' failed validation: {value}")
    
    def _run_sequential(self, input_data: dict, continue_on_error: bool) -> dict:
        """Run agents sequentially with error handling"""
        results = {}
        failed_agents = []
        
        for agent in self.agents:
            try:
                self.logger.info(f"Executing agent: {agent.name}")
                agent_start_time = datetime.now()
                
                result = agent.evaluate(input_data)
                
                agent_execution_time = (datetime.now() - agent_start_time).total_seconds()
                result['execution_time'] = agent_execution_time
                
                results[agent.name] = result
                self.agent_status[agent.name] = 'healthy'
                
                self.logger.info(f"Agent {agent.name} completed successfully in {agent_execution_time:.3f}s")
                
            except Exception as e:
                error_msg = f"Agent {agent.name} failed: {str(e)}"
                self.logger.error(error_msg)
                
                failed_agents.append(agent.name)
                self.agent_status[agent.name] = 'failed'
                
                if continue_on_error:
                    results[agent.name] = {
                        'error': error_msg,
                        'status': 'failed',
                        'execution_time': 0
                    }
                else:
                    raise OrchestrationException(error_msg) from e
        
        if failed_agents and not continue_on_error:
            raise OrchestrationException(f"Agents failed: {failed_agents}")
        
        return results
    
    def _run_parallel(self, input_data: dict, continue_on_error: bool) -> dict:
        """Run agents in parallel using asyncio"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            return loop.run_until_complete(
                self._async_run_agents(input_data, continue_on_error)
            )
        finally:
            loop.close()
    
    async def _async_run_agents(self, input_data: dict, continue_on_error: bool) -> dict:
        """Async method to run agents in parallel"""
        tasks = []
        
        for agent in self.agents:
            task = asyncio.create_task(self._async_agent_wrapper(agent, input_data))
            tasks.append((agent.name, task))
        
        results = {}
        failed_agents = []
        
        for agent_name, task in tasks:
            try:
                result = await task
                results[agent_name] = result
                self.agent_status[agent_name] = 'healthy'
                
            except Exception as e:
                error_msg = f"Agent {agent_name} failed: {str(e)}"
                self.logger.error(error_msg)
                
                failed_agents.append(agent_name)
                self.agent_status[agent_name] = 'failed'
                
                if continue_on_error:
                    results[agent_name] = {
                        'error': error_msg,
                        'status': 'failed',
                        'execution_time': 0
                    }
                else:
                    raise OrchestrationException(error_msg) from e
        
        return results
    
    async def _async_agent_wrapper(self, agent: BaseAgent, input_data: dict) -> dict:
        """Async wrapper for agent execution"""
        start_time = datetime.now()
        
        # Run agent in thread pool since it's not async
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, agent.evaluate, input_data)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        result['execution_time'] = execution_time
        
        return result
    
    def _generate_summary(self, results: dict, execution_time: float, execution_id: str) -> dict:
        """Generate orchestration summary with insights"""
        successful_agents = [name for name, result in results.items() 
                           if 'error' not in result]
        failed_agents = [name for name, result in results.items() 
                        if 'error' in result]
        
        # Extract key metrics from agent results
        risk_scores = []
        bias_scores = []
        decisions = []
        
        for agent_name, result in results.items():
            if 'error' not in result:
                if 'risk_score' in result:
                    risk_scores.append(result['risk_score'])
                if 'bias_score' in result:
                    bias_scores.append(result['bias_score'])
                if 'decision' in result:
                    decisions.append(result['decision'])
        
        # Generate insights
        insights = self._generate_insights(results)
        
        summary = {
            'execution_id': execution_id,
            'total_agents': len(self.agents),
            'successful_agents': len(successful_agents),
            'failed_agents': len(failed_agents),
            'success_rate': len(successful_agents) / len(self.agents),
            'total_execution_time': execution_time,
            'average_agent_time': execution_time / len(self.agents),
            'agent_status': self.agent_status.copy(),
            'overall_status': 'success' if not failed_agents else 'partial_failure' if successful_agents else 'failure',
            'insights': insights,
            'recommendations': self._generate_recommendations(results, insights)
        }
        
        return summary
    
    def _generate_insights(self, results: dict) -> dict:
        """Generate insights from agent results"""
        insights = {
            'consensus_analysis': {},
            'conflict_detection': [],
            'confidence_assessment': {},
            'risk_factors': []
        }
        
        # Analyze consensus between agents
        decisions = []
        compliance_results = []
        
        for agent_name, result in results.items():
            if 'error' not in result:
                if 'decision' in result:
                    decisions.append(result['decision'])
                if 'compliant' in result:
                    compliance_results.append(result['compliant'])
        
        # Consensus analysis
        if decisions:
            decision_consensus = len(set(decisions)) == 1
            insights['consensus_analysis']['decision_consensus'] = decision_consensus
            insights['consensus_analysis']['primary_decision'] = max(set(decisions), key=decisions.count) if decisions else None
        
        # Conflict detection
        if 'Compliance' in results and 'DecisionSupport' in results:
            compliance_result = results['Compliance']
            decision_result = results['DecisionSupport']
            
            if ('compliant' in compliance_result and 'decision' in decision_result and
                not compliance_result['compliant'] and decision_result['decision'] == 'Approve'):
                insights['conflict_detection'].append(
                    "Conflict: Non-compliant assessment but approval decision"
                )
        
        return insights
    
    def _generate_recommendations(self, results: dict, insights: dict) -> List[str]:
        """Generate recommendations based on orchestration results"""
        recommendations = []
        
        # Consensus-based recommendations
        if not insights['consensus_analysis'].get('decision_consensus', True):
            recommendations.append("Review conflicting agent decisions for consistency")
        
        # Error-based recommendations
        failed_agents = [name for name, result in results.items() if 'error' in result]
        if failed_agents:
            recommendations.append(f"Investigate failures in agents: {', '.join(failed_agents)}")
        
        # Performance recommendations
        slow_agents = [name for name, result in results.items() 
                      if 'execution_time' in result and result['execution_time'] > 1.0]
        if slow_agents:
            recommendations.append(f"Optimize performance for agents: {', '.join(slow_agents)}")
        
        return recommendations
    
    def _update_performance_metrics(self, execution_time: float, success: bool):
        """Update orchestrator performance metrics"""
        self.performance_metrics['total_executions'] += 1
        
        if success:
            self.performance_metrics['successful_executions'] += 1
        else:
            self.performance_metrics['failed_executions'] += 1
        
        # Update average execution time
        total_time = (self.performance_metrics['average_execution_time'] * 
                     (self.performance_metrics['total_executions'] - 1) + execution_time)
        self.performance_metrics['average_execution_time'] = total_time / self.performance_metrics['total_executions']
    
    def _store_execution_history(self, execution_id: str, input_data: dict, 
                                results: dict, execution_time: float, 
                                success: bool, error_msg: str = None):
        """Store execution history for analysis"""
        history_entry = {
            'execution_id': execution_id,
            'timestamp': datetime.now().isoformat(),
            'input_data': input_data,
            'results': results,
            'execution_time': execution_time,
            'success': success,
            'error_message': error_msg
        }
        
        self.execution_history.append(history_entry)
        
        # Keep only last 100 executions
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]
    
    def get_health_status(self) -> dict:
        """Get orchestrator and agent health status"""
        return {
            'orchestrator_status': 'healthy' if self.performance_metrics['failed_executions'] == 0 else 'degraded',
            'agent_status': self.agent_status.copy(),
            'performance_metrics': self.performance_metrics.copy(),
            'last_execution': self.execution_history[-1] if self.execution_history else None
        }
    
    def get_agent_reports(self) -> dict:
        """Get detailed reports from all agents"""
        reports = {}
        for agent in self.agents:
            try:
                reports[agent.name] = agent.report()
            except Exception as e:
                reports[agent.name] = {'error': str(e), 'status': 'failed'}
        
        return reports
    
    def reset_metrics(self):
        """Reset all performance metrics"""
        self.performance_metrics = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'average_execution_time': 0.0
        }
        self.execution_history.clear()
        
        # Reset agent metrics
        for agent in self.agents:
            if hasattr(agent, 'reset_metrics'):
                agent.reset_metrics()
        
        self.logger.info("Orchestrator metrics reset")
