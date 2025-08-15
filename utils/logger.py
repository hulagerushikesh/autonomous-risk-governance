import logging
import os
from datetime import datetime
from typing import Optional

class RiskGovernanceLogger:
    """Enhanced logging system for the Risk Governance application"""
    
    _instance: Optional['RiskGovernanceLogger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls) -> 'RiskGovernanceLogger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """Setup centralized logging configuration"""
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Create logger
        self._logger = logging.getLogger('risk_governance')
        self._logger.setLevel(logging.INFO)
        
        # Prevent duplicate handlers
        if not self._logger.handlers:
            # File handler with rotation
            file_handler = logging.FileHandler(
                f'logs/risk_governance_{datetime.now().strftime("%Y%m%d")}.log'
            )
            file_handler.setLevel(logging.INFO)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.WARNING)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # Add handlers
            self._logger.addHandler(file_handler)
            self._logger.addHandler(console_handler)
    
    def get_logger(self) -> logging.Logger:
        """Get the configured logger instance"""
        return self._logger
    
    def log_agent_evaluation(self, agent_name: str, input_data: dict, result: dict):
        """Log agent evaluation with structured data"""
        self._logger.info(f"Agent '{agent_name}' evaluation completed", extra={
            'agent_name': agent_name,
            'input_data': input_data,
            'result': result
        })
    
    def log_api_request(self, endpoint: str, request_data: dict, response_time: float):
        """Log API requests with performance metrics"""
        self._logger.info(f"API request to '{endpoint}' completed in {response_time:.3f}s", extra={
            'endpoint': endpoint,
            'request_data': request_data,
            'response_time': response_time
        })

# Convenience function for backward compatibility
def setup_logger() -> logging.Logger:
    """Setup and return logger instance"""
    logger_instance = RiskGovernanceLogger()
    return logger_instance.get_logger()