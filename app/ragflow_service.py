from typing import Generator
from ragflow_sdk import RAGFlow, Agent
from session_manager import SessionManager

class RAGFlowService:
    def __init__(self, api_key: str, base_url: str, agent_id: str) -> None:
        self.ragflow = RAGFlow(api_key=api_key, base_url=base_url)
        self.agent_id = agent_id
        self.session_manager = SessionManager()  # 取得 Singleton

    def ask_question(self, user_id: str, question: str) -> str:
        """
        取得 user_id 對應的 Session，並向 RAGFlow 進行問答。
        回傳完整回應字串。
        """
        session: Agent = self.session_manager.get_session(
            user_id=user_id,
            agent_id=self.agent_id,
            ragflow=self.ragflow
        )
        full_response = ""
        cont = ""
        
        count = 0
        for ans in session.ask(question, stream=True):
            count += 1
            # 只新增最新回傳的差量
            full_response += ans.content[len(cont):]
            cont = ans.content
        
        return full_response
        



