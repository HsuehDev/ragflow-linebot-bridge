import threading
import time
from typing import Dict
from ragflow_sdk import RAGFlow, Agent

class SessionManager:
    _instance = None
    _sessions: Dict[str, Agent] = {}
    _timers: Dict[str, threading.Timer] = {}

    SESSION_TIMEOUT = 300  # 5 分鐘

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance

    def _remove_session(self, user_id: str):
        """移除 session 並刪除計時器"""
        if user_id in self._sessions:
            del self._sessions[user_id]
        if user_id in self._timers:
            del self._timers[user_id]
        print(f"Session for {user_id} has been removed due to inactivity.")

    def _reset_timer(self, user_id: str):
        """重置計時器"""
        if user_id in self._timers:
            self._timers[user_id].cancel()

        timer = threading.Timer(self.SESSION_TIMEOUT, self._remove_session, [user_id])
        timer.start()
        self._timers[user_id] = timer

    def get_session(self, user_id: str, agent_id: str, ragflow: RAGFlow) -> Agent:
        """
        若尚未為指定 user_id 建立 Session，則建立新的 Session。
        否則直接回傳先前儲存的 Session，並重置計時器。
        """
        if user_id not in self._sessions:
            self._sessions[user_id] = Agent.create_session(agent_id, ragflow)
        self._reset_timer(user_id)  # 每次取得 session 都重置計時器
        return self._sessions[user_id]
