# 🌿 CalmSpace - AI-Powered Mental Health Support Platform

A comprehensive mental health support chatbot designed specifically for college students, built with Chainlit and OpenAI.

## 📋 Project Overview

College students face increasing mental health challenges including stress, anxiety, depression, and academic pressure. CalmSpace provides a 24/7 anonymous, accessible first-line support system.

### Problem Statement

Design an AI-powered mental health support platform for college students that provides:
- Emotional support and empathetic conversations
- Mood tracking and insights
- Self-help resources and coping strategies
- Guided exercises (breathing, meditation)
- Pathways to professional help when needed

---

## ✨ Features

### Core Functionality

| Feature | Description |
|---------|-------------|
| **Empathetic AI Chat** | Context-aware conversations for 10+ mental health scenarios |
| **Mood Tracking** | Log and view mood history with insights |
| **30-Day Wellness Challenge** | Daily activities with affirmations |
| **Resource Library** | 20+ mental health topics |
| **Guided Exercises** | Breathing techniques and meditation scripts |
| **Journal Prompts** | Reflective questions for self-exploration |
| **Crisis Detection** | Automatic detection with helpline resources |
| **Coping Strategies** | Emotion-specific and general strategies |

### Mental Health Scenarios Covered

1. Exam/Academic Anxiety
2. Loneliness & Isolation
3. Homesickness
4. Burnout
5. Imposter Syndrome
6. Relationship Issues
7. Depression Symptoms
8. Sleep Problems
9. Financial Stress
10. Future/Career Anxiety

### Resource Library Topics (20+)

- Stress Management
- Understanding Anxiety
- Signs of Depression
- Sleep Hygiene
- Exam Preparation
- Building Connections
- Dealing with Homesickness
- Imposter Syndrome
- Academic Burnout
- Healthy Relationships
- Time Management
- Mindfulness Basics
- Self-Compassion
- Managing Panic Attacks
- Substance Use Awareness
- Grief & Loss
- Social Anxiety
- Perfectionism
- Financial Wellness
- When to Seek Help

---

## 🛠️ AI Tools Used

This project integrates multiple AI tools as required:

### 1. OpenAI GPT (Runtime)
- Powers the empathetic conversational AI
- Generates contextual responses
- Handles scenario detection and response

### 2. Claude AI (Content Development)
- Created empathetic response templates
- Designed conversation flows
- Wrote mental health resource content
- Developed crisis handling protocols

### 3. Canva AI (Visual Content)
- Platform logo and branding
- Motivational posters
- Infographics on mental health topics
- UI mockups

### 4. Notion AI (Documentation)
- Organized project documentation
- Structured resource library content
- Created user guides and manuals

### 5. Gamma AI (Presentations)
- Created awareness presentation
- "Breaking the Stigma: Mental Health Matters" slides

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- OpenAI API key

### Steps

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd calmspace
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. **Run the application**
```bash
chainlit run main.py -w
```

5. **Open in browser**
Navigate to http://localhost:8000

---

## 📁 Project Structure

```
calmspace/
├── main.py              # Main application code
├── chainlit.md          # Welcome message and documentation
├── requirements.txt     # Python dependencies
├── runtime.txt          # Python version for deployment
├── .env.example         # Environment variables template
├── .env                 # Your environment variables (not committed)
└── README.md            # This file
```

---

## 💻 Usage

### Quick Commands

| Command | Action |
|---------|--------|
| `menu` | Show all options |
| `mood` | Track your mood |
| `challenge` | Today's wellness challenge |
| `challenge [1-30]` | View specific day |
| `next challenge` | Move to next day |
| `resources` | Browse topic library |
| `breathe` | Breathing exercises |
| `meditate` | Quick meditations |
| `journal` | Get journal prompts |
| `coping` | General coping strategies |
| `coping anxiety` | Anxiety-specific strategies |
| `crisis` | Crisis resources |

### Natural Conversation

Just type how you're feeling! The bot detects context and responds appropriately:

- "I'm stressed about my exam tomorrow"
- "I feel so alone here"
- "I can't sleep at night"
- "I think I'm burning out"

---

## 🌐 Deployment (Free)

### Deploy to Render.com

1. Push your project to GitHub

2. Create account on [Render.com](https://render.com)

3. Create new Web Service

4. Connect your GitHub repository

5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `chainlit run main.py --host 0.0.0.0 --port $PORT`

6. Add environment variable:
   - `OPENAI_API_KEY`: Your OpenAI API key

7. Deploy!

---

## 📊 Deliverables Checklist

- [x] Chatbot conversation flows for 10+ mental health scenarios
- [x] 30-day mental wellness challenge with daily activities and affirmations
- [x] Resource library with 20+ topics
- [ ] Visual content package (15 motivational posts, 10 infographics) - Create in Canva
- [ ] Awareness presentation (20 slides) - Create in Gamma AI
- [x] Crisis escalation protocol
- [ ] Video demonstration (7 minutes) - Record walkthrough

---

## ⚠️ Important Disclaimer

CalmSpace is an AI companion designed to provide emotional support and mental health resources. **It is NOT a replacement for professional mental health care.**

If you or someone you know is experiencing a mental health crisis:

**India**
- AASRA: 9820466726
- iCall: 9152987821

**USA**
- 988 Suicide & Crisis Lifeline: Call/Text 988

**UK**
- Samaritans: 116 123

---

## 👥 Credits

Created using:
- OpenAI GPT-4
- Claude AI (Anthropic)
- Canva AI
- Notion AI
- Gamma AI
- Chainlit Framework

---

## 📄 License

This project is for educational purposes.

---

*You matter. Your feelings are valid. Help is available.* 💙
