import uuid
import datetime
import openai
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

class UserSession:
    def __init__(self, username):
        self.username = username
        self.session_id = str(uuid.uuid4())
        self.start_time = datetime.datetime.now()
        self.messages = []

    def add_message(self, sender, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.messages.append({
            "time": timestamp,
            "sender": sender,
            "text": message
        })

    def get_summary(self):
        return{
            "user": self.username,
            "session_id": self.session_id,
            "duration": str(datetime.datetime.now() - self.start_time),
            "messages": self.messages
        }
    
class ChatBotManager:
    def __init__(self, client):
        self.client = client
        self.sessions = {}

    def start_session(self, username):
        session = UserSession(username)
        self.sessions[session.session_id] = session
        return session.session_id
    
    def add_user_message(self, session_id, message):
        if session_id not in self.sessions:
            print("Invalid session ID")
            return
        
        session = self.sessions[session_id]
        session.add_message(session.username, message)

        response = self.generate_response(session)
        session.add_message("Bot", response)
        print(f"\n Bot: {response}\n")

    def generate_response(self, session):
        from openai import OpenAI
        client = self.client
        
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        for msg in session.messages:
            role = "user" if msg["sender"] == session.username else "assistant"
            messages.append({"role": role, "content": msg["text"]})

        try:
            response = client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages = messages,
                temperature = 0.7
            )
            return response.choices[0].message['content']
        except Exception as e:
            return f"Error generating response: {str(e)}"
        
     def end_session(self, session_id):
        if session_id in self.sessions:
            summary = self.sessions[session_id].get_summary()
            print(f"\n Session Ended for {summary['user']}")
            print(f"Duration: {summary['duration']}")
            print("Chat Summary:")
            for msg in summary["messages"]:
                print(f"{msg['time']} - {msg['sender']}: {msg['text']}")
            del self.sessions[session_id]
        else:
            print("Invalid session ID.")





