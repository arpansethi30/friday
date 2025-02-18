import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json
import logging
from typing import Dict, List, Any, Optional
import sqlite3
from datetime import datetime
import subprocess

class CommunicationManager:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('FRIDAY.Communication')
        self.contacts_db = os.path.expanduser("~/Library/Application Support/AddressBook/AddressBook-v22.abcddb")
        self._setup_email_config()

    def _setup_email_config(self):
        """Setup email configuration"""
        self.email_config = {
            'gmail': {
                'smtp': 'smtp.gmail.com',
                'imap': 'imap.gmail.com',
                'smtp_port': 587,
                'imap_port': 993
            },
            'outlook': {
                'smtp': 'smtp.office365.com',
                'imap': 'outlook.office365.com',
                'smtp_port': 587,
                'imap_port': 993
            }
        }

    def compose_email(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Compose email based on context"""
        try:
            # Get recipient details
            recipient = self._get_contact_details(context['recipient'])
            if not recipient:
                raise ValueError(f"Contact not found: {context['recipient']}")

            # Generate email content
            subject = self._generate_subject(context)
            body = self._generate_body(context)
            
            email_data = {
                'to': recipient['email'],
                'subject': subject,
                'body': body,
                'recipient_name': recipient['name']
            }

            # Save draft
            self._save_draft(email_data)
            return email_data

        except Exception as e:
            self.logger.error(f"Error composing email: {e}")
            return {'error': str(e)}

    def send_email(self, email_data: Dict[str, Any]) -> bool:
        """Send email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config.EMAIL_ADDRESS
            msg['To'] = email_data['to']
            msg['Subject'] = email_data['subject']
            msg.attach(MIMEText(email_data['body'], 'plain'))

            with smtplib.SMTP(self.email_config['gmail']['smtp'], 
                            self.email_config['gmail']['smtp_port']) as server:
                server.starttls()
                server.login(self.config.EMAIL_ADDRESS, self.config.EMAIL_PASSWORD)
                server.send_message(msg)
            
            return True
        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            return False

    def compose_mail_native(self, email_data: Dict[str, Any]) -> bool:
        """Compose email using Mac Mail app"""
        try:
            script = f'''
                tell application "Mail"
                    activate
                    set newMessage to make new outgoing message with properties {{visible:true}}
                    tell newMessage
                        set subject to "{email_data['subject']}"
                        set content to "{email_data['body']}"
                        make new to recipient at end of to recipients with properties {{address:"{email_data['to']}"}}
                    end tell
                end tell
            '''
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Error composing email in Mail app: {e}")
            return False

    def send_mail_native(self) -> bool:
        """Send email using Mac Mail app"""
        try:
            script = '''
                tell application "Mail"
                    send the first message of outgoing messages
                end tell
            '''
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            return False

    def check_unread_emails(self) -> Dict[str, Any]:
        """Check unread emails in Mail app"""
        try:
            script = '''
                tell application "Mail"
                    set unreadCount to 0
                    set urgentMessages to {}
                    
                    repeat with theAccount in accounts
                        set unreadCount to unreadCount + (unread count of inbox of theAccount)
                        set msgs to (messages of inbox of theAccount whose read status is false)
                        repeat with msg in msgs
                            if subject of msg contains "Urgent" or subject of msg contains "Important" then
                                copy {subject:subject of msg, sender:sender of msg} to end of urgentMessages
                            end if
                        end repeat
                    end repeat
                    
                    return {unreadCount, urgentMessages}
                end tell
            '''
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            if result.returncode == 0:
                return {
                    "unread_count": int(result.stdout.split(',')[0]),
                    "urgent_messages": json.loads(result.stdout.split(',')[1])
                }
            return {"error": "Failed to check emails"}
        except Exception as e:
            self.logger.error(f"Error checking emails: {e}")
            return {"error": str(e)}

    def _get_contact_details(self, name: str) -> Optional[Dict[str, str]]:
        """Get contact details from Address Book"""
        try:
            # Connect to macOS Contacts database
            conn = sqlite3.connect(self.contacts_db)
            cursor = conn.cursor()
            
            # Search for contact
            cursor.execute("""
                SELECT ZFIRSTNAME, ZLASTNAME, ZEMAILADDRESS 
                FROM ZABCDRECORD 
                WHERE ZFIRSTNAME LIKE ? OR ZLASTNAME LIKE ?
            """, (f"%{name}%", f"%{name}%"))
            
            result = cursor.fetchone()
            if result:
                return {
                    'name': f"{result[0]} {result[1]}",
                    'email': result[2]
                }
            return None
        except Exception as e:
            self.logger.error(f"Error accessing contacts: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def _generate_subject(self, context: Dict[str, Any]) -> str:
        """Generate appropriate email subject"""
        if 'absent' in context['intent'].lower():
            return "Absence Notification"
        elif 'meeting' in context['intent'].lower():
            return f"Meeting {context.get('action', 'Update')}"
        return context.get('subject', 'No Subject')

    def _generate_body(self, context: Dict[str, Any]) -> str:
        """Generate email body based on context"""
        templates = {
            'absence': """
Dear {recipient},

I hope this email finds you well. I wanted to inform you that I will not be able to come to work today due to {reason}.

{additional_info}

Best regards,
{sender}
""",
            'meeting': """
Hi {recipient},

{action} our meeting {timing}.

{details}

Best regards,
{sender}
"""
        }

        template = templates.get(context['intent'].lower(), "")
        return template.format(
            recipient=context['recipient_name'],
            reason=context.get('reason', 'personal reasons'),
            additional_info=context.get('additional_info', ''),
            sender=self.config.USER_NAME,
            action=context.get('action', ''),
            timing=context.get('timing', ''),
            details=context.get('details', '')
        )

    def _save_draft(self, email_data: Dict[str, Any]):
        """Save email draft"""
        drafts_folder = os.path.expanduser("~/Documents/EmailDrafts")
        os.makedirs(drafts_folder, exist_ok=True)
        
        draft_file = os.path.join(
            drafts_folder, 
            f"draft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(draft_file, 'w') as f:
            json.dump(email_data, f, indent=2)
