from typing import List, Dict, Any
import datetime

class SharedBuffer:
    """A shared communication channel for all agents."""
    
    def __init__(self):
        self.messages: List[Dict[str, Any]] = []
        
    def post_message(self, sender: str, content: str, msg_type: str = "report"):
        """Posts a message to the buffer."""
        timestamp = datetime.datetime.now().isoformat()
        msg = {
            "timestamp": timestamp,
            "sender": sender,
            "content": content,
            "type": msg_type
        }
        self.messages.append(msg)
        
    def get_recent_messages(self, count: int = 10) -> List[Dict[str, Any]]:
        """Gets the N most recent messages."""
        return self.messages[-count:]
        
    def get_all_messages(self) -> List[Dict[str, Any]]:
        return self.messages
        
    def clear(self):
        self.messages = []
