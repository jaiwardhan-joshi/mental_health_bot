import chainlit as cl
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversation_memory = []

def ai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a warm, empathetic mental health support assistant."},
            *conversation_memory,
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message["content"]


def generate_daily_challenge():
    prompt = "Generate 1 short wellness challenge for students (2–3 lines)."
    return ai_response(prompt)


def generate_journal_prompts():
    prompt = "Give 3 short mood journaling prompts for self-reflection."
    return ai_response(prompt)


def mental_health_support(user_msg):
    prompt = f"""
User: "{user_msg}"

Provide:
1. 2-line empathetic reflection  
2. Emotion they may be feeling  
3. 2-3 grounding/coping strategies  
4. Gentle follow-up question
"""
    return ai_response(prompt)


def crisis_check(user_msg):
    crisis_keywords = ["suicide", "kill myself", "end my life", "can't continue", "self harm", "die"]

    if any(word in user_msg.lower() for word in crisis_keywords):
        return """⚠️ **Important Notice**

I'm really sorry you're feeling this way.

☎️ **AASRA India:** 9820466726  
☎️ **988 Suicide & Crisis Lifeline (USA)**  
🏥 Visit the nearest hospital emergency room.

You deserve support — please reach out immediately."""
    return None


@cl.on_chat_start
async def on_chat_start(data):
    conversation_memory.clear()

    await cl.Message("""
👋 **Welcome to the Mental Health Support Assistant**

I'm here to support you with stress, anxiety, exam pressure, loneliness, burnout — anything on your mind.

Try:
- "I'm stressed"
- "Give me a challenge"
- "journal prompts"
- "I feel anxious"

How are you feeling today?
""").send()


@cl.on_message
async def on_message(message, data):
    user_msg = message["content"]

    conversation_memory.append({"role": "user", "content": user_msg})
    conversation_memory[:] = conversation_memory[-10:]

    crisis = crisis_check(user_msg)
    if crisis:
        await cl.Message(crisis).send()
        return

    if "challenge" in user_msg.lower():
        txt = generate_daily_challenge()
        await cl.Message(f"🌱 **Your Daily Wellness Challenge:**\n\n{txt}").send()
        return

    if "journal" in user_msg.lower() or "prompt" in user_msg.lower():
        txt = generate_journal_prompts()
        await cl.Message(f"📓 **Journal Prompts:**\n\n{txt}").send()
        return

    reply = mental_health_support(user_msg)
    conversation_memory.append({"role": "assistant", "content": reply})
    conversation_memory[:] = conversation_memory[-10:]

    await cl.Message(reply).send()
