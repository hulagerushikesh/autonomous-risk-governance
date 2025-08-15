from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
import time
import traceback
from datetime import datetime

from agents.bias_audit import BiasAuditingAgent
from agents.compliance import ComplianceAgent
from agents.decision_support import DecisionSupportAgent
from agents.explainability import ExplainabilityAgent
from orchestration.orchestrator import AgentOrchestrator, OrchestrationException
from utils.logger import RiskGovernanceLogger

# Enhanced Pydantic models with validation
class EvaluationRequest(BaseModel):
    """Enhanced request model with comprehensive validation"""
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Risk score between 0 and 1")
    bias_score: float = Field(..., ge=0.0, le=1.0, description="Bias score between 0 and 1")
    risk_level: int = Field(..., ge=0, le=2, description="Risk level: 0 (low), 1 (medium), 2 (high)")
    features: List[str] = Field(..., min_items=1, description="List of features used in assessment")
    
    # Optional metadata
    customer_id: Optional[str] = Field(None, description="Customer identifier")
    request_id: Optional[str] = Field(None, description="Request identifier")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")
    
    @validator('features')
    def validate_features(cls, v):
        if not v or len(v) == 0:
            raise ValueError('At least one feature is required')
        # Remove duplicates and empty strings
        cleaned_features = [f.strip() for f in v if f.strip()]
        if not cleaned_features:
            raise ValueError('Features cannot be empty strings')
        return cleaned_features
    
    @validator('context')
    def validate_context(cls, v):
        if v is None:
            return {}
        return v

class EvaluationResponse(BaseModel):
    """Enhanced response model with comprehensive results"""
    success: bool
    execution_time: float
    timestamp: str
    request_id: Optional[str]
    agent_results: Dict[str, Any]
    orchestration_summary: Dict[str, Any]
    execution_metadata: Dict[str, Any]
    errors: Optional[List[str]] = None

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: str
    orchestrator_health: Dict[str, Any]
    agent_health: Dict[str, Any]
    performance_metrics: Dict[str, Any]

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: str
    timestamp: str
    request_id: Optional[str]

# Initialize FastAPI app with enhanced configuration
app = FastAPI(
    title="Autonomous Risk Governance API",
    description="Advanced multi-agent system for banking risk management",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize logger
logger = RiskGovernanceLogger().get_logger()

# Create enhanced orchestrator with error handling
try:
    orchestrator = AgentOrchestrator([
        ComplianceAgent("Compliance"),
        BiasAuditingAgent("BiasAudit"),
        DecisionSupportAgent("DecisionSupport"),
        ExplainabilityAgent("Explainability")
    ])
    logger.info("Agent orchestrator initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize orchestrator: {str(e)}")
    raise

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with detailed logging"""
    logger.error(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=f"HTTP {exc.status_code}",
            detail=exc.detail,
            timestamp=datetime.now().isoformat(),
            request_id=getattr(request.state, 'request_id', None)
        ).dict()
    )

@app.exception_handler(OrchestrationException)
async def orchestration_exception_handler(request, exc):
    """Handle orchestration-specific exceptions"""
    logger.error(f"Orchestration exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Orchestration Error",
            detail=str(exc),
            timestamp=datetime.now().isoformat(),
            request_id=getattr(request.state, 'request_id', None)
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unexpected exception: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal Server Error",
            detail="An unexpected error occurred",
            timestamp=datetime.now().isoformat(),
            request_id=getattr(request.state, 'request_id', None)
        ).dict()
    )

# Middleware for request tracking
@app.middleware("http")
async def request_tracking_middleware(request, call_next):
    """Add request tracking and timing"""
    start_time = time.time()
    request_id = f"req_{int(start_time * 1000)}"
    request.state.request_id = request_id
    
    logger.info(f"Request {request_id} started: {request.method} {request.url}")
    
    response = await call_next(request)
    
    execution_time = time.time() - start_time
    logger.info(f"Request {request_id} completed in {execution_time:.3f}s")
    
    # Add request ID to response headers
    response.headers["X-Request-ID"] = request_id
    
    return response

# Enhanced endpoints
@app.get("/", response_model=Dict[str, Any])
async def read_root():
    """Enhanced root endpoint with system information"""
    return {
        "message": "Welcome to Autonomous Risk Governance API v2.0",
        "description": "Advanced multi-agent system for banking risk management",
        "version": "2.0.0",
        "features": [
            "Multi-agent risk assessment",
            "Bias detection and fairness auditing",
            "Regulatory compliance checking",
            "Explainable AI decisions",
            "Real-time orchestration"
        ],
        "endpoints": {
            "evaluate": "/evaluate - Risk assessment evaluation",
            "health": "/health - System health check",
            "agents": "/agents - Agent status and reports",
            "metrics": "/metrics - Performance metrics",
            "docs": "/docs - API documentation"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate(request: EvaluationRequest):
    """Enhanced evaluation endpoint with comprehensive error handling"""
    start_time = time.time()
    request_id = request.request_id or f"eval_{int(start_time * 1000)}"
    
    logger.info(f"Starting evaluation {request_id}")
    
    try:
        # Convert request to dict for orchestrator
        input_data = request.dict()
        
        # Add timing and metadata
        input_data['request_metadata'] = {
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'api_version': '2.0.0'
        }
        
        # Run orchestrator
        logger.info(f"Running orchestrator for request {request_id}")
        results = orchestrator.run(
            input_data, 
            parallel=False,  # Can be made configurable
            continue_on_error=True
        )
        
        execution_time = time.time() - start_time
        
        # Log performance metrics
        logger.log_api_request("/evaluate", input_data, execution_time)
        
        # Create response
        response = EvaluationResponse(
            success=True,
            execution_time=execution_time,
            timestamp=datetime.now().isoformat(),
            request_id=request_id,
            agent_results=results['agent_results'],
            orchestration_summary=results['orchestration_summary'],
            execution_metadata=results['execution_metadata']
        )
        
        logger.info(f"Evaluation {request_id} completed successfully")
        return response
        
    except OrchestrationException as e:
        logger.error(f"Orchestration failed for request {request_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Orchestration failed: {str(e)}"
        )
    
    except Exception as e:
        logger.error(f"Unexpected error in evaluation {request_id}: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during evaluation"
        )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check endpoint"""
    try:
        # Get orchestrator health
        orchestrator_health = orchestrator.get_health_status()
        
        # Get agent reports
        agent_reports = orchestrator.get_agent_reports()
        
        # Determine overall health
        overall_status = "healthy"
        if orchestrator_health['orchestrator_status'] != 'healthy':
            overall_status = "degraded"
        
        for agent_name, status in orchestrator_health['agent_status'].items():
            if status != 'healthy':
                overall_status = "degraded"
                break
        
        return HealthResponse(
            status=overall_status,
            timestamp=datetime.now().isoformat(),
            orchestrator_health=orchestrator_health,
            agent_health=agent_reports,
            performance_metrics=orchestrator_health['performance_metrics']
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Health check failed"
        )

@app.get("/agents", response_model=Dict[str, Any])
async def get_agent_status():
    """Get detailed agent status and reports"""
    try:
        agent_reports = orchestrator.get_agent_reports()
        orchestrator_status = orchestrator.get_health_status()
        
        return {
            "agent_reports": agent_reports,
            "agent_status": orchestrator_status['agent_status'],
            "total_agents": len(orchestrator.agents),
            "healthy_agents": sum(1 for status in orchestrator_status['agent_status'].values() 
                                if status == 'healthy'),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get agent status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve agent status"
        )

@app.get("/metrics", response_model=Dict[str, Any])
async def get_metrics():
    """Get system performance metrics"""
    try:
        health_status = orchestrator.get_health_status()
        
        return {
            "performance_metrics": health_status['performance_metrics'],
            "orchestrator_status": health_status['orchestrator_status'],
            "agent_metrics": {
                agent.name: {
                    "execution_count": agent.execution_count,
                    "error_count": agent.error_count,
                    "error_rate": agent.error_count / max(agent.execution_count, 1),
                    "last_execution": agent.last_execution_time.isoformat() if agent.last_execution_time else None
                }
                for agent in orchestrator.agents
            },
            "system_uptime": "N/A",  # Would be calculated from startup time
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get metrics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve metrics"
        )

@app.post("/reset-metrics")
async def reset_metrics():
    """Reset performance metrics"""
    try:
        orchestrator.reset_metrics()
        logger.info("Metrics reset successfully")
        
        return {
            "message": "Metrics reset successfully",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to reset metrics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to reset metrics"
        )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Autonomous Risk Governance API v2.0 starting up")
    logger.info(f"Initialized with {len(orchestrator.agents)} agents")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Autonomous Risk Governance API v2.0 shutting down")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
