"""
Configuration module for Operation Miniature Garden.
Centralized configuration management with validation.
"""
import os
from dataclasses import dataclass
from typing import Dict, Any, Optional
import logging
from dotenv import load_dotenv

load_dotenv()

@dataclass
class DatabaseConfig:
    """Firebase database configuration"""
    project_id: str = "miniature-garden-prod"
    collection_name: str = "garden_metrics"
    max_retries: int = 3
    timeout_seconds: int = 10

@dataclass
class AIConfig:
    """AI model configuration with fallback strategies"""
    model_name: str = "deepseek-chat"
    max_retries: int = 3
    timeout_seconds: int = 30
    temperature: float = 0.7
    max_tokens: int = 500
    fallback_enabled: bool = True
    fallback_model: str = "rule_based"

@dataclass
class SensorConfig:
    """Sensor simulation and real hardware configuration"""
    simulation_mode: bool = True
    update_interval_seconds: int = 60
    mock_data_range: Dict[str, tuple] = None
    
    def __post_init__(self):
        if self.mock_data_range is None:
            self.mock_data_range = {
                "temperature": (18.0, 28.0),
                "humidity": (40.0, 80.0),
                "soil_moisture": (20.0, 95.0),
                "light_intensity": (100.0, 1000.0)
            }

@dataclass
class LoggingConfig:
    """Logging configuration for observability"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = "logs/garden_system.log"
    max_bytes: int = 10_485_760  # 10MB
    backup_count: int = 5

class ConfigManager:
    """Central configuration manager with validation"""
    
    def __init__(self):
        self.database = DatabaseConfig()
        self.ai = AIConfig()
        self.sensor = SensorConfig()
        self.logging = LoggingConfig()
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate all configuration parameters"""
        if self.ai.max_retries < 1:
            raise ValueError("AI max_retries must be at least 1")
        if self.sensor.update_interval_seconds < 10:
            raise ValueError("Update interval too short (minimum 10 seconds)")
        if not os.path.exists("logs"):
            os.makedirs("logs")
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary for logging"""
        return {
            "database": self.database.__dict__,
            "ai": self.ai.__dict__,
            "sensor": self.sensor.__dict__,
            "logging": self.logging.__dict__
        }

# Global configuration instance
config = ConfigManager()