import streamlit as st
from dataclasses import dataclass
from typing import Literal
import streamlit.components.v1 as components
from chatbot import ChatBot

@dataclass
class Message:
    """Class for keeping track of a chat message."""
    origin: Literal["human", "ai"]
    message: str

class ChatApp:
    def __init__(self):
        self.initialize_session_state()
        self.load_css()

    def initialize_session_state(self):
        if "history" not in st.session_state:
            st.session_state.history = []
        if "bot" not in st.session_state:
            model_path = "vinai/PhoGPT-4B-Chat"
            st.session_state.bot = ChatBot(model_path)

    def load_css(self):
        with open("/mlcv2/WorkingSpace/Personal/longlb/chatbot/Chatbot_AI_model/static/styles.css", "r") as f:
            css = f"<style>{f.read()}</style>"
            st.markdown(css, unsafe_allow_html=True)

    def on_click_callback(self):
        instruction = st.session_state.human_prompt
        response = st.session_state.bot.generate_response(instruction)
        st.session_state.history.append(Message("human", instruction))
        st.session_state.history.append(Message("ai", response))
        st.session_state.human_prompt = ""

    def render_sidebar(self):
        with st.sidebar:
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
            if st.button("Account Status", key="account_status"):
                st.session_state.selected_option = "Account Status"
                st.info("Active!")

            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
            if st.button("Support Service", key="support_service"):
                st.session_state.selected_option = "Support Service"
                st.info("""Contact us at: \n
                        Email: 23520877@gmail.com
            Phone: 0354403877 """)

    def render_chat_history(self):
        with st.container(height=400, border=True):
            chat_placeholder = st.container()
            with chat_placeholder:
                if "history" in st.session_state:
                    for chat in st.session_state.history:
                        div = f"""
        <div class="chat-row 
            {'' if chat.origin == 'ai' else 'row-reverse'}">
            <img class="chat-icon" src="app/static/{
                '/mlcv2/WorkingSpace/Personal/longlb/chatbot/Chatbot_AI_model/static/chatbot.png' if chat.origin == 'ai' 
                            else '/mlcv2/WorkingSpace/Personal/longlb/chatbot/Chatbot_AI_model/static/profile.png'}"
                width=32 height=32>
            <div class="chat-bubble
            {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
                &#8203;{chat.message}
            </div>
        </div>
                        """
                        st.markdown(div, unsafe_allow_html=True)

    def render_chat_input(self):
        prompt_placeholder = st.form("chat-form")
        with prompt_placeholder:
            st.markdown("**Chat**")
            cols = st.columns((6, 1))
            human_prompt = cols[0].text_input(
                "Chat",
                value="",
                label_visibility="collapsed",
                key="human_prompt",
            )
            submit_button = cols[1].form_submit_button(
                "Send", on_click=self.on_click_callback
            )

            if human_prompt:
                self.on_click_callback()

    def render_credit(self):
        credit_card_placeholder = st.empty()
        credit_card_placeholder.caption("Author: Lê Bảo Long")

    def run(self):
        self.render_sidebar()
        st.markdown("""<div style="display: flex; justify-content: center; align-items: center;">
                        <h1 style="margin-left: 10px;">Leomine</h1>
                        <div style="border: 2px solid black; border-radius: 10px; padding: 5px;">
                            <img src="https://cdn-icons-png.flaticon.com/128/897/897219.png" width="60" height="60">
                    </div>
                    </div>""", unsafe_allow_html=True)
        st.markdown("")
        self.render_chat_history()
        st.markdown("")
        self.render_chat_input()
        self.render_credit()

# Initialize and run the chat app
chat_app = ChatApp()
chat_app.run()
