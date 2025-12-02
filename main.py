import chainlit as cl
from chainlit import Message
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# Crisis Helper
# -----------------------------
def ai_response(prompt):
    return f"""Here is your structured response:

**1. Empathetic reflection:**  
I hear how overwhelming this feels for you. It sounds like you're dealing with a lot right now.  

**2. Emotion you might be feeling:**  
You might be feeling stressed, frustrated, or emotionally flooded.  

**3. Grounding/Coping strategies:**  
- Take a slow inhale for 4 seconds, exhale for 6 seconds.  
- Put your feet flat on the floor and notice 3 things you can see around you.  
- Stretch your shoulders or arms to release physical tension.  

**4. Gentle follow-up question:**  
What part of this situation is hitting you the hardest right now?  
"""

# -----------------------------
# Message Handler
# -----------------------------
@cl.on_message
async def start_chat(message: Message):
    user_input = message.content

    prompt = f"""
The user said: {user_input}

Respond in this format:
1. Empathetic reflection (2 lines)
2. What emotion they may be feeling
3. 2–3 grounding or coping strategies
4. A gentle follow-up question
"""

    result = ai_response(prompt)

    await cl.Message(result).send()
