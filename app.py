import streamlit as st
from session_manager import ChatBotManager
from openai import OpenAI

st.set_page_config(page_title="Mr. Bot", page_icon=":robot:", layout="wide")

st.title("Mr. Bot")
st.caption("Built with Streamlit and OpenAI API")

st.sidebar.title("API Settings")
user_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
username = st.sidebar.text_input("Enter your name", value="Guest")

# Stop app until key is provided
if not user_api_key:
    st.warning("Please enter your OpenAI API key in the sidebar.")
    st.stop()

# set up client
client = OpenAI(api_key=user_api_key)

if "bot" not in st.session_state:
    st.session_state.bot = ChatBotManager(client)
    st.session_state.username = username
    st.session_state.session_id = st.session_state.bot.start_session(username)
    
user_input = st.text_input("You:", placeholder="Type your message here...")

if st.button("Send"):
    if user_input.strip():
        st.session_state.bot.add_user_message(st.session_state.session_id, user_input)
    else:
        st.warning("Please type something before sending!")
    
chat = st.session_state.bot.sessions[st.session_state.session_id]
for msg in chat.messages:
    with st.chat_message("user" if msg["sender"] == chat.username else "assistant"):
        st.markdown(msg["text"])

if st.button("End Chat"):
    st.session_state.bot.end_session(st.session_state.session_id)
    st.success("Chat session ended. Reload to start a new chat. Thank you for chatting!")
    st.stop()
