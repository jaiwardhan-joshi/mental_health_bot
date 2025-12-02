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
    return response.choices[0].message.content


def generate_daily_challenge():
    prompt = "Generate 1 short wellness challenge for students (2-3 lines)."
    return ai_response(prompt)


def generate_journal_prompts():
    prompt = "Give 3 short mood journaling prompts for self-reflection."
    return ai_response(prompt)


def mental_health_support(user_msg):
    prompt = (
        f'User: "{user_msg}"\n\n'
        "Provide:\n"
        "1. 2-line empathetic reflection\n"
        "2. Emotion they may be feeling\n"
        "3. 2-3 grounding/coping strategies\n"
        "4. Gentle follow-up question"
    )
    return ai_response(prompt)


def crisis_check(user_msg):
    crisis_keywords = ["suicide", "kill myself", "end my life", "can't continue", "self harm", "die"]

    if any(word in user_msg.lower() for word in crisis_keywords):
        crisis_message = (
            "Warning: Important Notice\n\n"
            "I'm really sorry you're feeling this way.\n\n"
            "Phone: AASRA India: 9820466726\n"
            "Phone: 988 Suicide & Crisis Lifeline (USA)\n"
            "Hospital: Please go to the nearest hospital if you feel unsafe.\n\n"
            "You deserve support - please reach out immediately."
        )
        return crisis_message
    return None


@cl.on_chat_start
async def on_chat_start():
    conversation_memory.clear()

    welcome_message = (
        "Welcome to the Mental Health Support Assistant\n\n"
        "I'm here to support you with stress, anxiety, exam pressure, "
        "loneliness, burnout - anything on your mind.\n\n"
        "Try:\n"
        '- "I\'m stressed"\n'
        '- "Give me a challenge"\n'
        '- "journal prompts"\n'
        '- "I feel anxious"\n\n'
        "How are you feeling today?"
    )
    
    await cl.Message(welcome_message).send()


@cl.on_message
async def on_message(message: cl.Message):
    user_msg = message.content
    
    conversation_memory.append({"role": "user", "content": user_msg})
    conversation_memory[:] = conversation_memory[-10:]

    crisis = crisis_check(user_msg)
    if crisis:
        await cl.Message(crisis).send()
        return

    if "challenge" in user_msg.lower():
        txt = generate_daily_challenge()
        challenge_msg = f"Your Daily Wellness Challenge:\n\n{txt}"
        await cl.Message(challenge_msg).send()
        return

    if "journal" in user_msg.lower() or "prompt" in user_msg.lower():
        txt = generate_journal_prompts()
        journal_msg = f"Journal Prompts:\n\n{txt}"
        await cl.Message(journal_msg).send()
        return

    reply = mental_health_support(user_msg)
    conversation_memory.append({"role": "assistant", "content": reply})
    conversation_memory[:] = conversation_memory[-10:]

    await cl.Message(reply).send()
