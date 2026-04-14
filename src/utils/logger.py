"""
Comprehensive Logging System for MoodSense AI
"""

import logging
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
import traceback
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger


class MoodSenseLogger:
    """
    Centralized logging system with structured logging,
    error tracking, and performance monitoring
    """
    
    def __init__(self, name: str = "MoodSenseAI", log_dir: str = "logs"):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create different loggers for different purposes
        self.mood_logger = self._setup_logger("mood_analysis", "mood_analysis.log")
        self.rag_logger = self._setup_logger("rag_system", "rag_system.log")
        self.agent_logger = self._setup_logger("agent", "agent_actions.log")
        self.error_logger = self._setup_logger("errors", "errors.log", level=logging.ERROR)
        self.metrics_logger = self._setup_logger("metrics", "metrics.log")
        self.audit_logger = self._setup_logger("audit", "audit.log")
        
    def _setup_logger(self, name: str, filename: str, level=logging.INFO) -> logging.Logger:
        """Setup individual logger with JSON formatting and rotation"""
        logger = logging.getLogger(f"{self.name}.{name}")
        logger.setLevel(level)
        
        # Clear existing handlers
        logger.handlers = []
        
        # File handler with rotation (10MB max, keep 5 backups)
        file_handler = RotatingFileHandler(
            self.log_dir / filename,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        
        # JSON formatter for structured logging
        json_formatter = jsonlogger.JsonFormatter(
            fmt='%(timestamp)s %(level)s %(name)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(json_formatter)
        logger.addHandler(file_handler)
        
        # Console handler for errors
        if level == logging.ERROR:
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
        return logger
        
    def log_mood_analysis(
        self,
        user_id: str,
        input_text: str,
        result: Any,
        response_time: float
    ):
        """Log mood analysis with full context"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "input_text": input_text[:200],  # Truncate for privacy
            "primary_mood": result.primary_mood,
            "confidence": result.confidence,
            "intensity": result.intensity,
            "triggers": result.triggers,
            "crisis_detected": result.requires_crisis_support,
            "response_time_ms": response_time * 1000,
            "emotion_scores": {k: round(v, 3) for k, v in result.emotion_scores.items() if v != 0}
        }
        
        self.mood_logger.info("mood_analysis", extra=log_entry)
        
        # Log to audit if crisis detected
        if result.requires_crisis_support:
            self.audit_logger.warning("crisis_detected", extra={
                **log_entry,
                "alert": "CRISIS_PROTOCOL_ACTIVATED"
            })
            
    def log_rag_retrieval(
        self,
        user_id: str,
        query: str,
        mood: Optional[str],
        num_results: int,
        relevance_scores: list,
        response_time: float
    ):
        """Log RAG retrieval operations"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "query": query[:100],
            "mood_context": mood,
            "num_results_requested": num_results,
            "num_results_returned": len(relevance_scores),
            "avg_relevance_score": sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0,
            "top_relevance_score": max(relevance_scores) if relevance_scores else 0,
            "response_time_ms": response_time * 1000
        }
        
        self.rag_logger.info("retrieval", extra=log_entry)
        
    def log_agent_action(
        self,
        user_id: str,
        action_type: str,
        parameters: Dict[str, Any],
        success: bool,
        result: Any = None,
        error: str = None
    ):
        """Log agent actions and interventions"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "action_type": action_type,
            "parameters": parameters,
            "success": success,
            "result_summary": str(result)[:200] if result else None,
            "error": error
        }
        
        if success:
            self.agent_logger.info("action_executed", extra=log_entry)
        else:
            self.agent_logger.error("action_failed", extra=log_entry)
            self.log_error(f"Agent action failed: {action_type}", error, context=log_entry)
            
    def log_error(
        self,
        message: str,
        error: Exception = None,
        context: Dict[str, Any] = None
    ):
        """Log errors with full stack trace"""
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "error_type": type(error).__name__ if error else "Unknown",
            "error_message": str(error) if error else None,
            "stack_trace": traceback.format_exc() if error else None,
            "context": context
        }
        
        self.error_logger.error("error_occurred", extra=error_entry)
        
    def log_performance_metrics(
        self,
        component: str,
        operation: str,
        duration: float,
        success: bool,
        metadata: Dict[str, Any] = None
    ):
        """Log performance metrics for monitoring"""
        metrics_entry = {
            "timestamp": datetime.now().isoformat(),
            "component": component,
            "operation": operation,
            "duration_ms": duration * 1000,
            "success": success,
            "metadata": metadata or {}
        }
        
        self.metrics_logger.info("performance", extra=metrics_entry)
        
    def log_user_feedback(
        self,
        user_id: str,
        resource_id: str,
        helpful: bool,
        rating: Optional[float] = None,
        comment: Optional[str] = None
    ):
        """Log user feedback for continuous improvement"""
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "resource_id": resource_id,
            "helpful": helpful,
            "rating": rating,
            "comment": comment[:500] if comment else None
        }
        
        self.audit_logger.info("user_feedback", extra=feedback_entry)
        
    def get_metrics_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get summary of metrics for the last N hours"""
        # This would typically query the log files or a metrics database
        # For now, return a sample structure
        return {
            "period_hours": hours,
            "total_analyses": 0,
            "avg_response_time_ms": 0,
            "crisis_detections": 0,
            "error_rate": 0,
            "user_satisfaction": 0
        }
        

class ErrorHandler:
    """Global error handler with recovery strategies"""
    
    def __init__(self, logger: MoodSenseLogger):
        self.logger = logger
        
    def handle_with_fallback(
        self,
        primary_func,
        fallback_func,
        context: Dict[str, Any]
    ):
        """Execute primary function with fallback on error"""
        try:
            return primary_func()
        except Exception as e:
            self.logger.log_error(
                f"Primary function failed: {primary_func.__name__}",
                e,
                context
            )
            
            try:
                return fallback_func()
            except Exception as fallback_error:
                self.logger.log_error(
                    f"Fallback also failed: {fallback_func.__name__}",
                    fallback_error,
                    context
                )
                raise
                
    def safe_execute(self, func, default_return=None, log_errors=True):
        """Safely execute function with error logging"""
        try:
            return func()
        except Exception as e:
            if log_errors:
                self.logger.log_error(
                    f"Safe execution failed: {func.__name__}",
                    e
                )
            return default_return


# Global logger instance
logger = MoodSenseLogger()
error_handler = ErrorHandler(logger)


# Convenience functions for direct logging
def log_mood_analysis(user_id: str, input_text: str, result: Any, response_time: float):
    """Convenience function for mood analysis logging"""
    logger.log_mood_analysis(user_id, input_text, result, response_time)
    

def log_error(message: str, error: Exception = None, context: Dict[str, Any] = None):
    """Convenience function for error logging"""
    logger.log_error(message, error, context)
    

def log_metrics(component: str, operation: str, duration: float, success: bool):
    """Convenience function for metrics logging"""
    logger.log_performance_metrics(component, operation, duration, success)