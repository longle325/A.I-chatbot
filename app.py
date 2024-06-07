import streamlit as st
import torch
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
import streamlit.components.v1 as components

class ChatBot:
    def __init__(self, model_path, device="cuda:3", torch_dtype=torch.bfloat16):
        self.model_path = model_path
        self.device = device
        self.config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
        self.config.init_device = device

        self.model = AutoModelForCausalLM.from_pretrained(model_path, config=self.config, torch_dtype=torch_dtype, trust_remote_code=True)
        self.model.eval()

        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.prompt_template = "### Câu hỏi: {instruction}\n### Trả lời:"

    def generate_response(self, instruction):
        input_prompt = self.prompt_template.format(instruction=instruction)
        input_ids = self.tokenizer(input_prompt, return_tensors="pt")

        outputs = self.model.generate(
            inputs=input_ids["input_ids"].to(self.device),
            attention_mask=input_ids["attention_mask"].to(self.device),
            do_sample=True,
            temperature=1.0,
            top_k=50,
            top_p=0.9,
            max_new_tokens=1024,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.pad_token_id
        )

        response = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        response = response.split("### Trả lời:")[1]
        return response.strip()

# Initialize ChatBot
bot = ChatBot("vinai/PhoGPT-4B-Chat")

# Streamlit setup
st.set_page_config(page_title="DeepSeek Chat", layout="wide")

# HTML, CSS, and JavaScript code
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DeepSeek Chat</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }
        body, html {
            height: 100%;
            width: 100%;
        }
        .container {
            display: flex;
            height: 100vh;
        }
        .sidebar {
            width: 25%;
            background-color: #f8f9fa;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 20px;
        }
        .sidebar-button {
            background-color: #f8f9fa;
            color: black;
            font-weight: bold;
            border: none;
            padding: 15px;
            text-align: left;
            width: 100%;
            margin-bottom: 10px;
            cursor: pointer;
        }
        .sidebar-button.active {
            background-color: #007bff;
            color: white;
        }
        .api-button {
            color: red;
        }
        .terms p {
            color: #6c757d;
            font-size: 12px;
            text-align: left;
        }
        .chat-area {
            width: 75%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 20px;
        }
        .chat-display {
            background-color: #e9ecef;
            padding: 20px;
            flex-grow: 1;
            overflow-y: auto;
            margin-bottom: 10px;
            border-radius: 5px;
        }
        .input-area {
            display: flex;
        }
        #chat-input {
            flex-grow: 1;
            padding: 15px;
            border: 1px solid #ced4da;
            border-radius: 5px 0 0 5px;
        }
        #send-button {
            padding: 15px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 0 5px 5px 0;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <button class="sidebar-button active">DeepSeek-V2 Chat</button>
            <button class="sidebar-button">DeepSeek Coder</button>
            <div class="sidebar-bottom">
                <button class="sidebar-button">Contact us</button>
                <button class="sidebar-button">My Profile</button>
                <button class="sidebar-button api-button">API Platform</button>
                <div class="terms">
                    <p>Service Status · Terms of Use · Privacy Policy</p>
                </div>
            </div>
        </div>
        <div class="chat-area">
            <div class="chat-display" id="chat-display">
                <p>Hi, I'm DeepSeek Chat assistant. Feel free to ask me anything!</p>
            </div>
            <div class="input-area">
                <input type="text" id="chat-input" placeholder="Send a message">
                <button id="send-button">Send</button>
            </div>
        </div>
    </div>
    <script>
        const sendButton = document.getElementById('send-button');
        const chatInput = document.getElementById('chat-input');
        const chatDisplay = document.getElementById('chat-display');

        sendButton.addEventListener('click', () => {
            const message = chatInput.value.trim();
            if (message) {
                const userMessage = document.createElement('p');
                userMessage.textContent = `You: ${message}`;
                chatDisplay.appendChild(userMessage);

                // Clear the input box
                chatInput.value = '';

                // Send the message to Streamlit backend
                const formData = new FormData();
                formData.append('message', message);

                fetch('/send_message', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    const botMessage = document.createElement('p');
                    botMessage.textContent = `Bot: ${data.response}`;
                    chatDisplay.appendChild(botMessage);
                });
            }
        });
    </script>
</body>
</html>
"""

# Display the HTML code in Streamlit
components.html(html_code, height=700, scrolling=True)

# Streamlit backend to handle chatbot responses
if 'chatbot' not in st.session_state:
    st.session_state['chatbot'] = ChatBot(model_path="path_to_your_model")

# Endpoint to handle message sending
def handle_message():
    message = st.experimental_get_query_params().get('message', [''])[0]
    if message:
        response = st.session_state['chatbot'].generate_response(message)
        st.write({'response': response})

st.experimental_singleton(handle_message)
