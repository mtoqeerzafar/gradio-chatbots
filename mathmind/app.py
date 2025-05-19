import gradio as gr
import os
import requests

# Load GROQ API key from environment (set it in Hugging Face secrets)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-8b-8192"
CHATBOT_NAME = "MathMind"  # Added chatbot name

# Updated system prompt with the chatbot name
SYSTEM_PROMPT = f"""You are {CHATBOT_NAME}, an expert mathematics and computer science assistant specializing in:
- Linear algebra (vectors, matrices, eigenvalues, SVD)
- Probability and statistics (distributions, hypothesis testing, Bayesian methods)
- Discrete mathematics (graph theory, combinatorics, logic)
- Calculus (differentiation, integration, series)
- Multivariable calculus (gradients, Hessians, optimization)
- Differential equations (ODEs, PDEs, numerical solutions)
As {CHATBOT_NAME}, you provide:
1. Clear, step-by-step mathematical solutions with {CHATBOT_NAME}'s signature clarity
2. Computer science applications (algorithms, data structures)
3. Data science perspectives (ML model implications, feature engineering)
4. Python/Numpy implementations when relevant
5. Visual explanations (suggest plots/graphs when helpful)
Always respond as {CHATBOT_NAME}:
- Use precise mathematical notation
- Explain concepts intuitively
- Connect math to practical CS applications
- Suggest relevant algorithms or libraries
- Maintain academic rigor while being approachable
- Sign off with "- {CHATBOT_NAME}" at the end of each response"""

def query_groq(message, chat_history):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for conversation in chat_history:
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
    # Updated interface with chatbot name
    gr.Markdown(f"""
    <style>
        .gradio-container {{
            font-family: 'Arial', sans-serif;
            background-color: #f5f5f5;
            border-radius: 12px;
            padding: 25px;
        }}
        .chatbox {{
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            max-height: 400px;
            overflow-y: scroll;
        }}
        .user {{
            background-color: #d4edff;
            padding: 10px;
            margin: 7px 0;
            border-radius: 14px;
            text-align: right;
        }}
        .bot {{
            background-color: #f0f7ff;
            padding: 10px;
            margin: 7px 0;
            border-radius: 14px;
            text-align: left;
            position: relative;
        }}
        .bot::before {{
            content: "{CHATBOT_NAME}:";
            font-weight: bold;
            color: #3366cc;
            margin-right: 5px;
        }}
        .gr-textbox {{
            font-size: 18px;
            border-radius: 10px;
            padding: 15px;
            border: 1px solid #ddd;
            background-color: #ffffff;
        }}
        .gr-button {{
            background-color: #1e88e5;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            transition: background-color 0.3s;
        }}
        .gr-button:hover {{
            background-color: #1565c0;
        }}
        .title {{
            color: #3366cc;
            text-align: center;
            margin-bottom: 20px;
        }}
        .send-button {{
            background-color: #1e88e5 !important;
        }}
        .clear-button {{
            background-color: #1e88e5 !important;
        }}
    </style>
    <h1 class="title">🧮 {CHATBOT_NAME}: Your Mathematics & CS Assistant</h1>
    <p style="text-align: center; color: #555;">Powered by GROQ LLM | Ask me anything about math, algorithms, or data science!</p>
    """)

    chat_history = gr.State([])
    
    topic = gr.Dropdown(
        choices=["General", "Linear Algebra", "Probability", "Calculus", "ML Math", "Algorithms"],
        value="General",
        label="Choose a topic (optional)"
    )
    
    with gr.Column():
        chatbot = gr.Chatbot(
            [],
            elem_id="chatbot",
            avatar_images=("https://i.imgur.com/xQBdKKI.png", "https://i.imgur.com/7vKRQ3T.png"),  # Updated bot avatar
        )
        
        with gr.Row():
            msg = gr.Textbox(
                show_label=False,
                placeholder=f"Ask {CHATBOT_NAME} a question (e.g., 'Explain gradient descent')...",
                container=False
            )
        
        with gr.Row():
            submit = gr.Button("Send", elem_classes="send-button")
            clear = gr.Button("Clear", elem_classes="clear-button")
    
    def process_and_respond(message, chat_history, topic):
        message_with_topic = add_topic_to_message(message, topic)
        return respond(message_with_topic, chat_history)
    
    msg.submit(process_and_respond, [msg, chat_history, topic], [msg, chatbot])
    submit.click(process_and_respond, [msg, chat_history, topic], [msg, chatbot])
    clear.click(lambda: ([], []), outputs=[chatbot, chat_history])

if __name__ == "__main__":
    demo.launch(share=True)