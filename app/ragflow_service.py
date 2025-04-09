from typing import Generator
from ragflow_sdk import RAGFlow, Agent
from session_manager import SessionManager

import time
import re

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
        
        print('question:')
        print(question)

        max_retries = 5
        retry_count = 0

        while retry_count < max_retries:
            count = 0
            full_response = ""
            cont = ""
            
            try:
                for ans in session.ask(question, stream=True):
                    count += 1
                    # 只新增最新回傳的差量
                    full_response += ans.content[len(cont):]
                    cont = ans.content
            except Exception as e:
                retry_count += 1
                time.sleep(1)
                continue

            if not isinstance(full_response, str):
                print("\u7cfb\u7d71\u932f\u8aa4\uff0c\u8acb\u806f\u7d61\u7dad\u8b77\u4eba\u54e1 (Response Format Error)")
                break

            full_response = re.sub(r'##\d+\$\$', '', full_response)
            print('print:')
            print(full_response)

            if len(full_response) == 0:
                retry_count += 1
                time.sleep(1)
            else:
                break
        else:
            print("\u7cfb\u7d71\u932f\u8aa4\uff0c\u8acb\u806f\u7d61\u7dad\u8b77\u4eba\u54e1 (Session Error)")

        return full_response
        



