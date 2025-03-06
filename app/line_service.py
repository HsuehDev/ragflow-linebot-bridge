import os, time, random
from fastapi import FastAPI, Request, HTTPException

from linebot.v3.messaging import Configuration, TextMessage, ReplyMessageRequest
from linebot.v3.messaging import ApiClient, MessagingApi
from linebot.v3.messaging import ShowLoadingAnimationRequest
from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError
from ragflow_service import RAGFlowService


# Fetching environment variables for secure handling of sensitive information
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

# RAGFlow related configuration fetched from environment variables
RAGFLOW_API_KEY = os.getenv("RAGFLOW_API_KEY")
RAGFLOW_BASE_URL = os.getenv("RAGFLOW_BASE_URL")  # Providing a default value if not set
AGENT_ID = os.getenv("AGENT_ID")


# LINE configuration
line_channel_access_token = LINE_CHANNEL_ACCESS_TOKEN
line_channel_secret = LINE_CHANNEL_SECRET

WAIT_TIME = 5 # wait around 5 seconds before respond to the user

# Create configuration for messaging API
configuration = Configuration(access_token=line_channel_access_token)
with ApiClient(configuration) as api_client:
    line_bot_api = MessagingApi(api_client)

# Correct WebhookHandler initialization
handler = WebhookHandler(channel_secret=line_channel_secret)

# FastAPI app
app = FastAPI()


# @app.post("/") # use this or use next
@app.post("/callback") 
async def line_webhook(request: Request):
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return "OK"

# Message handler
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    start_time = time.time()

    line_bot_api.show_loading_animation_with_http_info(
        ShowLoadingAnimationRequest(chat_id=event.source.user_id)
    )

    user_id = event.source.user_id
    user_message = event.message.text
    
    ragflow = RAGFlowService(
        api_key=RAGFLOW_API_KEY,
        base_url=RAGFLOW_BASE_URL,
        agent_id=AGENT_ID
    )
    
    response = ragflow.ask_question(user_id, user_message)
    print(response)
    
    line_bot_api.reply_message(
        ReplyMessageRequest(
            replyToken=event.reply_token,
            messages=[TextMessage(text=response)]
        )
    )