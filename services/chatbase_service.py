## streamer.py

import requests
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

class ChatbaseHandler():
    def __init__(self):
        self.api_url: str = 'https://www.chatbase.co/api/v1/chat'
        api_key: str = os.environ.get('CHATBASE_API_KEY')
        self.chat_id: str = os.environ.get('CHATBASE_AGENT_ID')
        self.authorization_header = f'Bearer {api_key}'

    async def read_chatbot_reply(self, message):
        try:
            messages = [
                { 'content': message, 'role': 'user' }
            ]

            headers = {
                'Authorization': self.authorization_header,
                'Content-Type': 'application/json'
            }

            data = {
                'messages': messages,
                'chatbotId': self.chat_id,
                'stream': True,
                'temperature': 0,
            }
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream("POST", self.api_url, json=data, headers=headers) as response:
                    async for chunk in response.aiter_text():
                    # chunk_value = chunk.decode('utf-8')
                        yield chunk

        except requests.exceptions.RequestException as error:
            print('Error:', error)
