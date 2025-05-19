import gradio as gr
import os
import requests

# Load GROQ API key from environment (set it in Hugging Face secrets)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  # <-- Make sure this key is securely set
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-8b-8192"  # Balanced and fast for Q&A bots

# Customize this system prompt based on your bot's role
SYSTEM_PROMPT = """You are a respectful, knowledgeable, and non-judgmental sex education assistant. 
You provide accurate, age-appropriate, and inclusive information about sexual health, relationships, consent, and the human body. 
Your tone is friendly, supportive, and clear. You avoid explicit content unless necessary for educational purposes and always promote safety, respect, and well-being."""

def query_groq(message, chat_history):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for conversation in chat_history:
        # Make sure we have proper role and content format for each message
        if isinstance(conversation, tuple) and len(conversation) == 2:
            user_msg, bot_msg = conversation
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
    
    messages.append({"role": "user", "content": message})

    response = requests.post(GROQ_API_URL, headers=headers, json={
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.7
    })

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return reply
    else:
        return f"Error {response.status_code}: {response.text}"

def respond(message, chat_history):
    if not message.strip():
        return "", chat_history
        
    bot_reply = query_groq(message, chat_history)
    chat_history = chat_history + [[message, bot_reply]]
    return "", chat_history

def add_topic_to_message(message, topic):
    if topic and topic != "General":
        return f"[{topic}] {message}"
    return message

with gr.Blocks() as demo:
    # Customizing the layout and design for a sex education coach theme
    gr.Markdown("""
    <style>
        .gradio-container {
            font-family: 'Arial', sans-serif;
            background-color: #f0f9ff;
            border-radius: 12px;
            padding: 25px;
        }
        .chatbox {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            max-height: 400px;
            overflow-y: scroll;
        }
        .user {
            background-color: #ffb6c1;
            padding: 10px;
            margin: 7px 0;
            border-radius: 14px;
            text-align: right;
        }
        .bot {
            background-color: #e0f7fa;
            padding: 10px;
            margin: 7px 0;
            border-radius: 14px;
            text-align: left;
        }
        .gr-textbox {
            font-size: 18px;
            border-radius: 10px;
            padding: 15px;
            border: 1px solid #ddd;
            background-color: #ffffff;
        }
        .gr-button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            padding: 12px 24px;
            font-size: 18px;
        }
        .gr-button:hover {
            background-color: #45a049;
        }
    </style>
    ## 🌍 Your Sex Education Coach (Powered by GROQ LLM)
    """)

    # Create chat history state
    chat_history = gr.State([])
    
    # Topic selection
    topic = gr.Dropdown(
        choices=["General", "Consent", "Puberty", "STIs", "Relationships"],
        value="General",
        label="Choose a topic (optional)"
    )
    
    # Chat interface
    with gr.Column():
        chatbot = gr.Chatbot(
            [],
            elem_id="chatbot",
            avatar_images=["https://i.imgur.com/xQBdKKI.png", "https://i.imgur.com/zHnKs9t.png"],
        )
        
        with gr.Row():
            msg = gr.Textbox(
                show_label=False,
                placeholder="Ask a question about sexual health...",
                container=False
            )
        
        with gr.Row():
            submit = gr.Button("Send")
            clear = gr.Button("Clear")
    
    # Define combined function to process topic and then respond
    def process_and_respond(message, chat_history, topic):
        message_with_topic = add_topic_to_message(message, topic)
        return respond(message_with_topic, chat_history)
    
    # Connect the components
    msg.submit(process_and_respond, [msg, chat_history, topic], [msg, chatbot])
    submit.click(process_and_respond, [msg, chat_history, topic], [msg, chatbot])
    clear.click(lambda: ([], []), outputs=[chatbot, chat_history])

# Launch the app
if __name__ == "__main__":
    demo.launch(share=True)