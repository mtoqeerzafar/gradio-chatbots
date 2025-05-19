# Gradio Chatbot Applications

This repository contains two AI-powered chatbot applications built with Gradio and GROQ LLM:

1. **MathMind**: A mathematics and computer science tutoring assistant
2. **Sex Education Coach**: A comprehensive sexual health education advisor

## Project Structure

```
gradio-chatbots/
├── mathmind/
│   ├── app.py
│   └── requirements.txt
├── sex-education-coach/
│   ├── app.py
│   └── requirements.txt
└── README.md
```

## Live Demos

Both applications are deployed on Hugging Face Spaces:

- MathMind: [https://huggingface.co/spaces/mtoqeerzafar/MathMind](https://huggingface.co/spaces/mtoqeerzafar/MathMind)
- Sex Education Coach: [https://huggingface.co/spaces/mtoqeerzafar/Sex_Education_Coach](https://huggingface.co/spaces/mtoqeerzafar/Sex_Education_Coach)

## Project Details

### MathMind: Mathematics & CS Assistant

An intelligent tutoring bot specializing in mathematics and computer science:
- Topic-specific guidance with dropdown categories
- Covers Linear Algebra, Probability, Calculus, ML Math, and Algorithms
- Step-by-step explanations and problem-solving assistance
- Powered by GROQ's Llama3-8b model for fast, accurate responses

### Sex Education Coach

A comprehensive sex education chatbot providing safe, informative guidance:
- Evidence-based sexual health information
- Topic categories: General, Consent, Puberty, STIs, and Relationships
- Safe space for asking sensitive questions
- Professional, non-judgmental responses with educational focus

## Technologies

- Python 3.8+
- Gradio (UI framework)
- GROQ API (LLM provider)
- Requests (HTTP client)
- Hugging Face Spaces (deployment)

## Features

- **Topic Selection**: Dropdown menus for focused conversations
- **Chat History**: Maintains context throughout the conversation
- **Clear Chat**: Reset functionality for new sessions
- **Responsive UI**: Clean, modern interface with Gradio
- **Real-time Responses**: Fast API integration with GROQ

## Running Locally

1. Clone this repository
2. Get your GROQ API key from [console.groq.com](https://console.groq.com)
3. Set environment variable:
   ```
   export GROQ_API_KEY="your_api_key_here"
   ```
4. Install requirements:
   ```
   pip install -r mathmind/requirements.txt
   ```
5. Run the application:
   ```
   python mathmind/app.py
   ```
   or
   ```
   python sex-education-coach/app.py
   ```

## Deployment

Both apps are deployed on Hugging Face Spaces with:
- GROQ_API_KEY stored in Spaces secrets
- Automatic builds from repository updates
- Public access with usage analytics

## License

MIT