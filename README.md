# Health Query Chatbot with TinyLlama

A safety-focused health information chatbot using TinyLlama-1.1B-Chat model.

## Features

# Prompt Engineering:

Clear system prompt defining the assistant's role and constraints

Rules for safe, non-diagnostic responses

Tone and length guidelines

# Safety Mechanisms:

Keyword filtering for potentially dangerous content

Automatic disclaimer addition for medical-adjacent responses

Response sanitization to remove markdown formatting

# User Experience:

Friendly, conversational interface

Error handling for API issues

Interactive chat loop or single query mode

# Customization:

Adjustable temperature parameter

## How to Use
Install requirements:

bash
pip install openai regex
Get an OpenAI API key:

Create an account at platform.openai.com

Get your API key from the "API Keys" section

# Run the chatbot:

Replace "your-api-key-here" with your actual key

# Run the script: 
python health_chatbot.py

# Example queries to test:

"What are common causes of headaches?"

"How much water should I drink daily?"

"When should I see a doctor for a fever?"

Model selection flexibility

Configurable safety keywords
