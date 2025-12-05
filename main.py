"""
CalmSpace - AI-Powered Mental Health Support Platform for College Students
===========================================================================
Features:
- Empathetic AI conversations (10+ mental health scenarios)
- Mood tracking with history and insights
- 30-day wellness challenge
- Resource library (20+ topics)
- Crisis detection and escalation
- Guided breathing/meditation exercises
- Journal prompts
- Coping strategies (emotion-specific)
"""

import chainlit as cl
from openai import OpenAI
import os
from datetime import datetime
from typing import Optional
import random

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================================================================
# SYSTEM PROMPTS FOR DIFFERENT SCENARIOS
# ============================================================================

MAIN_SYSTEM_PROMPT = """You are CalmSpace, a warm, empathetic, and supportive mental health companion designed specifically for college students. 

Your core traits:
- Deeply empathetic and non-judgmental
- Use a warm, conversational tone (like a supportive friend who happens to be trained in mental health)
- Validate emotions before offering solutions
- Never dismiss or minimize feelings
- Use "I hear you" and "That sounds really difficult" type phrases genuinely
- Ask thoughtful follow-up questions
- Offer practical, student-relevant coping strategies
- Know when to recommend professional help

Important boundaries:
- You are NOT a replacement for professional therapy
- You cannot diagnose conditions
- For crisis situations, always provide helpline numbers
- Keep responses concise but meaningful (not walls of text)

When responding:
1. First, acknowledge and validate their feelings (1-2 sentences)
2. Reflect back what you're hearing (shows you understand)
3. Offer 1-2 relevant coping strategies or insights
4. End with a gentle question or supportive statement

Remember: Many students are experiencing these feelings for the first time away from home. Be the supportive presence they need."""

SCENARIO_PROMPTS = {
    "exam_anxiety": """The student is experiencing exam/academic anxiety. Focus on:
- Normalizing pre-exam stress
- Study-break balance
- Grounding techniques before exams
- Perspective on grades vs self-worth
- Practical study strategies""",
    
    "loneliness": """The student is feeling lonely or isolated. Focus on:
- Validating that loneliness in college is extremely common
- Small steps to connection (not overwhelming suggestions)
- Quality vs quantity of friendships
- Campus resources for meeting people
- Self-compassion during lonely times""",
    
    "homesickness": """The student is homesick. Focus on:
- Acknowledging this as a natural transition
- Creating comfort rituals
- Staying connected with home while building new connections
- Making their space feel like home
- Timeline perspective (it gets easier)""",
    
    "burnout": """The student is experiencing burnout. Focus on:
- Recognizing burnout signs
- Permission to rest (not lazy)
- Setting boundaries
- Breaking the cycle
- Sustainable habits""",
    
    "imposter_syndrome": """The student feels like they don't belong or aren't good enough. Focus on:
- How common this is (especially for high achievers)
- Evidence vs feelings
- Reframing "fraud" thoughts
- Celebrating small wins
- Everyone struggles (they just don't show it)""",
    
    "relationship_issues": """The student is having relationship problems (romantic, friendship, family). Focus on:
- Listening without taking sides
- Healthy communication strategies
- Boundaries in relationships
- Self-care during conflict
- When to seek help""",
    
    "depression_feelings": """The student seems to be experiencing depressive feelings. Focus on:
- Taking their feelings seriously
- Small, manageable steps
- The importance of professional support
- Daily functioning strategies
- Hope and recovery perspective""",
    
    "sleep_issues": """The student has sleep problems. Focus on:
- Sleep hygiene basics
- College-specific challenges (roommates, late nights)
- Anxiety-sleep connection
- Practical tips
- When sleep issues need professional attention""",
    
    "financial_stress": """The student is stressed about money. Focus on:
- Validating financial stress as real stress
- Campus resources (financial aid, food pantries)
- Budgeting without judgment
- Part-time work balance
- Asking for help is okay""",
    
    "future_anxiety": """The student is anxious about their future/career. Focus on:
- Uncertainty is normal
- Present moment focus
- Career exploration as a process
- Comparison trap
- Small steps forward"""
}

# ============================================================================
# RESOURCE LIBRARY - 20+ Mental Health Topics
# ============================================================================

RESOURCE_LIBRARY = {
    "stress management": {
        "title": "📚 Stress Management",
        "content": """**Understanding & Managing Stress**

Stress is your body's response to demands. Some stress is normal, but chronic stress affects your health.

**Signs of Stress:**
• Racing thoughts or difficulty concentrating
• Muscle tension, headaches
• Changes in sleep or appetite
• Irritability or mood swings
• Procrastination or avoidance

**Quick Stress Busters:**
1. **4-7-8 Breathing**: Inhale 4 sec, hold 7 sec, exhale 8 sec
2. **5-minute walk**: Movement releases tension
3. **Brain dump**: Write everything on your mind
4. **Cold water on wrists**: Activates calming response
5. **Progressive muscle relaxation**: Tense and release each muscle group

**Long-term Strategies:**
• Regular exercise (even 20 min helps)
• Consistent sleep schedule
• Time blocking for work and rest
• Saying "no" to overcommitment
• Weekly planning sessions"""
    },
    
    "anxiety": {
        "title": "💭 Understanding Anxiety",
        "content": """**Anxiety in College Students**

Anxiety is the most common mental health concern for college students. You're not alone.

**Types You Might Experience:**
• **Generalized anxiety**: Constant worry about many things
• **Social anxiety**: Fear of judgment in social situations
• **Performance anxiety**: Stress about exams, presentations
• **Panic attacks**: Sudden intense fear with physical symptoms

**Grounding Techniques (5-4-3-2-1):**
• 5 things you can SEE
• 4 things you can TOUCH
• 3 things you can HEAR
• 2 things you can SMELL
• 1 thing you can TASTE

**When to Seek Help:**
• Anxiety interferes with daily activities
• You avoid situations due to fear
• Physical symptoms are frequent
• You're using substances to cope"""
    },
    
    "depression": {
        "title": "🌧️ Signs of Depression",
        "content": """**Recognizing Depression**

Depression is more than sadness—it's a persistent condition that affects how you think, feel, and function.

**Warning Signs:**
• Persistent sad, empty, or hopeless feelings
• Loss of interest in activities you used to enjoy
• Changes in appetite or weight
• Sleeping too much or too little
• Fatigue or loss of energy
• Difficulty concentrating or making decisions
• Feelings of worthlessness or excessive guilt
• Thoughts of death or suicide

**What Helps:**
• Maintain routines (even basic ones)
• Gentle movement and sunlight
• Connect with one trusted person
• Professional support (therapy, counseling)
• Sometimes medication is helpful

**Important:** Depression is treatable. Reaching out is a sign of strength, not weakness."""
    },
    
    "sleep": {
        "title": "😴 Sleep Hygiene",
        "content": """**Better Sleep for Students**

College schedules make good sleep challenging, but sleep affects everything—mood, memory, grades, and health.

**Sleep Hygiene Basics:**
1. **Consistent schedule**: Same bedtime/wake time (even weekends)
2. **Screen curfew**: No phones/laptops 1 hour before bed
3. **Cool, dark room**: 65-68°F is optimal
4. **Caffeine cutoff**: None after 2 PM
5. **Bed = sleep only**: Don't study in bed

**Can't Sleep?**
• Get up after 20 minutes of trying
• Do something boring in dim light
• Return when sleepy
• Don't check the time

**College-Specific Tips:**
• White noise for noisy dorms
• Eye mask if roommate has different schedule
• Communicate boundaries with roommates
• Naps before 3 PM, under 30 minutes"""
    },
    
    "exam anxiety": {
        "title": "📝 Exam Anxiety & Preparation",
        "content": """**Managing Exam Stress**

Some anxiety before exams is normal and can even help performance. Too much anxiety hurts it.

**Before the Exam:**
• Start early—cramming increases anxiety
• Break material into chunks
• Use active recall (test yourself)
• Teach concepts to someone else
• Get enough sleep (memory consolidation)

**Night Before:**
• Light review only (no new material)
• Prepare everything you need
• Relaxing activity before bed
• Trust your preparation

**During the Exam:**
• Read all instructions first
• Start with questions you know
• Skip and return to hard ones
• Breathe if you feel panicky
• Don't compare pace with others

**If You Blank Out:**
• Close your eyes, breathe deeply
• Start writing anything related
• Move to another question
• It will come back"""
    },
    
    "loneliness": {
        "title": "🤝 Loneliness & Building Connections",
        "content": """**Feeling Lonely at College**

Loneliness is incredibly common in college, even when surrounded by people. Social media makes it worse by showing everyone else's highlight reels.

**Why It's Common:**
• New environment, no established friendships
• Everyone seems to have friends already (they don't)
• Harder to make friends than in high school
• Quality connections take time

**Small Steps to Connect:**
1. Say hi to someone in class
2. Join ONE club or group
3. Study in public spaces
4. Accept invitations (even when tired)
5. Be the one who initiates

**Quality Over Quantity:**
• One genuine friend > many acquaintances
• Deep conversations > surface chat
• Consistent contact > constant contact

**Be Patient:**
It takes 50+ hours of interaction to form a friendship. Give it time."""
    },
    
    "homesickness": {
        "title": "🏠 Dealing with Homesickness",
        "content": """**Missing Home**

Homesickness is grief for your old life while adjusting to a new one. It's completely normal.

**What Helps:**
• **Stay connected**: Regular calls/texts with family
• **Bring comfort items**: Photos, favorite blanket, familiar snacks
• **Create new routines**: Sunday morning coffee ritual, etc.
• **Make your space yours**: Decorate, organize, nest
• **Get involved**: Campus activities give purpose

**What Doesn't Help:**
• Going home every weekend (prevents adjustment)
• Isolating in your room
• Constant comparison to home
• Refusing to try new things

**Timeline:**
• Weeks 1-3: Often the hardest
• Month 2-3: Starts improving
• End of semester: New normal forms

It does get better. Give yourself grace during the transition."""
    },
    
    "imposter syndrome": {
        "title": "🎭 Imposter Syndrome",
        "content": """**Feeling Like a Fraud**

Imposter syndrome: believing you don't deserve your success and will be "found out" as incompetent.

**Signs:**
• Attributing success to luck, not skill
• Downplaying achievements
• Fear of being exposed
• Overworking to prove worth
• Difficulty accepting praise

**Reality Check:**
• 70% of people experience this
• High achievers feel it MORE
• Your acceptance wasn't a mistake
• Others struggle too (they hide it)

**Reframing Strategies:**
1. Keep a "wins" file of accomplishments
2. When you think "I got lucky," add "AND I worked hard"
3. Talk to peers—they feel it too
4. Mentor someone newer (you DO know things)
5. "I'm learning" not "I'm failing"

**Remember:** You don't have to feel confident to be competent."""
    },
    
    "burnout": {
        "title": "🔥 Academic Burnout",
        "content": """**Recognizing & Recovering from Burnout**

Burnout isn't laziness—it's exhaustion from prolonged stress without adequate recovery.

**Signs of Burnout:**
• Exhaustion that sleep doesn't fix
• Cynicism about school/activities
• Feeling ineffective despite effort
• Emotional numbness
• Physical symptoms (headaches, illness)

**Recovery Steps:**
1. **Acknowledge it**: This is real, not weakness
2. **Reduce load**: Drop what you can (even temporarily)
3. **Rest without guilt**: Recovery is productive
4. **Set boundaries**: Learn to say no
5. **Seek support**: Talk to advisor, counselor

**Prevention:**
• Build breaks into your schedule
• Protect sleep and exercise
• Have non-academic interests
• Regular check-ins with yourself
• Sustainable pace > sprint

**The "hustle culture" lie:** Burning out doesn't mean you worked hard. It means you worked unsustainably."""
    },
    
    "relationships": {
        "title": "💕 Healthy Relationships",
        "content": """**Building & Maintaining Healthy Relationships**

College relationships (romantic, friendships, roommates) can be wonderful and challenging.

**Signs of Healthy Relationships:**
• Mutual respect and trust
• Open communication
• Supporting each other's goals
• Maintaining individual identity
• Healthy conflict resolution
• Feeling safe to be yourself

**Red Flags:**
• Controlling behavior
• Constant criticism
• Isolation from friends/family
• Jealousy presented as "caring"
• Making you feel bad about yourself
• Physical intimidation

**Communication Tips:**
• Use "I feel" statements
• Listen to understand, not respond
• Address issues early
• It's okay to need space
• Apologize meaningfully

**Remember:** You deserve relationships that add to your life, not drain it."""
    },
    
    "time management": {
        "title": "⏰ Time Management",
        "content": """**Managing Time in College**

College gives you more freedom and less structure—this is both exciting and challenging.

**Common Traps:**
• Overcommitting
• Underestimating task time
• Procrastination spirals
• All-nighters (they don't work)
• No buffer time

**Effective Strategies:**
1. **Time blocking**: Schedule specific tasks
2. **2-minute rule**: If it takes <2 min, do it now
3. **Pomodoro**: 25 min work, 5 min break
4. **Sunday planning**: Map out the week
5. **Buffer time**: Things take longer than expected

**Prioritization:**
• **Urgent + Important**: Do first
• **Important + Not urgent**: Schedule it
• **Urgent + Not important**: Delegate/minimize
• **Neither**: Eliminate

**Energy Management:**
Do hard tasks when you're most alert. Save easy tasks for low-energy times."""
    },
    
    "mindfulness": {
        "title": "🧘 Mindfulness Basics",
        "content": """**Introduction to Mindfulness**

Mindfulness: paying attention to the present moment without judgment. Simple concept, powerful practice.

**Benefits:**
• Reduced anxiety and stress
• Improved focus
• Better emotional regulation
• Decreased rumination
• Better sleep

**Simple Practices:**
1. **Mindful breathing**: Focus on breath for 1 minute
2. **Body scan**: Notice sensations head to toe
3. **Mindful eating**: Really taste your food
4. **Walking meditation**: Feel each step
5. **STOP technique**: Stop, Take a breath, Observe, Proceed

**Common Misconceptions:**
• You DON'T need to clear your mind
• Thoughts are normal—notice and return to breath
• 5 minutes counts
• You can't do it "wrong"
• It's a practice, not perfection

**Start Small:**
2 minutes daily > 20 minutes once a week. Consistency matters more than duration."""
    },
    
    "self compassion": {
        "title": "💚 Self-Compassion",
        "content": """**Being Kind to Yourself**

Self-compassion: treating yourself with the same kindness you'd offer a friend.

**Three Components:**
1. **Self-kindness** vs self-judgment
2. **Common humanity** (everyone struggles) vs isolation
3. **Mindfulness** vs over-identification with pain

**Self-Compassion Break:**
When struggling, say to yourself:
• "This is a moment of suffering" (mindfulness)
• "Suffering is part of life" (common humanity)
• "May I be kind to myself" (self-kindness)

**Reframing Self-Talk:**
• Instead of: "I'm so stupid"
• Try: "I'm struggling, and that's okay"

• Instead of: "Everyone else has it together"
• Try: "Everyone struggles with something"

**Why It Matters:**
Self-compassion increases resilience, motivation, and wellbeing. Self-criticism does the opposite."""
    },
    
    "panic attacks": {
        "title": "😰 Managing Panic Attacks",
        "content": """**Understanding Panic Attacks**

A panic attack is a sudden surge of intense fear with physical symptoms. They're terrifying but not dangerous.

**Symptoms:**
• Racing heart
• Shortness of breath
• Chest tightness
• Dizziness
• Tingling sensations
• Feeling of unreality
• Fear of dying or losing control

**During a Panic Attack:**
1. **Remember**: This will pass (usually 10-20 min)
2. **Breathe slowly**: In for 4, out for 6
3. **Ground yourself**: 5-4-3-2-1 technique
4. **Don't fight it**: Resistance increases panic
5. **Stay present**: "I am safe. This is temporary."

**After:**
• Be gentle with yourself
• Rest if needed
• Reflect on triggers
• Consider professional support if recurring

**Prevention:**
Regular stress management, sleep, exercise, and limiting caffeine can reduce frequency."""
    },
    
    "substance use": {
        "title": "🍺 Substance Use Awareness",
        "content": """**Making Informed Choices**

College often involves exposure to alcohol and other substances. Here's what to know.

**Alcohol Awareness:**
• Standard drink = 12oz beer = 5oz wine = 1.5oz liquor
• Your brain is still developing until ~25
• "Everyone drinks" is a myth (many don't)
• Hangovers affect next-day performance significantly

**Warning Signs of Problem Use:**
• Using to cope with stress/emotions
• Blacking out
• Needing more to feel effects
• Neglecting responsibilities
• Others expressing concern

**Harm Reduction:**
• Eat before drinking
• Alternate with water
• Never leave drinks unattended
• Have a buddy system
• Know how you're getting home

**If You're Concerned:**
• Campus health services
• SAMHSA Helpline: 1-800-662-4357
• It's okay to ask for help"""
    },
    
    "grief": {
        "title": "🕊️ Grief & Loss",
        "content": """**Navigating Grief**

Loss comes in many forms: death, breakups, friendships ending, leaving home, loss of identity or dreams.

**Grief Isn't Linear:**
The "stages" (denial, anger, bargaining, depression, acceptance) aren't steps. You may cycle through them randomly.

**What's Normal:**
• Waves of intense emotion
• Feeling okay, then suddenly not
• Physical symptoms (fatigue, appetite changes)
• Difficulty concentrating
• Questioning everything

**What Helps:**
• Let yourself feel (don't "should" yourself)
• Talk to someone who listens without fixing
• Maintain basic routines
• Be patient with yourself
• Create rituals of remembrance

**Grief While in College:**
It's hard to grieve while keeping up with classes. Talk to professors—most will understand. Use campus counseling."""
    },
    
    "social anxiety": {
        "title": "😓 Social Anxiety",
        "content": """**Managing Social Anxiety**

Social anxiety: intense fear of social situations due to fear of judgment or embarrassment.

**Common Triggers:**
• Meeting new people
• Speaking in class
• Eating in public
• Group projects
• Parties/social events

**What's Happening:**
Your brain overestimates threat and underestimates your ability to cope. Others notice your anxiety far less than you think.

**Coping Strategies:**
1. **Challenge thoughts**: "What's the evidence I'll be judged?"
2. **Focus outward**: Listen to others vs. monitoring yourself
3. **Gradual exposure**: Start with low-stakes situations
4. **Prepare**: Having topics ready can help
5. **Self-compassion**: Everyone feels awkward sometimes

**Helpful Reframes:**
• "I don't have to be perfect"
• "Awkward moments pass"
• "Most people are focused on themselves"
• "I'm allowed to be quiet"

**When to Seek Help:**
If social anxiety significantly limits your life, therapy (especially CBT) is very effective."""
    },
    
    "perfectionism": {
        "title": "🎯 Perfectionism",
        "content": """**When High Standards Hurt**

Perfectionism: setting extremely high standards and being highly self-critical when you don't meet them.

**Healthy Striving vs. Perfectionism:**
• Healthy: "I want to do well"
• Perfectionism: "I must be perfect or I'm a failure"

**Signs:**
• All-or-nothing thinking
• Procrastination (fear of imperfection)
• Difficulty celebrating achievements
• Harsh self-criticism
• Never feeling "good enough"
• Avoiding challenges (might fail)

**Costs of Perfectionism:**
• Anxiety and depression
• Burnout
• Actually worse performance
• Missed opportunities
• Relationship strain

**Recovery Strategies:**
1. Set "good enough" goals
2. Practice imperfection deliberately
3. Notice and challenge all-or-nothing thoughts
4. Celebrate effort, not just outcomes
5. Ask: "Will this matter in 5 years?"

**Remember:** Done is better than perfect. Progress over perfection."""
    },
    
    "financial stress": {
        "title": "💰 Financial Stress",
        "content": """**Managing Money Stress**

Financial stress is real stress. It affects mental health, academic performance, and relationships.

**Common Concerns:**
• Tuition and loans
• Daily expenses
• Work-school balance
• Comparing to others
• Family expectations

**Practical Steps:**
1. **Know your numbers**: Track spending for one week
2. **Basic budget**: Needs, wants, savings
3. **Use campus resources**: Food pantries, emergency funds
4. **Financial aid office**: They can help more than you think
5. **Student discounts**: Always ask

**Part-Time Work Balance:**
• 15-20 hours/week generally manageable
• On-campus jobs often more flexible
• Work-study can be helpful

**If You're Struggling:**
• Talk to financial aid BEFORE a crisis
• Many schools have emergency funds
• Food insecurity support exists
• You're not alone in this

**Mindset:** Financial stress doesn't define your worth or future."""
    },
    
    "seeking help": {
        "title": "🆘 When & How to Seek Help",
        "content": """**Reaching Out for Support**

Asking for help is a strength, not a weakness. Knowing when and how to seek help is an important life skill.

**Signs You Should Talk to Someone:**
• Feelings that won't go away
• Difficulty functioning (classes, relationships, self-care)
• Using substances to cope
• Thoughts of self-harm
• Feeling hopeless
• Significant changes in sleep, appetite, energy

**Campus Resources:**
• **Counseling Center**: Usually free for students
• **Health Services**: Can address physical symptoms
• **Dean of Students**: Academic accommodations
• **RA/Resident Advisor**: First point of contact

**What to Expect:**
• Initial assessment/intake
• You'll discuss what's bringing you in
• Together you'll make a plan
• Confidential (with some legal exceptions)

**If the Wait is Long:**
• Ask about crisis appointments
• Group therapy often has shorter waits
• Online resources as supplement
• Community mental health centers

**Remember:** You don't have to be in crisis to seek help. Early support prevents bigger problems."""
    }
}

# ============================================================================
# 30-DAY WELLNESS CHALLENGE
# ============================================================================

WELLNESS_CHALLENGES = [
    {"day": 1, "title": "Gratitude Start", "task": "Write down 3 things you're grateful for today. They can be small—a warm coffee, a text from a friend, sunshine.", "category": "mindfulness"},
    {"day": 2, "title": "Hydration Check", "task": "Drink 8 glasses of water today. Set reminders if needed. Notice how your body feels.", "category": "physical"},
    {"day": 3, "title": "Digital Sunset", "task": "Put your phone away 30 minutes before bed. Read, stretch, or just be.", "category": "sleep"},
    {"day": 4, "title": "Reach Out", "task": "Send a message to someone you haven't talked to in a while. Just say hi.", "category": "connection"},
    {"day": 5, "title": "Movement Joy", "task": "Do 10 minutes of movement you enjoy—dance, walk, stretch, anything.", "category": "physical"},
    {"day": 6, "title": "Mindful Meal", "task": "Eat one meal without screens. Notice the flavors, textures, and how your body feels.", "category": "mindfulness"},
    {"day": 7, "title": "Reflection", "task": "Journal for 5 minutes: How has your week been? What do you need more of?", "category": "reflection"},
    {"day": 8, "title": "Nature Break", "task": "Spend 15 minutes outside. No phone. Just notice your surroundings.", "category": "mindfulness"},
    {"day": 9, "title": "Boundary Practice", "task": "Say 'no' to one thing today that doesn't serve you. Notice how it feels.", "category": "self-care"},
    {"day": 10, "title": "Sleep Sanctuary", "task": "Make your sleep space more comfortable—tidy up, adjust lighting, fresh sheets.", "category": "sleep"},
    {"day": 11, "title": "Compliment Day", "task": "Give three genuine compliments today—to others or yourself.", "category": "connection"},
    {"day": 12, "title": "Breathing Space", "task": "Practice 4-7-8 breathing (inhale 4, hold 7, exhale 8) three times today.", "category": "mindfulness"},
    {"day": 13, "title": "Nourish", "task": "Eat one extra serving of fruits or vegetables today.", "category": "physical"},
    {"day": 14, "title": "Weekly Check-in", "task": "Rate your week 1-10. What worked? What needs adjustment?", "category": "reflection"},
    {"day": 15, "title": "Act of Kindness", "task": "Do something kind for someone else—hold a door, buy a coffee, send encouragement.", "category": "connection"},
    {"day": 16, "title": "Creative Expression", "task": "Spend 15 minutes on something creative—draw, write, play music, craft.", "category": "self-care"},
    {"day": 17, "title": "Body Scan", "task": "Do a 5-minute body scan meditation. Notice areas of tension without judgment.", "category": "mindfulness"},
    {"day": 18, "title": "Social Media Fast", "task": "Take a break from social media for the entire day. Notice how you feel.", "category": "self-care"},
    {"day": 19, "title": "Learn Something", "task": "Spend 20 minutes learning something new just for fun—not for class.", "category": "growth"},
    {"day": 20, "title": "Declutter", "task": "Organize one small space (desk, drawer, bag). External order helps internal calm.", "category": "self-care"},
    {"day": 21, "title": "Three-Week Reflection", "task": "You're 3 weeks in! Write about what changes you've noticed.", "category": "reflection"},
    {"day": 22, "title": "Morning Mindfulness", "task": "Before checking your phone, take 5 deep breaths and set an intention for the day.", "category": "mindfulness"},
    {"day": 23, "title": "Movement Challenge", "task": "Take the stairs all day, or do 20 squats every few hours.", "category": "physical"},
    {"day": 24, "title": "Forgiveness", "task": "Write about something you need to forgive—yourself or someone else. You don't have to share it.", "category": "reflection"},
    {"day": 25, "title": "Connection Deep Dive", "task": "Have a meaningful conversation with someone. Ask real questions. Listen fully.", "category": "connection"},
    {"day": 26, "title": "Joy List", "task": "Make a list of 10 things that bring you joy. Do at least one today.", "category": "self-care"},
    {"day": 27, "title": "Affirmation Day", "task": "Choose 3 affirmations and repeat them throughout the day. Write them somewhere visible.", "category": "mindfulness"},
    {"day": 28, "title": "Future Self Letter", "task": "Write a letter to yourself 6 months from now. What do you hope for?", "category": "reflection"},
    {"day": 29, "title": "Celebration", "task": "Celebrate yourself today. You've almost completed 30 days! Do something you enjoy.", "category": "self-care"},
    {"day": 30, "title": "Integration", "task": "Reflect: Which practices will you continue? What have you learned about yourself?", "category": "reflection"}
]

DAILY_AFFIRMATIONS = [
    "I am worthy of rest and recovery.",
    "My feelings are valid, even when they're difficult.",
    "I am doing the best I can with what I have.",
    "It's okay to ask for help.",
    "I am more than my grades or productivity.",
    "This difficult moment will pass.",
    "I deserve compassion, especially from myself.",
    "Progress, not perfection.",
    "I am enough, exactly as I am.",
    "My mental health matters.",
    "I can handle challenges one step at a time.",
    "It's okay to not have everything figured out.",
    "I am learning and growing every day.",
    "My worth is not determined by others' opinions.",
    "I give myself permission to take breaks.",
    "Struggling doesn't mean failing.",
    "I am resilient.",
    "Today, I choose to be kind to myself.",
    "I trust my ability to get through this.",
    "I am allowed to set boundaries."
]

# ============================================================================
# CRISIS RESOURCES
# ============================================================================

CRISIS_RESOURCES = """
🚨 **Crisis Resources**

If you're in immediate danger, please call emergency services (911 in US).

**24/7 Crisis Helplines:**

🇮🇳 **India:**
• AASRA: 9820466726
• iCall: 9152987821
• Vandrevala Foundation: 1860-2662-345

🇺🇸 **USA:**
• 988 Suicide & Crisis Lifeline: Call/Text **988**
• Crisis Text Line: Text **HOME** to **741741**

🇬🇧 **UK:**
• Samaritans: 116 123
• SHOUT: Text **SHOUT** to **85258**

🌍 **International:**
• International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/

**Remember:** Reaching out is brave. You matter. Help is available. 💙
"""

CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "want to die", "better off dead",
    "self harm", "self-harm", "hurt myself", "cutting", "overdose",
    "can't go on", "no point living", "end it all", "take my life",
    "don't want to be here", "wish i was dead", "not worth living"
]

# ============================================================================
# GUIDED EXERCISES
# ============================================================================

BREATHING_EXERCISES = {
    "box": {
        "name": "Box Breathing",
        "content": """
**Box Breathing Exercise** 📦

Used by Navy SEALs to stay calm under pressure.

1. **Inhale** slowly for 4 seconds
2. **Hold** your breath for 4 seconds
3. **Exhale** slowly for 4 seconds
4. **Hold** empty for 4 seconds

Repeat 4 times.

This activates your parasympathetic nervous system and reduces stress hormones.

How do you feel? 💙"""
    },
    "478": {
        "name": "4-7-8 Breathing",
        "content": """
**4-7-8 Breathing Exercise** 🌬️

Dr. Andrew Weil's relaxation technique.

1. **Exhale** completely through your mouth
2. **Inhale** quietly through your nose for **4 seconds**
3. **Hold** your breath for **7 seconds**
4. **Exhale** completely through your mouth for **8 seconds**

Repeat 4 times.

This is especially good for anxiety and falling asleep.

How are you feeling now? 💙"""
    },
    "grounding": {
        "name": "5-4-3-2-1 Grounding",
        "content": """
**5-4-3-2-1 Grounding Exercise** 🌳

Brings you back to the present moment.

Look around and find:

👀 **5 things you can SEE**
(Name them out loud or in your mind)

✋ **4 things you can TOUCH**
(Feel their texture)

👂 **3 things you can HEAR**
(Near or far away)

👃 **2 things you can SMELL**
(Or 2 scents you like)

👅 **1 thing you can TASTE**
(Or imagine a favorite taste)

Take a deep breath. You are here. You are safe.

How do you feel now? 💙"""
    }
}

MEDITATION_SCRIPTS = {
    "calm": {
        "name": "2-Minute Calm",
        "content": """
**2-Minute Calm** 🧘

Find a comfortable position. Close your eyes if that feels okay.

Take a deep breath in... and slowly let it out.

Notice your feet on the ground. Feel the support beneath you.

Breathe in calm... breathe out tension.

You don't need to change anything right now. Just be here.

One more deep breath... and when you're ready, gently open your eyes.

You can return to this moment whenever you need it. 💙"""
    },
    "body scan": {
        "name": "Quick Body Scan",
        "content": """
**Quick Body Scan** 🌟

Close your eyes. Take three deep breaths.

**Head**: Notice any tension in your forehead, jaw, or neck. Soften.

**Shoulders**: Let them drop away from your ears. Release.

**Arms & Hands**: Unclench your fists. Let your hands be heavy.

**Chest**: Notice your breath. No need to change it.

**Stomach**: Release any holding or tightness.

**Legs & Feet**: Feel them supported by the ground.

Take one more breath. You are whole. You are here. 💙"""
    },
    "self compassion": {
        "name": "Self-Compassion Meditation",
        "content": """
**Self-Compassion Meditation** 💚

Place your hand on your heart. Feel its warmth.

Repeat silently or aloud:

*"This is a moment of difficulty."*
(Acknowledge what you're feeling)

*"Difficulty is part of being human."*
(You're not alone in this)

*"May I be kind to myself."*
(You deserve compassion)

*"May I give myself the compassion I need."*
(Let it in)

Breathe. You are worthy of kindness—especially your own. 💚"""
    }
}

# ============================================================================
# COPING STRATEGIES (Emotion-Specific)
# ============================================================================

COPING_STRATEGIES = {
    "anxiety": {
        "title": "Coping with Anxiety",
        "strategies": [
            "Try the 5-4-3-2-1 grounding technique",
            "Do box breathing (4-4-4-4 pattern)",
            "Go for a short walk",
            "Write down your worries and challenge each one",
            "Call a friend or family member",
            "Limit caffeine intake",
            "Progressive muscle relaxation"
        ]
    },
    "sadness": {
        "title": "Coping with Sadness",
        "strategies": [
            "Let yourself feel it—crying is okay",
            "Reach out to someone you trust",
            "Do one small act of self-care",
            "Listen to music that matches or shifts your mood",
            "Write in a journal without judgment",
            "Get some sunlight or fresh air",
            "Be gentle with yourself"
        ]
    },
    "anger": {
        "title": "Coping with Anger",
        "strategies": [
            "Remove yourself from the situation if possible",
            "Physical exercise or movement",
            "Write an angry letter you won't send",
            "Use cold water on your face or wrists",
            "Count to 10 before responding",
            "Deep breathing exercises",
            "Identify the underlying emotion"
        ]
    },
    "overwhelm": {
        "title": "Coping with Overwhelm",
        "strategies": [
            "Brain dump everything on your mind",
            "Pick ONE thing to focus on",
            "Break tasks into smaller steps",
            "It's okay to ask for an extension",
            "5 minutes of deep breathing",
            "Step away from the situation briefly",
            "Ask for help"
        ]
    },
    "general": {
        "title": "General Coping Strategies",
        "strategies": [
            "Movement—even a short walk helps",
            "Deep breathing exercises",
            "Talk to someone you trust",
            "Write it out in a journal",
            "Do something with your hands (draw, craft, cook)",
            "Change your environment",
            "Practice self-compassion",
            "Limit social media",
            "Get outside in nature",
            "Progressive muscle relaxation"
        ]
    }
}

# ============================================================================
# USER SESSION MANAGEMENT
# ============================================================================

user_sessions = {}

def get_user_session():
    """Get or create user session data."""
    session_id = cl.user_session.get("id", "default")
    if session_id not in user_sessions:
        user_sessions[session_id] = {
            "mood_history": [],
            "conversation_history": [],
            "challenge_day": 1,
            "challenge_started": None
        }
    return user_sessions[session_id]


def add_to_conversation(role: str, content: str):
    """Add message to conversation history with limit."""
    session = get_user_session()
    session["conversation_history"].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })
    # Keep last 20 messages for context
    session["conversation_history"] = session["conversation_history"][-20:]


def log_mood(mood: str, intensity: int):
    """Log a mood entry."""
    session = get_user_session()
    session["mood_history"].append({
        "mood": mood,
        "intensity": intensity,
        "timestamp": datetime.now().isoformat()
    })


# ============================================================================
# AI RESPONSE FUNCTIONS
# ============================================================================

def detect_scenario(message: str) -> Optional[str]:
    """Detect which mental health scenario the message relates to."""
    message_lower = message.lower()
    
    scenario_keywords = {
        "exam_anxiety": ["exam", "test", "finals", "midterm", "grade", "gpa", "study", "fail class"],
        "loneliness": ["lonely", "alone", "no friends", "isolated", "left out", "nobody likes"],
        "homesickness": ["miss home", "homesick", "miss my family", "miss my mom", "miss my dad", "far from home"],
        "burnout": ["burnout", "burned out", "exhausted", "tired of everything", "can't keep up", "overwhelmed"],
        "imposter_syndrome": ["imposter", "don't belong", "fraud", "not smart enough", "everyone else is better", "mistake admitting me"],
        "relationship_issues": ["relationship", "boyfriend", "girlfriend", "partner", "breakup", "broke up", "fight with", "roommate problem"],
        "depression_feelings": ["depressed", "depression", "hopeless", "empty", "numb", "don't care anymore", "what's the point"],
        "sleep_issues": ["can't sleep", "insomnia", "sleep", "tired", "exhausted", "nightmares", "sleeping too much"],
        "financial_stress": ["money", "afford", "broke", "debt", "loan", "financial", "pay for", "expensive"],
        "future_anxiety": ["future", "career", "job", "after graduation", "what am i doing", "life after college", "don't know what to do"]
    }
    
    for scenario, keywords in scenario_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            return scenario
    
    return None


def check_crisis(message: str) -> bool:
    """Check if message contains crisis indicators."""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in CRISIS_KEYWORDS)


async def get_ai_response(user_message: str, scenario: Optional[str] = None) -> str:
    """Get AI response with appropriate context."""
    session = get_user_session()
    
    # Build conversation context
    messages = [{"role": "system", "content": MAIN_SYSTEM_PROMPT}]
    
    # Add scenario-specific guidance if detected
    if scenario and scenario in SCENARIO_PROMPTS:
        messages.append({
            "role": "system", 
            "content": f"Context: {SCENARIO_PROMPTS[scenario]}"
        })
    
    # Add recent conversation history
    for msg in session["conversation_history"][-10:]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    # Add current message
    messages.append({"role": "user", "content": user_message})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "I'm having trouble connecting right now. Please try again in a moment. If you're in crisis, please type 'crisis' for helpline numbers. 💙"


# ============================================================================
# COMMAND HANDLERS
# ============================================================================

def get_menu() -> str:
    """Return the main menu."""
    return """
**🌿 CalmSpace Menu**

Here's what I can help you with:

**💬 Just Chat** — Tell me how you're feeling
**📊 mood** — Track and view your mood
**🌱 challenge** — Daily wellness challenge
**📚 resources** — Mental health topic library
**🧘 breathe** — Guided breathing exercises
**🧘 meditate** — Quick meditation scripts
**📝 journal** — Journaling prompts
**💪 coping** — Coping strategies
**🆘 crisis** — Crisis resources

Just type the command or tell me what's on your mind. I'm here to listen. 💙
"""


def get_resource_menu() -> str:
    """Return the resource library menu."""
    topics = list(RESOURCE_LIBRARY.keys())
    menu = "**📚 Resource Library**\n\nChoose a topic to learn more:\n\n"
    
    for i, topic in enumerate(topics, 1):
        title = RESOURCE_LIBRARY[topic]["title"]
        menu += f"{i}. {title}\n"
    
    menu += "\nType the topic name (e.g., 'anxiety') or number to view."
    return menu


def get_resource(query: str) -> Optional[str]:
    """Get a specific resource by name or number."""
    query_lower = query.lower().strip()
    topics = list(RESOURCE_LIBRARY.keys())
    
    # Check if it's a number
    try:
        num = int(query_lower)
        if 1 <= num <= len(topics):
            topic = topics[num - 1]
            return RESOURCE_LIBRARY[topic]["content"]
    except ValueError:
        pass
    
    # Check by name (partial match)
    for key, value in RESOURCE_LIBRARY.items():
        if query_lower in key.lower() or query_lower in value["title"].lower():
            return value["content"]
    
    return None


def get_wellness_challenge(day: int = None) -> str:
    """Get the wellness challenge for a specific day."""
    session = get_user_session()
    
    if session["challenge_started"] is None:
        session["challenge_started"] = datetime.now().isoformat()
        session["challenge_day"] = 1
    
    if day is None:
        day = session["challenge_day"]
    
    if day < 1 or day > 30:
        return "The 30-day challenge has days 1-30. Which day would you like to see? Type 'challenge [number]'"
    
    challenge = WELLNESS_CHALLENGES[day - 1]
    affirmation = random.choice(DAILY_AFFIRMATIONS)
    
    return f"""
**🌱 Day {day} of 30: {challenge['title']}**

*Category: {challenge['category'].title()}*

**Today's Challenge:**
{challenge['task']}

**Daily Affirmation:**
*"{affirmation}"*

---
Type **'next challenge'** for tomorrow's challenge.
Type **'challenge [number]'** to see a specific day.
"""


def get_journal_prompts() -> str:
    """Generate journal prompts."""
    prompts = [
        "What emotion have you felt most strongly today? Where did you feel it in your body?",
        "What's one thing you're proud of yourself for recently, no matter how small?",
        "If you could tell your past self one thing, what would it be?",
        "What does self-care look like for you today?",
        "What's weighing on your mind? Write it out without judgment.",
        "Describe a moment this week when you felt at peace.",
        "What boundaries do you need to set or reinforce?",
        "What are you grateful for today? What's challenging?",
        "How are you really doing? Not the polite answer—the real one.",
        "What do you need to hear right now? Write it to yourself."
    ]
    
    selected = random.sample(prompts, 3)
    
    return f"""
**📝 Journal Prompts**

Take a few minutes to reflect on one or more of these:

1. {selected[0]}

2. {selected[1]}

3. {selected[2]}

*There's no right or wrong way to journal. Just let the words flow.* 💙
"""


def get_coping_strategies(emotion: str = None) -> str:
    """Get coping strategies, optionally for a specific emotion."""
    if emotion and emotion.lower() in COPING_STRATEGIES:
        data = COPING_STRATEGIES[emotion.lower()]
    else:
        data = COPING_STRATEGIES["general"]
    
    response = f"**💪 {data['title']}**\n\n"
    for i, strategy in enumerate(data['strategies'], 1):
        response += f"{i}. {strategy}\n"
    
    if emotion is None:
        response += "\nFor specific strategies, type: **coping anxiety**, **coping sadness**, **coping anger**, or **coping overwhelm**"
    
    return response


def get_breathing_menu() -> str:
    """Return breathing exercises menu."""
    return """
**🧘 Breathing Exercises**

Choose an exercise:

• **box** — Box Breathing (4 min) — Used by Navy SEALs to stay calm
• **478** — 4-7-8 Breathing (3 min) — Great for anxiety and sleep
• **grounding** — 5-4-3-2-1 Grounding (5 min) — Brings you to the present

Type the exercise name to begin.
"""


def get_meditation_menu() -> str:
    """Return meditation menu."""
    return """
**🧘 Quick Meditations**

Choose a meditation:

• **calm** — 2-Minute Calm — Quick reset
• **body scan** — Body Scan — Release tension
• **self compassion** — Self-Compassion — Be kind to yourself

Type the meditation name to begin.
"""


def get_mood_prompt() -> str:
    """Return mood tracking prompt."""
    session = get_user_session()
    
    response = "**📊 Mood Check-In**\n\n"
    
    # Show recent history if exists
    if session["mood_history"]:
        response += "**Recent Mood History:**\n"
        recent = session["mood_history"][-5:]
        for m in recent:
            response += f"• {m['timestamp'][:10]}: {m['mood']} ({m['intensity']}/5)\n"
        response += "\n"
    
    response += """How are you feeling right now? Rate your mood:

1️⃣ Really struggling
2️⃣ Not great
3️⃣ Okay/Neutral
4️⃣ Pretty good
5️⃣ Great!

Type a number (1-5), or just describe how you're feeling."""
    
    return response


# ============================================================================
# CHAINLIT EVENT HANDLERS
# ============================================================================

@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session."""
    # Generate a session ID
    cl.user_session.set("id", str(datetime.now().timestamp()))
    
    welcome_message = """
**🌿 Welcome to CalmSpace**

I'm here to support you through whatever you're experiencing—stress, anxiety, loneliness, exam pressure, or just needing someone to talk to.

**This is a safe, judgment-free space.** 💙

**Commands you can use:**
• **menu** — See all options
• **mood** — Track your mood
• **challenge** — Daily wellness challenge
• **resources** — Browse mental health topics
• **breathe** — Breathing exercises
• **meditate** — Quick meditations
• **journal** — Journal prompts
• **coping** — Coping strategies
• **crisis** — Crisis helplines

Or just tell me how you're feeling. **How are you doing today?**

*Note: I'm an AI companion, not a replacement for professional help. If you're in crisis, type 'crisis' for immediate resources.*
"""
    
    await cl.Message(content=welcome_message).send()


@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming messages."""
    user_msg = message.content.strip()
    user_msg_lower = user_msg.lower()
    
    # Add to conversation history
    add_to_conversation("user", user_msg)
    
    # ===== CRISIS CHECK (ALWAYS FIRST) =====
    if check_crisis(user_msg):
        crisis_response = f"""
I hear that you're going through something really difficult right now, and I'm genuinely concerned about you. 💙

What you're feeling is real, and you deserve support.

{CRISIS_RESOURCES}

I'm here if you want to talk, but please also reach out to one of these resources. You don't have to go through this alone.
"""
        await cl.Message(content=crisis_response).send()
        add_to_conversation("assistant", crisis_response)
        return
    
    # ===== COMMAND HANDLING =====
    
    # Menu
    if user_msg_lower in ["menu", "help", "options", "/menu", "/help", "start"]:
        await cl.Message(content=get_menu()).send()
        return
    
    # Resources
    if user_msg_lower in ["resources", "resource", "library", "topics", "/resources"]:
        await cl.Message(content=get_resource_menu()).send()
        return
    
    # Challenge
    if user_msg_lower in ["challenge", "wellness", "daily", "/challenge"]:
        response = get_wellness_challenge()
        await cl.Message(content=response).send()
        return
    
    # Challenge with day number
    if user_msg_lower.startswith("challenge "):
        try:
            day = int(user_msg_lower.split(" ")[1])
            response = get_wellness_challenge(day)
            await cl.Message(content=response).send()
            return
        except:
            pass
    
    # Next challenge
    if user_msg_lower in ["next challenge", "next", "tomorrow"]:
        session = get_user_session()
        session["challenge_day"] = min(session["challenge_day"] + 1, 30)
        response = get_wellness_challenge()
        await cl.Message(content=response).send()
        return
    
    # Journal
    if user_msg_lower in ["journal", "journal prompts", "prompts", "/journal"]:
        response = get_journal_prompts()
        await cl.Message(content=response).send()
        return
    
    # Breathe menu
    if user_msg_lower in ["breathe", "breathing", "breath", "/breathe"]:
        await cl.Message(content=get_breathing_menu()).send()
        return
    
    # Specific breathing exercises
    if user_msg_lower in ["box", "box breathing"]:
        await cl.Message(content=BREATHING_EXERCISES["box"]["content"]).send()
        return
    
    if user_msg_lower in ["478", "4-7-8", "4 7 8"]:
        await cl.Message(content=BREATHING_EXERCISES["478"]["content"]).send()
        return
    
    if user_msg_lower in ["grounding", "5-4-3-2-1", "54321", "ground"]:
        await cl.Message(content=BREATHING_EXERCISES["grounding"]["content"]).send()
        return
    
    # Meditate menu
    if user_msg_lower in ["meditate", "meditation", "/meditate"]:
        await cl.Message(content=get_meditation_menu()).send()
        return
    
    # Specific meditations
    if user_msg_lower in ["calm", "2 minute calm", "2-minute calm", "quick calm"]:
        await cl.Message(content=MEDITATION_SCRIPTS["calm"]["content"]).send()
        return
    
    if user_msg_lower in ["body scan", "bodyscan", "body"]:
        await cl.Message(content=MEDITATION_SCRIPTS["body scan"]["content"]).send()
        return
    
    if user_msg_lower in ["self compassion", "self-compassion", "compassion"]:
        await cl.Message(content=MEDITATION_SCRIPTS["self compassion"]["content"]).send()
        return
    
    # Coping strategies
    if user_msg_lower in ["coping", "cope", "strategies", "/coping"]:
        await cl.Message(content=get_coping_strategies()).send()
        return
    
    # Emotion-specific coping
    if user_msg_lower.startswith("coping "):
        emotion = user_msg_lower.replace("coping ", "").strip()
        await cl.Message(content=get_coping_strategies(emotion)).send()
        return
    
    # Crisis
    if user_msg_lower in ["crisis", "emergency", "help now", "/crisis", "helpline", "helplines"]:
        await cl.Message(content=CRISIS_RESOURCES).send()
        return
    
    # Mood tracking
    if user_msg_lower in ["mood", "track mood", "how am i", "/mood", "mood check"]:
        await cl.Message(content=get_mood_prompt()).send()
        return
    
    # Mood rating (1-5)
    if user_msg_lower in ["1", "2", "3", "4", "5"]:
        mood_labels = {
            "1": "struggling",
            "2": "not great", 
            "3": "okay",
            "4": "good",
            "5": "great"
        }
        mood = mood_labels[user_msg_lower]
        intensity = int(user_msg_lower)
        log_mood(mood, intensity)
        
        if intensity <= 2:
            response = f"Thank you for sharing. I've logged that you're feeling {mood}. That takes courage to acknowledge. 💙\n\nWould you like to talk about what's going on? I'm here to listen."
        elif intensity == 3:
            response = f"Logged: Feeling {mood}. 💙\n\nSometimes 'okay' is just fine. Is there anything specific on your mind today?"
        else:
            response = f"Logged: Feeling {mood}! 💙 That's wonderful to hear.\n\nIs there anything you'd like to chat about, or would you like to try today's wellness challenge?"
        
        await cl.Message(content=response).send()
        add_to_conversation("assistant", response)
        return
    
    # Check if it's a resource request (by number or name)
    resource = get_resource(user_msg)
    if resource:
        await cl.Message(content=resource).send()
        return
    
    # ===== AI RESPONSE FOR GENERAL CHAT =====
    
    # Detect scenario for context-aware response
    scenario = detect_scenario(user_msg)
    
    # Get AI response
    response = await get_ai_response(user_msg, scenario)
    
    add_to_conversation("assistant", response)
    
    await cl.Message(content=response).send()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("CalmSpace Mental Health Support Bot")
    print("Run with: chainlit run main.py -w")
