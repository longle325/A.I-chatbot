import streamlit as st
from dataclasses import dataclass
from typing import Literal
import streamlit.components.v1 as components
from chatbot import *

@dataclass
class Message:
    """Class for keeping track of a chat message."""
    origin: Literal["human", "ai"]
    message: str

def load_css():
    with open("/mlcv2/WorkingSpace/Personal/longlb/chatbot/Chatbot_AI_model/static/styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)


def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "bot" not in st.session_state:
        model_path = "vinai/PhoGPT-4B-Chat"
        st.session_state.bot = ChatBot(model_path)
    

def on_click_callback():
    instruction = st.session_state.human_prompt
    response =  st.session_state.bot.generate_response(instruction)
    st.session_state.history.append(Message("human", instruction))
    st.session_state.history.append(Message("ai", response))
    st.session_state.human_prompt = ""

# Ensure session state is initialized   
initialize_session_state()

# Ensure CSS is loaded early in the script
load_css()

# Title of the bot
st.markdown("""
<div style="display: flex; justify-content: center; align-items: center;">
    <h1 style="margin-left: 10px;">Leomine</h1>
    <div style="border: 2px solid black; border-radius: 10px; padding: 5px;">
        <img src="https://cdn-icons-png.flaticon.com/128/897/897219.png" width="60" height="60">
</div>
""", unsafe_allow_html=True)

# Creating sidebar of the Web
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


st.markdown("")    

# Creating a chatlist storing all the history chat with the chatbot
with st.container(height = 400, border = True):
    chat_placeholder = st.container()
    
    with chat_placeholder:
        # Safeguard in case history was not initialized
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

st.markdown("")

# Creating the input text field for typing request or question and "Send button"
# Custom CSS for the circular button
st.markdown("""
<style>
.circular-btn {
    display: inline-block;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    border: none;
    background-color: #ff8c00; /* Button background color */
    color: white; /* Text color */
    font-size: 16px; /* Text size */
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# Creating the input text field for typing request or question and "Send button"
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
    # Add the custom button with circular shape
    submit_button = cols[1].form_submit_button(
        "Send", on_click=on_click_callback
    )

    #if user ask something,activate submit button
    if human_prompt:
        on_click_callback()
    
# JavaScript to handle form submission and 'Enter' key press
components.html("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    const submitButton = window.parent.document.querySelector('.stButton button');
    const form = document.querySelector('form');

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            submitButton.click();
        }
    });

    submitButton.addEventListener('click', function() {
        if (form.reportValidity()) {
            form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
        }
    });
});
</script>
""", 
    height=0,
    width=0
)

# Creating Credit - small words under the boxchat 
credit_card_placeholder = st.empty()
credit_card_placeholder.caption("Author: Lê Bảo Long - Hoàng Minh Thái")
