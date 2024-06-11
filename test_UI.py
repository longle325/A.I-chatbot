import streamlit as st
from dataclasses import dataclass
from typing import Literal
import streamlit.components.v1 as components
from chatbot import ChatBot

@dataclass
class Message:
    """Class for keeping track of a chat message.
        Attributes
    ----------
    origin : Literal["human", "ai"]
        The origin of the message, indicating whether it was sent by the human user or the AI.
    message : str
        The content of the chat message.
    """
    origin: Literal["human", "ai"]
    message: str

class ChatApp:
    """
    A class to represent a chat application with a conversational AI assistant.

    Attributes
    ----------
    user_chat : bool
        A flag to indicate if there is an ongoing user chat session.

    Methods
    -------
    __init__():
        Initializes the chat application, setting up session state and loading CSS styles.
    
    initialize_session_state():
        Initializes the session state, including chat history and the chatbot instance.
    
    load_css():
        Loads and applies CSS styles for the chat application from an external stylesheet.
    
    on_click_callback():
        Handles the event when the user submits a chat prompt, generating and displaying the bot's response.
    
    render_sidebar():
        Renders the sidebar with buttons for account status and support service options.
    
    render_chat_history():
        Renders the chat history container, displaying the conversation between the user and the bot.
    
    render_chat_input():
        Renders the chat input form where the user can enter their messages.
    
    render_credit():
        Displays the author's credit at the bottom of the chat application.
    
    run():
        Runs the chat application, rendering the sidebar, chat history, chat input, and credits.
    """
    def __init__(self):
        """
        Initializes the ChatApp class.
        
        This method sets up the initial session state and loads the CSS for the chat application.
        """
        self.initialize_session_state()
        self.load_css()
        self.user_chat = False

    def initialize_session_state(self):
        """
        Initializes the session state for the chat application.
        
        This method sets up the chat history and creates an instance of the chatbot if they do not already exist
        in the session state.
        """
        if "history" not in st.session_state:
            st.session_state.history = []
            st.session_state.history.append(Message("ai", "Xin chào, tôi là trợ lí ảo Leomine. Bạn có thể hỏi tôi bất cứ điều gì!"))
        if "bot" not in st.session_state:
            model_path = "vinai/PhoGPT-4B-Chat"
            st.session_state.bot = ChatBot(model_path)

    def load_css(self):
        """
        Loads and applies CSS styles for the chat application.
        
        This method reads an external CSS file and applies the styles to the Streamlit application.
        """
        with open("/mlcv2/WorkingSpace/Personal/longlb/chatbot/Chatbot_AI_model/static/styles.css", "r") as f:
            css = f"<style>{f.read()}</style>"
            st.markdown(css, unsafe_allow_html=True)
        # with open('/mlcv2/WorkingSpace/Personal/longlb/chatbot/Chatbot_AI_model/static/styles.css') as f:
        #     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    def on_click_callback(self):
        """
        Callback function for handling user input in the chat.
        
        This method retrieves the user's input, generates a response using the chatbot, and updates the chat history.
        """
        instruction = st.session_state.human_prompt
        response = st.session_state.bot.generate_response(instruction)
        st.session_state.history.append(Message("human", instruction))
        st.session_state.history.append(Message("ai", response))
        st.session_state.human_prompt = ""

    def render_sidebar(self):
        """
        Renders the sidebar of the chat application.
        
        This method adds buttons for "Account Status" and "Support Service" to the sidebar.
        """
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
        """
        Renders the chat history container.
        
        This method displays the conversation between the user and the bot, using HTML for formatting.
        """
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
                            else '/mlcv2/WorkingSpace/Personal/longlb/chatbot/Chatbot_AI_model/static/user_icon.png'}"
                width=32 height=32>
            <div class="chat-bubble
            {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
                &#8203;{chat.message}
            </div>
        </div>
                        """
                        st.markdown(div, unsafe_allow_html=True)

    def render_chat_input(self):
        """
        Renders the chat input form.
        
        This method provides an input field for the user to type their messages and handles the submission of the form.
        """
        prompt_placeholder = st.form("chat-form")
        with prompt_placeholder:
            cols = st.columns((6, 1))
            human_prompt = cols[0].text_input(
                "Chat",
                value="",
                label_visibility="collapsed",
                key="human_prompt",
            )
            submit_button = cols[1].form_submit_button(
                "", on_click=self.on_click_callback
            )

            if human_prompt:
                self.on_click_callback()
                

    def render_credit(self):
        """
        Displays the author's credit.
        
        This method shows the author's name at the bottom of the chat application.
        """
        credit_card_placeholder = st.empty()
        credit_card_placeholder.caption("Author: Lê Bảo Long")

    def run(self):
        """
        Runs the chat application.
        
        This method orchestrates the rendering of the sidebar, chat history, chat input form, and the author's credit.
        """
        self.render_sidebar()
        st.markdown("""<div style="display: flex; justify-content: center; align-items: center;">
                        <h1 style="margin-left: 10px;font-family: "Libre Baskerville", serif;font-weight: 400">Leomine</h1>
                        <div style="border: 2px solid black; border-radius: 10px; padding: 5px;">
                            <img src="https://i.pinimg.com/474x/03/cd/45/03cd45a61a83b2aa86e7231cc01b44eb.jpg" width="75" height="75">
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
