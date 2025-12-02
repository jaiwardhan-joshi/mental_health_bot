# main.py
import os
import chainlit as cl
from openai import OpenAI
from sqlitedict import SqliteDict
import time
import textwrap
from dotenv import load_dotenv

# ----------------------------
# Load config
# ----------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-4o-mini")
DB_PATH = os.getenv("DB_PATH", "memory_db.sqlite")

if not OPENAI_API_KEY:
    raise RuntimeError("Please set OPENAI_API_KEY in .env")

client = OpenAI(api_key=OPENAI_API_KEY)
db = SqliteDict(DB_PATH, autocommit=True)

# ----------------------------
# Static data: flows, resources, challenge
# ----------------------------

SCENARIO_FLOWS = {
    "exam_stress": {
        "title": "Exam Stress",
        "triggers": ["exam", "test", "midterm", "finals", "grades"],
        "bot_script": [
            "I hear you — exams can feel overwhelming. Can you tell me one thing you’re most worried about?",
            "Let's try a quick grounding exercise together — can you name 5 things you can see right now?"
        ],
        "grounding": "5-4-3-2-1 grounding (name 5 things you can see...)",
        "escalate_when": "inability to eat/sleep for >1 week or suicidal ideation"
    },
    "loneliness": {
        "title": "Loneliness & Homesickness",
        "triggers": ["lonely", "homesick", "miss home", "no friends"],
        "bot_script": [
            "Feeling alone is really hard. Would you like some ideas to connect with others on campus?",
            "We can try a small social challenge you can try this week."
        ],
        "grounding": "Breathing and small actions list",
        "escalate_when": "prolonged isolation for weeks + mood deterioration"
    },
    "panic_attack": {
        "title": "Panic Attack",
        "triggers": ["panic attack", "can't breathe", "panic", "hyperventilating"],
        "bot_script": [
            "I’m sorry you’re having this. Let’s do a grounding/box-breathing method now. Breathe in for 4, hold 4, out 4, hold 4.",
            "Are you in a safe place? If not call local emergency services immediately."
        ],
        "grounding": "Box breathing",
        "escalate_when": "loss of consciousness or severe chest pain"
    },
    "depression_signs": {
        "title": "Low Mood / Depression Signs",
        "triggers": ["depressed", "can't get out of bed", "nothing matters", "no motivation"],
        "bot_script": [
            "I’m really sorry you're feeling this way. Can you tell me when this started?",
            "Would you like some small steps to try today? (sleep, short walk, water, reach out)"
        ],
        "grounding": "Activity scheduling + tiny steps",
        "escalate_when": "suicidal thoughts or self-harm"
    },
    "breakup": {
        "title": "Breakup / Relationship Loss",
        "triggers": ["breakup", "he left", "she left", "we broke up"],
        "bot_script": [
            "Breakups hurt a lot. I’m here with you. Want to talk about what happened, or try some coping steps?",
            "Try writing one thing you learned from the relationship — it can help in recovery."
        ],
        "grounding": "Self-compassion journaling"
    },
    "sleep_problems": {
        "title": "Sleep Problems",
        "triggers": ["can't sleep", "insomnia", "sleep late", "won't sleep"],
        "bot_script": [
            "Sleep troubles are common during stress. When do you usually go to bed?",
            "Here are two simple sleep hygiene tips: reduce screens 30 minutes before bed, keep a consistent wake time."
        ],
        "grounding": "Progressive muscle relaxation script"
    },
    "social_anxiety": {
        "title": "Social Anxiety",
        "triggers": ["anxious in social", "can't talk", "nervous in class"],
        "bot_script": [
            "Social situations can be so stressful. Want a small role-play practice or a breathing exercise first?",
            "A short exposure exercise (1 small interaction) can help — want one suggested?"
        ],
        "grounding": "Small exposure + breathing"
    },
    "overthinking": {
        "title": "Overthinking",
        "triggers": ["overthinking", "stuck in my head", "can't stop thinking"],
        "bot_script": [
            "Overthinking is draining. Let's try a 2-minute timed worry period: write it down for 2 minutes, then close it.",
            "Would you like a breathing or distraction exercise?"
        ],
        "grounding": "Timed worry period"
    },
    "confidence": {
        "title": "Low Confidence",
        "triggers": ["not confident", "imposter", "i'm worthless", "can't do it"],
        "bot_script": [
            "You’re not alone in feeling this — let’s list 3 small wins you had recently.",
            "Try a short self-affirmation practice today."
        ],
        "grounding": "3 wins list"
    },
    "anger_management": {
        "title": "Anger",
        "triggers": ["angry", "mad", "furious", "want to hit"],
        "bot_script": [
            "Anger is a strong signal. Are you safe right now?",
            "Try 60 seconds of paced breathing and 2 minutes of movement (walk, push-ups)."
        ],
        "grounding": "Paced breathing + movement"
    }
}

RESOURCE_LIBRARY = {
    "stress_management": {
        "title": "Stress Management",
        "summary": "Simple tools to reduce acute stress and build long-term resilience.",
        "symptoms": ["Irritability", "difficulty concentrating", "sleep issues"],
        "tips": [
            "Practice 5-10 minutes of daily deep breathing.",
            "Break tasks into 25-minute focused sessions (Pomodoro).",
            "Prioritize sleep and movement."
        ],
        "when_to_seek_help": "If stress persists >2 weeks and affects daily function."
    },
    "sleep_hygiene": {
        "title": "Sleep Hygiene",
        "summary": "Steps to improve sleep quality.",
        "symptoms": ["Trouble falling asleep", "non-restorative sleep"],
        "tips": [
            "Keep consistent sleep/wake times.",
            "Avoid screens 30 minutes before bed.",
            "Limit caffeine after 2 pm."
        ],
        "when_to_seek_help": "If insomnia persists >3 weeks."
    },
    "depression_signs": {
        "title": "Depression — Signs & Support",
        "summary": "Recognizing signs of depression and where to get help.",
        "symptoms": ["Low mood", "loss of interest", "changes in appetite/sleep"],
        "tips": [
            "Share your feelings with someone you trust.",
            "Try small daily goals and activity scheduling."
        ],
        "when_to_seek_help": "If you have suicidal thoughts or severe functional decline."
    },
    "anxiety": {
        "title": "Anxiety & Panic",
        "summary": "Understanding anxiety and immediate coping strategies.",
        "symptoms": ["Racing heart", "restlessness", "excessive worry"],
        "tips": [
            "Use grounding techniques: 5-4-3-2-1.",
            "Practice diaphragmatic breathing."
        ],
        "when_to_seek_help": "If panic attacks are recurrent or disabling."
    },
    "panic_attack": {
        "title": "Panic Attack — Immediate Steps",
        "summary": "Short steps to recover during a panic attack.",
        "symptoms": ["Shortness of breath", "chest tightness", "dizziness"],
        "tips": [
            "Box breathing: 4-4-4-4.",
            "Sit down, loosen clothes, splash cold water on face."
        ],
        "when_to_seek_help": "Severe chest pain or fainting -> emergency services."
    },
    "time_management": {
        "title": "Time Management",
        "summary": "Simple methods to manage study load without burnout.",
        "tips": ["Pomodoro method", "Prioritize MITs (Most important tasks)", "Use a planner"]
    },
    "burnout": {
        "title": "Burnout",
        "summary": "How burnout looks and how to recover.",
        "tips": ["Schedule rest", "Reassess workload", "Talk to peers/counselor"]
    },
    "supporting_friends": {
        "title": "How to support a friend",
        "summary": "Practical steps to help a friend in distress.",
        "tips": ["Listen without judgment", "Ask if they are safe", "Encourage professional help"]
    },
    "substance_awareness": {
        "title": "Substance Use Awareness",
        "summary": "Understanding when use becomes risky and how to get help."
    },
    "suicide_warning": {
        "title": "Suicide Warning Signs",
        "summary": "Recognize important warning signs and immediate steps to take."
    },
    "body_image": {"title": "Body Image"},
    "study_stress_balance": {"title": "Study–Stress Balance"},
    "mindfulness": {"title": "Mindfulness Basics"},
    "breathing_techniques": {"title": "Breathing Techniques"},
    "anger_management": {"title": "Anger Management"},
    "sleep_routine": {"title": "Healthy Sleep Routine"},
    "academic_pressure": {"title": "Academic Pressure"},
    "social_comparison": {"title": "Social Comparison"},
    "healthy_boundaries": {"title": "Healthy Boundaries"},
    "how_to_talk_to_counselor": {"title": "How to talk to a counselor"}
}

THIRTY_DAY_CHALLENGE = [
    {"day": 1, "task": "5-minute deep breathing", "affirmation": "I can begin with one breath."},
    {"day": 2, "task": "Write 3 things you're grateful for", "affirmation": "I notice what helps me."},
    {"day": 3, "task": "10-minute walk outside", "affirmation": "Movement calms me."},
    {"day": 4, "task": "Digital curfew 30 mins before bed", "affirmation": "I deserve rest."},
    {"day": 5, "task": "Write a 2-minute journal entry", "affirmation": "My feelings matter."},
    {"day": 6, "task": "Try a short guided meditation (5 mins)", "affirmation": "I can be calm."},
    {"day": 7, "task": "Reach out to a friend", "affirmation": "Connection helps."},
    {"day": 8, "task": "Drink 2 extra glasses of water", "affirmation": "I nourish my body."},
    {"day": 9, "task": "Practice 5-4-3-2-1 grounding", "affirmation": "I am here now."},
    {"day": 10, "task": "Declutter your workspace for 10 minutes", "affirmation": "I create a calmer space."},
    {"day": 11, "task": "List 3 small wins this week", "affirmation": "I celebrate myself."},
    {"day": 12, "task": "Do a 10-minute stretching routine", "affirmation": "My body supports me."},
    {"day": 13, "task": "Turn phone on Do Not Disturb for 1 hour", "affirmation": "I protect my focus."},
    {"day": 14, "task": "Prepare a healthy meal", "affirmation": "I care for my health."},
    {"day": 15, "task": "Practice progressive muscle relaxation (10 mins)", "affirmation": "I release tension."},
    {"day": 16, "task": "Write a short letter to future you", "affirmation": "I am growing."},
    {"day": 17, "task": "Do something creative (draw, doodle, sing)", "affirmation": "Creativity refreshes me."},
    {"day": 18, "task": "Spend 15 minutes in sunlight", "affirmation": "Light helps my mood."},
    {"day": 19, "task": "Say no to one thing you don't want to do", "affirmation": "My boundaries matter."},
    {"day": 20, "task": "Read a short inspiring article or poem", "affirmation": "Inspiration finds me."},
    {"day": 21, "task": "Try a 5-minute body scan", "affirmation": "I listen to my body."},
    {"day": 22, "task": "Make a simple to-do list for tomorrow", "affirmation": "I plan kindly."},
    {"day": 23, "task": "Practice mindful eating for one meal", "affirmation": "I savor nourishment."},
    {"day": 24, "task": "Watch one funny short video", "affirmation": "Laughter helps."},
    {"day": 25, "task": "Offer a compliment to someone", "affirmation": "Kindness connects us."},
    {"day": 26, "task": "Try box breathing (4-4-4-4)", "affirmation": "My breath steadies me."},
    {"day": 27, "task": "List 3 things you like about yourself", "affirmation": "I accept myself."},
    {"day": 28, "task": "Practice a 10-minute guided relaxation", "affirmation": "Rest is necessary."},
    {"day": 29, "task": "Plan one social activity for next week", "affirmation": "Connections are possible."},
    {"day": 30, "task": "Reflect: what helped most this month?", "affirmation": "I did the work."}
]

# ----------------------------
# Simple persistent storage using sqlitedict
# ----------------------------
# Keying scheme:
#  - user:{user_id}:meta -> dict (name, created_at)
#  - user:{user_id}:convos -> list of dicts {role, text, ts}
#  - user:{user_id}:mood -> list of {day_ts, mood, note}
#  - user:{user_id}:challenge -> dict (progress)
# ----------------------------

def ensure_user(user_id):
    key = f"user:{user_id}:meta"
    if key not in db:
        db[key] = {"created_at": time.time()}
    return db[key]

def add_convo(user_id, role, text):
    key = f"user:{user_id}:convos"
    convos = db.get(key, [])
    convos.append({"role": role, "text": text, "ts": time.time()})
    db[key] = convos[-100:]

def get_recent_convo(user_id, n=6):
    key = f"user:{user_id}:convos"
    convos = db.get(key, [])
    return convos[-n:]

def add_mood(user_id, mood_score, note=None):
    key = f"user:{user_id}:mood"
    moods = db.get(key, [])
    moods.append({"ts": time.time(), "mood": mood_score, "note": note})
    db[key] = moods[-365:]

def get_mood_history(user_id, last_n=14):
    key = f"user:{user_id}:mood"
    moods = db.get(key, [])
    return moods[-last_n:]

def set_challenge_progress(user_id, day):
    key = f"user:{user_id}:challenge"
    db[key] = {"current_day": day, "updated_at": time.time()}

def get_challenge_progress(user_id):
    key = f"user:{user_id}:challenge"
    return db.get(key, {"current_day": 0})

# ----------------------------
# Crisis detection
# ----------------------------
SUICIDE_KEYWORDS = [
    "suicide", "kill myself", "end my life", "i want to die",
    "can't live", "dont want to live", "kill myself"
]

def detect_crisis(text):
    t = text.lower()
    for k in SUICIDE_KEYWORDS:
        if k in t:
            return "suicide"
    if any(w in t for w in ["panic attack", "i'm panicking", "hyperventilating", "can't breathe"]):
        return "panic"
    if "hurt myself" in t or "self-harm" in t or "cutting" in t:
        return "selfharm"
    return None

# ----------------------------
# Utility: call LLM (OpenAI)
# ----------------------------
def call_openai_system_prompt(system, user_prompt, max_tokens=400):
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return resp.choices[0].message["content"]
    except Exception as e:
        return "Sorry — I'm having trouble connecting to the model right now. Please try again later."

# ----------------------------
# Chainlit event handlers
# ----------------------------
@cl.on_chat_start
async def start_chat(data):
    user = cl.get_client().user
    ensure_user(user.id)
    greeting = "Hi — I'm a friendly support bot for college students. You can tell me how you feel or choose an option below."
    msg = cl.Message(content=greeting)
    msg.actions = [
        cl.Action(name="mood_check", value="mood_check", label="Record Mood"),
        cl.Action(name="30_day_challenge", value="start_challenge", label="Start 30-Day Challenge"),
        cl.Action(name="resources", value="resources", label="Browse Resources"),
        cl.Action(name="talk_now", value="talk_now", label="I want to talk")
    ]
    await msg.send()

@cl.action_callback("mood_check")
async def mood_check_action():
    await cl.Message(content="On a scale of 1 (very low) to 5 (very good), how are you feeling today?").send()

@cl.action_callback("30_day_challenge")
async def start_challenge_action():
    user = cl.get_client().user
    prog = get_challenge_progress(user.id)
    day = prog.get("current_day", 0) + 1
    if day > 30:
        await cl.Message(content="You've completed the 30-day challenge — great work! Want to restart?").send()
        return
    entry = THIRTY_DAY_CHALLENGE[day-1]
    set_challenge_progress(user.id, day)
    await cl.Message(content=f"Day {day}: {entry['task']}\nAffirmation: {entry['affirmation']}").send()

@cl.action_callback("resources")
async def resources_action():
    keys = list(RESOURCE_LIBRARY.keys())
    buttons = [cl.Action(name=f"res_{k}", value=k, label=RESOURCE_LIBRARY[k].get("title", k).replace("_"," ").title()) for k in keys[:8]]
    await cl.Message(content="Here are some popular topics. Tap one to open:").send()
    await cl.Message(content="Choose a topic:", actions=buttons).send()

# generic resource actions
for res_key in list(RESOURCE_LIBRARY.keys()):
    action_name = f"res_{res_key}"
    @cl.action_callback(action_name)
    async def _res_action(value=None, res_key=res_key):
        r = RESOURCE_LIBRARY[res_key]
        summary = r.get("summary", "Short summary not available.")
        tips = r.get("tips", [])
        t = f"**{r.get('title','Topic')}**\n\n{summary}\n\nTips:\n" + "\n".join([f"- {it}" for it in tips])
        await cl.Message(content=t).send()

# Mood submission
@cl.on_message
async def main(message):
    user_obj = cl.get_client().user
    user_id = user_obj.id
    ensure_user(user_id)

    text = message.content.strip()
    add_convo(user_id, "user", text)

    # crisis detection
    crisis = detect_crisis(text)
    if crisis == "suicide":
        add_convo(user_id, "bot", "escalation")
        college_counselor = "College Counseling Center: +91-XXXXXXXXXX"
        national_hotline = "National Helpline (India): 9152987821 (example)"
        reply = textwrap.dedent(f"""
        I'm really sorry you're feeling this way. This sounds serious. Please contact someone who can help you immediately:
        • Your college counseling center: {college_counselor}
        • Local emergency services if you are in immediate danger.
        • National helpline: {national_hotline}
        
        Do you want me to connect you with steps to keep safe right now (grounding steps, breathing)?
        """).strip()
        await cl.Message(content=reply).send()
        return
    elif crisis == "panic":
        add_convo(user_id, "bot", "panic_response")
        await cl.Message(content="I hear panic. Let's do box breathing together: breathe in 4, hold 4, out 4, hold 4. Repeat 4 times. Are you in a safe place?").send()
        return
    elif crisis == "selfharm":
        add_convo(user_id, "bot", "selfharm_response")
        await cl.Message(content="I'm really sorry you're hurting. If you're in immediate danger, please contact local emergency services. Would you like grounding steps or a list of professionals nearby?").send()
        return

    # If user typed a mood score quickly (single number 1-5), treat as mood input
    if text in ["1","2","3","4","5"]:
        score = int(text)
        add_mood(user_id, score, note=None)
        await cl.Message(content=f"Got it — recorded mood {score}/5. Would you like a small activity suggestion?").send()
        return

    # Recognize quick commands
    lower = text.lower()
    if lower.startswith("/resource ") or lower.startswith("resource "):
        topic = text.split(" ",1)[1].strip()
        r = RESOURCE_LIBRARY.get(topic.replace(" ","_").lower())
        if r:
            await cl.Message(content=f"**{r.get('title')}**\n\n{r.get('summary','')}\n\nTips:\n" + "\n".join([f"- {it}" for it in r.get("tips",[])])).send()
            return
        else:
            await cl.Message(content="Sorry, I don't have that resource. Try a topic like 'stress management' or 'sleep hygiene'.").send()
            return

    # Detect scenario from triggers (simple matching)
    matched_scenario = None
    for k, s in SCENARIO_FLOWS.items():
        if any(tok in lower for tok in s.get("triggers", [])):
            matched_scenario = k
            break

    # Compose system prompt for helpful, empathetic replies
    system_prompt = (
        "You are a calm, empathetic, supportive assistant for college students. "
        "You provide short, actionable coping steps, grounding exercises, mood tracking prompts, and suggest professional help when needed. "
        "Be brief (3-6 sentences), avoid clinical diagnosis, and encourage help-seeking when risk is detected. "
        "Use inclusive, non-judgmental language."
    )
    recent = get_recent_convo(user_id, n=6)
    recent_text = "\n".join([f"{c['role']}: {c['text']}" for c in recent])
    mood_hist = get_mood_history(user_id, last_n=7)
    mood_summary = ""
    if mood_hist:
        avg = sum([m['mood'] for m in mood_hist]) / len(mood_hist)
        mood_summary = f"Recent mood average (last {len(mood_hist)}): {avg:.2f}/5."

    user_prompt = f"{mood_summary}\nRecent messages:\n{recent_text}\n\nUser said: {text}\n\nPlease respond empathetically and provide 1) short validation, 2) 2 quick coping steps, 3) ask one follow-up question or offer buttons for Mood/Resource/Escalate."

    if matched_scenario:
        scenario = SCENARIO_FLOWS[matched_scenario]
        user_prompt = user_prompt + f"\n\nUser scenario: {scenario['title']}. Provide grounding: {scenario.get('grounding')}."
    reply = call_openai_system_prompt(system_prompt, user_prompt, max_tokens=300)
    msg = cl.Message(content=reply)
    msg.actions = [
        cl.Action(name="mood_1to5", value="mood_prompt", label="Record mood (1-5)"),
        cl.Action(name="resource_quick", value="resource_quick", label="Open resources"),
        cl.Action(name="escalate", value="escalate", label="I need urgent help")
    ]
    await msg.send()
    add_convo(user_id, "bot", reply)

@cl.action_callback("mood_1to5")
async def mood_prompt_action():
    await cl.Message(content="Please type a number from 1 (very low) to 5 (very good) to record your mood.").send()

@cl.action_callback("resource_quick")
async def resource_quick_action():
    keys = list(RESOURCE_LIBRARY.keys())
    buttons = [cl.Action(name=f"res_{k}", value=k, label=RESOURCE_LIBRARY[k].get("title", k).title()) for k in keys[:6]]
    await cl.Message(content="Choose a topic:", actions=buttons).send()

@cl.action_callback("escalate")
async def escalate_action():
    user = cl.get_client().user
    college_counselor = "College Counseling Center: +91-XXXXXXXXXX"
    national_hotline = "National Helpline (India): 9152987821"
    reply = f"If you're feeling unsafe, please contact someone right now:\n• College counselor: {college_counselor}\n• National helpline: {national_hotline}\nDo you want steps to stay safe now (grounding/exercises)?"
    await cl.Message(content=reply).send()

@cl.on_message
async def admin_commands(message):
    if message.content.strip() == "/export_memory":
        out = []
        for k in db.keys():
            if k.startswith("user:"):
                out.append(f"{k}: {db[k]}")
        await cl.Message(content="Memory keys:\n" + "\n".join(out[:50])).send()

