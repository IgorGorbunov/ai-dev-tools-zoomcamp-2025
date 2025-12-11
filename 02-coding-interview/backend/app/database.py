from datetime import datetime
from typing import Optional, Dict, Any, List
import uuid


class InMemoryDatabase:
    """Simple in-memory database for demo purposes"""
    
    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {}
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.participants: Dict[str, List[str]] = {}
    
    def create_user(self, username: str, email: str, hashed_password: str) -> Dict[str, Any]:
        """Create a new user"""
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "username": username,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.utcnow()
        }
        self.users[user_id] = user
        return {k: v for k, v in user.items() if k != "password"}
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        user = self.users.get(user_id)
        if user:
            return {k: v for k, v in user.items() if k != "password"}
        return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        for user in self.users.values():
            if user["email"] == email:
                return user
        return None
    
    def create_session(
        self,
        title: str,
        description: str,
        created_by: str,
        language: str,
        time_limit_minutes: int
    ) -> Dict[str, Any]:
        """Create a new coding session"""
        session_id = str(uuid.uuid4())
        session = {
            "id": session_id,
            "title": title,
            "description": description,
            "created_by": created_by,
            "language": language,
            "created_at": datetime.utcnow(),
            "time_limit_minutes": time_limit_minutes,
            "code": "",
            "status": "active"
        }
        self.sessions[session_id] = session
        self.participants[session_id] = [created_by]
        return session
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def get_sessions(self, created_by: str = None) -> List[Dict[str, Any]]:
        """Get all sessions, optionally filtered by creator"""
        if created_by:
            return [s for s in self.sessions.values() if s["created_by"] == created_by]
        return list(self.sessions.values())
    
    def get_user_sessions(self, user_id: str, limit: int = 50, offset: int = 0):
        """Get sessions for a user with pagination"""
        user_sessions = [s for s in self.sessions.values() if s["created_by"] == user_id]
        total = len(user_sessions)
        sessions = user_sessions[offset:offset + limit]
        return sessions, total
    
    def update_session(self, session_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a session"""
        session = self.sessions.get(session_id)
        if session:
            session.update(kwargs)
            return session
        return None
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            if session_id in self.participants:
                del self.participants[session_id]
            return True
        return False
    
    def add_participant(self, session_id: str, user_id: str) -> bool:
        """Add a participant to a session"""
        if session_id in self.participants:
            if user_id not in self.participants[session_id]:
                self.participants[session_id].append(user_id)
            return True
        return False
    
    def get_participants(self, session_id: str) -> List[str]:
        """Get participants of a session"""
        return self.participants.get(session_id, [])
    
    def update_session_code(self, session_id: str, code: str) -> bool:
        """Update the code in a session"""
        session = self.sessions.get(session_id)
        if session:
            session["code"] = code
            return True
        return False
    
    def get_session_code(self, session_id: str) -> Optional[str]:
        """Get the code from a session"""
        session = self.sessions.get(session_id)
        return session["code"] if session else None


# Global database instance
db = InMemoryDatabase()
