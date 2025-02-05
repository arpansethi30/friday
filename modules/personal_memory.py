import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from security.encryption_utils import EncryptionManager  # Updated import

class PersonalMemory:
    def __init__(self, config):
        self.config = config
        self.data_dir = Path(config.PERSONAL_DATA_DIR)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "personal_brain.db"
        self.encryption = EncryptionManager()  # Added encryption manager
        self._verify_security()  # Added security verification
        self.setup_database()
        
    def _verify_security(self):
        """Verify data directory permissions"""
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True)
            os.chmod(str(self.data_dir), 0o700)  # Owner only access
            
        if not self.encryption.secure_file_access(self.db_path):
            os.chmod(str(self.db_path), 0o600)
        
    def setup_database(self):
        """Initialize SQLite database for personal data"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        # Create tables
        c.executescript('''
            CREATE TABLE IF NOT EXISTS personal_info (
                category TEXT,
                key TEXT,
                value TEXT,
                last_updated TIMESTAMP,
                PRIMARY KEY (category, key)
            );
            
            CREATE TABLE IF NOT EXISTS preferences (
                category TEXT,
                preference TEXT,
                value TEXT,
                last_used TIMESTAMP,
                frequency INTEGER,
                PRIMARY KEY (category, preference)
            );
            
            CREATE TABLE IF NOT EXISTS learning (
                topic TEXT,
                data TEXT,
                source TEXT,
                timestamp TIMESTAMP,
                confidence FLOAT
            );
        ''')
        conn.commit()
        conn.close()
        
    def add_personal_info(self, category: str, key: str, value: str):
        """Safely store encrypted personal information"""
        encrypted_value = self.encryption.encrypt(value)  # Updated encryption
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO personal_info (category, key, value, last_updated)
            VALUES (?, ?, ?, ?)
        ''', (category, key, encrypted_value, datetime.now()))
        conn.commit()
        conn.close()
        
    def learn_from_interaction(self, data: Dict[str, Any]):
        """Learn from user interactions"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        # Store learning data
        c.execute('''
            INSERT INTO learning (topic, data, source, timestamp, confidence)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('topic', 'general'),
            json.dumps(data.get('data', {})),
            data.get('source', 'interaction'),
            datetime.now(),
            data.get('confidence', 0.5)
        ))
        
        # Update preferences if present
        if 'preferences' in data:
            for category, prefs in data['preferences'].items():
                for pref, value in prefs.items():
                    self._update_preference(c, category, pref, value)
                    
        conn.commit()
        conn.close()
        
    def _update_preference(self, cursor, category: str, preference: str, value: str):
        """Update user preference with increased frequency"""
        cursor.execute('''
            INSERT INTO preferences (category, preference, value, last_used, frequency)
            VALUES (?, ?, ?, ?, 1)
            ON CONFLICT(category, preference) DO UPDATE SET
                frequency = frequency + 1,
                last_used = ?,
                value = ?
        ''', (category, preference, value, datetime.now(), datetime.now(), value))
        
    def get_personal_context(self) -> Dict[str, Any]:
        """Retrieve relevant personal context for AI interactions"""
        context = super().get_personal_context()  # Updated to call super method
        
        # Add additional security check
        if not self._is_local_request():
            return {"error": "Access denied: Personal data only available locally"}
            
        return context
        
    def _is_local_request(self) -> bool:
        """Verify request is coming from local instance"""
        import socket
        return socket.gethostname() == 'localhost'
