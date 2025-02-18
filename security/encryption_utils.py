
from cryptography.fernet import Fernet
import os
from pathlib import Path
import base64
from typing import Any
import json

class EncryptionManager:
    def __init__(self):
        self.key_file = Path.home() / '.friday' / '.secrets' / 'encryption_key.txt'
        self.key = self._load_or_generate_key()
        self.fernet = Fernet(self.key)
        
    def _load_or_generate_key(self) -> bytes:
        """Load existing key or generate new one"""
        try:
            if self.key_file.exists():
                return self.key_file.read_bytes()
            else:
                key = Fernet.generate_key()
                self.key_file.parent.mkdir(parents=True, exist_ok=True)
                self.key_file.write_bytes(key)
                os.chmod(str(self.key_file), 0o600)  # Read/write for owner only
                return key
        except Exception as e:
            raise Exception(f"Failed to setup encryption: {e}")
            
    def encrypt(self, data: Any) -> bytes:
        """Encrypt data"""
        json_data = json.dumps(data)
        return self.fernet.encrypt(json_data.encode())
        
    def decrypt(self, encrypted_data: bytes) -> Any:
        """Decrypt data"""
        try:
            decrypted = self.fernet.decrypt(encrypted_data)
            return json.loads(decrypted.decode())
        except Exception:
            return None
            
    def secure_file_access(self, path: Path) -> bool:
        """Check if file permissions are secure"""
        try:
            return oct(os.stat(path).st_mode)[-3:] == '600'
        except Exception:
            return False