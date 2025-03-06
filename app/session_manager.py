from typing import Dict
from ragflow_sdk import RAGFlow, Agent

class SessionManager:
    _instance = None
    _sessions: Dict[str, Agent] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance

    def get_session(self, user_id: str, agent_id: str, ragflow: RAGFlow) -> Agent:
        """
        若尚未為指定 user_id 建立 Session，則建立新的 Session。
        否則直接回傳先前儲存的 Session。
        """
        if user_id not in self._sessions:
            self._sessions[user_id] = Agent.create_session(agent_id, ragflow)
        return self._sessions[user_id]
