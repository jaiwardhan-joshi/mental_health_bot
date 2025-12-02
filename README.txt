CalmSpace - Chainlit Mental Health Support Bot

PROJECT OVERVIEW

College students often struggle with stress, anxiety, academic pressure, loneliness, homesickness, and emotional instability. Many hesitate to seek help due to stigma or lack of awareness.
This project provides a 24/7 AI-powered mental-health support platform designed specifically for students.

The platform includes:
• Emotional support chatbot
• Guided self-help tools
• Mood tracking system
• Personalized coping strategies
• Anonymous conversations
• Crisis detection and escalation
• Learning resources
• Tool-based content creation using ChatGPT, Claude, Canva, Notion AI

PROBLEM STATEMENT

Design an AI-powered mental health support platform specifically for college students that offers:

• Anonymous emotional support
• Mood tracking
• Stress management
• Self-help resources
• Pathways to professional help
• 24/7 access
• AI-generated insights
• Student-focused interface

USE OF REQUIRED AI TOOLS

The project integrates multiple required AI tools:

ChatGPT

Creates coping strategies

Generates meditation scripts

Assists with journaling prompts

Provides mood interpretation

Used in the Chainlit backend

Claude AI

Creates empathetic response templates

Generates mental-health topic explanations

Helps design guided support flows

Assists in writing safe-crisis-handling text

Canva AI

Creates visual posters (stress management, sleep hygiene, exam tips)

Generates platform logo

Creates UI mockup for the app

Makes simple infographics (optional)

Notion AI

Used to organize project documentation

Manages mood resource library

Writes structured step-by-step manuals

Stores the generated scripts and flows

These tools make the project valid for the required multi-AI-tool rubric.

FEATURES

• AI chatbot using GPT
• Mood tracking with memory storage
• Daily mood insights
• Resource library (anxiety, sleep, exam pressure, etc.)
• Guided journaling prompts
• Breathing & meditation scripts
• Crisis word detection
• Alerts for severe distress
• Conversation history recall
• Personalized suggestions based on mood trends
• Chainlit UI

TECHNOLOGIES USED

• Python
• Chainlit
• OpenAI API
• SQLite (in-memory dictionary alternative)
• dotenv
• HTML/CSS (Chainlit frontend)
• GitHub
• Render.com (free hosting)

INSTALLATION GUIDE

Install Python 3.10 or above

Install dependencies:

pip install chainlit openai python-dotenv sqlitedict

Create a file named .env with your OpenAI API key:

OPENAI_API_KEY=your_key_here

Start the app:

chainlit run main.py -w

Open the local host URL shown in terminal.

FILE STRUCTURE

mental_health_bot/
|-- main.py
|-- requirements.txt
|-- chainlit.md
|-- README.txt
|-- .env

DEPLOYMENT (FREE)

The easiest free hosting method:

Push project to GitHub

Create an account on Render.com

Select "New → Web Service"

Connect the GitHub repo

Use the following commands:

Build Command:
pip install -r requirements.txt

Start Command:
chainlit run main.py --host 0.0.0.0 --port $PORT

Deploy.
Your AI mental health platform is now live online.

CREDITS

Created using:
ChatGPT
Claude
Canva AI
Notion AI
Chainlit Framework
OpenAI GPT models
