
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import logging

class InteractionLogger:
    def __init__(self, config):
        self.config = config
        self.logs_dir = Path(config.LOGS_DIR)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup different log files
        self.setup_loggers()
        
    def setup_loggers(self):
        """Setup different loggers for various types of interactions"""
        # Commands logger
        self.cmd_logger = logging.getLogger('commands')
        cmd_handler = logging.FileHandler(self.logs_dir / 'commands.log')
        cmd_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(message)s'
        ))
        self.cmd_logger.addHandler(cmd_handler)
        self.cmd_logger.setLevel(logging.INFO)
        
        # Conversations logger
        self.conv_logger = logging.getLogger('conversations')
        conv_handler = logging.FileHandler(self.logs_dir / 'conversations.log')
        conv_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(message)s'
        ))
        self.conv_logger.addHandler(conv_handler)
        self.conv_logger.setLevel(logging.INFO)
        
        # Features usage logger
        self.feature_logger = logging.getLogger('features')
        feature_handler = logging.FileHandler(self.logs_dir / 'features_usage.log')
        feature_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(message)s'
        ))
        self.feature_logger.addHandler(feature_handler)
        self.feature_logger.setLevel(logging.INFO)
        
    def log_command(self, command: str, success: bool, response: str):
        """Log command execution"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'success': success,
            'response': response
        }
        self.cmd_logger.info(json.dumps(log_entry))
        
    def log_conversation(self, user_input: str, assistant_response: str, 
                        context: Optional[Dict] = None):
        """Log conversation exchange"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'assistant_response': assistant_response,
            'context': context or {}
        }
        self.conv_logger.info(json.dumps(log_entry))
        
    def log_feature_usage(self, feature: str, details: Dict[str, Any]):
        """Log feature usage"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'feature': feature,
            'details': details
        }
        self.feature_logger.info(json.dumps(log_entry))
        
    def get_usage_stats(self, days: int = 7) -> Dict[str, Any]:
        """Get usage statistics for the specified period"""
        stats = {
            'commands': self._analyze_log_file('commands.log', days),
            'conversations': self._analyze_log_file('conversations.log', days),
            'features': self._analyze_log_file('features_usage.log', days)
        }
        return stats
        
    def _analyze_log_file(self, filename: str, days: int) -> Dict[str, Any]:
        """Analyze log file for statistics"""
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        log_file = self.logs_dir / filename
        
        if not log_file.exists():
            return {}
            
        entries = []
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    timestamp_str = line.split(' - ')[0]
                    timestamp = datetime.fromisoformat(timestamp_str).timestamp()
                    if timestamp >= cutoff_date:
                        entries.append(json.loads(line.split(' - ')[1]))
                except:
                    continue
                    
        return self._calculate_stats(entries)
        
    def _calculate_stats(self, entries: list) -> Dict[str, Any]:
        """Calculate statistics from log entries"""
        # Implementation for calculating various statistics
        return {
            'total_entries': len(entries),
            'success_rate': self._calculate_success_rate(entries),
            'common_patterns': self._find_common_patterns(entries)
        }