from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import traceback
from utils.logger import RiskGovernanceLogger

class AgentException(Exception):
    """Custom exception for agent-related errors"""
    def __init__(self, agent_name: str, message: str, original_error: Optional[Exception] = None):
        self.agent_name = agent_name
        self.original_error = original_error
        super().__init__(f"Agent '{agent_name}': {message}")

class BaseAgent(ABC):
    """Enhanced base agent with error handling, logging, and validation"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = RiskGovernanceLogger().get_logger()
        self.execution_count = 0
        self.error_count = 0
        self.last_execution_time: Optional[datetime] = None
    
    def validate_input(self, input_data: dict) -> bool:
        """Validate input data format and required fields"""
        if not isinstance(input_data, dict):
            raise AgentException(self.name, "Input data must be a dictionary")
        
        # Check for required fields based on agent type
        required_fields = self.get_required_fields()
        missing_fields = [field for field in required_fields if field not in input_data]
        
        if missing_fields:
            raise AgentException(
                self.name, 
                f"Missing required fields: {missing_fields}"
            )
        
        return True
    
    @abstractmethod
    def get_required_fields(self) -> list:
        """Return list of required input fields for this agent"""
        pass
    
    @abstractmethod
    def _evaluate_logic(self, input_data: dict) -> dict:
        """Core evaluation logic - to be implemented by subclasses"""
        pass
    
    def evaluate(self, input_data: dict) -> dict:
        """Enhanced evaluate method with error handling and logging"""
        start_time = datetime.now()
        
        try:
            # Validate input
            self.validate_input(input_data)
            
            # Log start of evaluation
            self.logger.info(f"Starting evaluation for agent '{self.name}'")
            
            # Perform actual evaluation
            result = self._evaluate_logic(input_data)
            
            # Add metadata to result
            result['agent_metadata'] = {
                'name': self.name,
                'execution_time': (datetime.now() - start_time).total_seconds(),
                'timestamp': datetime.now().isoformat(),
                'execution_count': self.execution_count + 1
            }
            
            # Update counters
            self.execution_count += 1
            self.last_execution_time = datetime.now()
            
            # Log successful completion
            self.logger.info(f"Agent '{self.name}' evaluation completed successfully", extra={
                'agent_name': self.name,
                'input_data': input_data,
                'result': result
            })
            
            return result
            
        except AgentException:
            self.error_count += 1
            self.logger.error(f"Agent '{self.name}' validation error: {traceback.format_exc()}")
            raise
            
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"Agent '{self.name}' unexpected error: {traceback.format_exc()}")
            raise AgentException(self.name, f"Unexpected error during evaluation: {str(e)}", e)
    
    def report(self) -> dict:
        """Enhanced reporting with performance metrics"""
        error_rate = self.error_count / max(self.execution_count, 1)
        return {
            "agent": self.name,
            "status": "active",
            "execution_count": self.execution_count,
            "error_count": self.error_count,
            "error_rate": error_rate,
            "last_execution": self.last_execution_time.isoformat() if self.last_execution_time else None,
            "health_status": "healthy" if error_rate < 0.1 else "degraded"
        }
    
    def reset_metrics(self):
        """Reset performance metrics"""
        self.execution_count = 0
        self.error_count = 0
        self.last_execution_time = None
