import chainlit as cl
from openai import OpenAI
import os

# Create OpenAI client (Render injects OPENAI_API_KEY)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------------------
# Store short-term memory (last 10 msgs)
# ---------------------------------------
conversation_memory = []


# ---------------------------------------
# Helper: Generate AI responses
# ---------------------------------------
def ai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a warm, empathetic mental health support assistant for college students."},
            *conversation_memory,
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]


# ---------------------------------------
# Daily Wellness Challenge
# ---------------------------------------
def generate_daily_challenge():
    prompt = """
Generate 1 simple, actionable daily mental wellness challenge for students.
Keep it short (2–3 lines).
"""
    return ai_response(prompt)


# ---------------------------------------
# Journal Prompts
# ---------------------------------------
def generate_journal_prompts():
    prompt = """
Give 3 short mood journaling prompts for self-reflection.
Keep them simple and supportive.
"""
    return ai_response(prompt)


# ---------------------------------------
# Support Flow
# ---------------------------------------
def mental_health_support(user_msg):
    prompt = f"""
The user says: "{user_msg}"

Provide:
1. Empathetic reflection (2 lines)
2. What emotion they may be feeling
3. 2–3 grounding or coping strategies
4. A gentle follow-up question
"""
    return ai_response(prompt)


# ---------------------------------------
# Crisis Detection
# ---------------------------------------
def crisis_check(user_msg):
    crisis_words = ["suicide", "kill myself", "end my life", "can't continue", "die", "self harm"]

    if any(word in user_msg.lower() for word in crisis_words):
        return """⚠️ **Important Notice**

I'm really sorry you're feeling this way.  
Please contact someone who can help immediately:

📞 **AASRA Helpline (India): 9820466726**  
📞 **Suicide & Crisis Lifeline (USA): 988**  
🏥 Go to the nearest hospital or emergency room.

You deserve support — please reach out now."""
    return None


# ---------------------------------------
# Chat Start
# ---------------------------------------
@cl.on_chat_start
async def on_start():
    conversation_memory.clear()

    await cl.Message("""
👋 **Welcome to the Mental Health Support Assistant**

I'm here to listen and support you with stress, anxiety, exams, relationships, burnout, loneliness — anything on your mind.

You can say things like:
- "I'm stressed about exams"
- "I feel lonely"
- "Give me a wellness challenge"
- "Give me journaling prompts"
- "I'm anxious"

How are you feeling today?
""").send()


# ---------------------------------------
# Message Handler
# ---------------------------------------
@cl.on_message
async def message_handler(message: cl.Message):

    user_msg = message.content

    # Save message to memory
    conversation_memory.append({"role": "user", "content": user_msg})
    conversation_memory[:] = conversation_memory[-10:]  # keep last 10

    # Crisis check
    crisis = crisis_check(user_msg)
    if crisis:
        await cl.Message(crisis).send()
        return

    # Special commands
    if "challenge" in user_msg.lower():
        out = generate_daily_challenge()
        await cl.Message(f"🌱 **Your Daily Wellness Challenge:**\n\n{out}").send()
        return

    if "journal" in user_msg.lower() or "prompt" in user_msg.lower():
        out = generate_journal_prompts()
        await cl.Message(f"📓 **Mood Journaling Prompts:**\n\n{out}").send()
        return

    # Default support message
    reply = mental_health_support(user_msg)

    # Save assistant reply to memory
    conversation_memory.append({"role": "assistant", "content": reply})
    conversation_memory[:] = conversation_memory[-10:]

    await cl.Message(reply).send()
