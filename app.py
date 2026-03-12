import streamlit as st
import json
import os
from datetime import datetime, date, timedelta
import random
import math

# ============================================
# CONFIG
# ============================================
DATA_FILE = "player_data.json"

st.set_page_config(
    page_title="Shadow System",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SOLO LEVELING + MINECRAFT THEME
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Orbitron:wght@400;700;900&family=VT323&display=swap');

    .stApp {
        background-color: #0a0a1a;
    }
    section[data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 2px solid #4361ee;
    }
    .status-window {
        background: linear-gradient(180deg, #0a1628 0%, #0d1f3c 100%);
        border: 2px solid #4361ee;
        border-radius: 4px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(67, 97, 238, 0.3),
                    inset 0 0 20px rgba(67, 97, 238, 0.05);
        margin: 10px 0;
        font-family: 'Orbitron', monospace;
    }
    .system-alert {
        background: linear-gradient(180deg, #1a0a28 0%, #2d1f4e 100%);
        border: 2px solid #9b59b6;
        border-radius: 4px;
        padding: 15px;
        box-shadow: 0 0 15px rgba(155, 89, 182, 0.3);
        margin: 10px 0;
        text-align: center;
        font-family: 'Orbitron', monospace;
        color: #bb86fc;
    }
    .quest-card {
        background: #111927;
        border: 1px solid #1e3a5f;
        border-left: 4px solid #00b4d8;
        padding: 12px 15px;
        margin: 6px 0;
        border-radius: 0 4px 4px 0;
        font-family: 'VT323', monospace;
        font-size: 1.1rem;
    }
    .quest-done {
        background: #0d2818;
        border: 1px solid #1a5c2e;
        border-left: 4px solid #00ff88;
        padding: 12px 15px;
        margin: 6px 0;
        border-radius: 0 4px 4px 0;
        font-family: 'VT323', monospace;
        font-size: 1.1rem;
        color: #00ff88;
    }
    .quest-active {
        background: #1a1a00;
        border: 1px solid #5c5c1a;
        border-left: 4px solid #ffdd00;
        padding: 12px 15px;
        margin: 6px 0;
        border-radius: 0 4px 4px 0;
        font-family: 'VT323', monospace;
        font-size: 1.1rem;
        color: #ffdd00;
        animation: glow 2s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { box-shadow: 0 0 5px rgba(255, 221, 0, 0.2); }
        to { box-shadow: 0 0 15px rgba(255, 221, 0, 0.4); }
    }
    .xp-bar-outer {
        background: #1a1a2e;
        border: 2px solid #4361ee;
        height: 30px;
        border-radius: 3px;
        overflow: hidden;
        position: relative;
    }
    .xp-bar-inner {
        background: linear-gradient(90deg, #4361ee, #00b4d8);
        height: 100%;
        transition: width 0.5s;
        box-shadow: 0 0 10px rgba(0, 180, 216, 0.5);
    }
    .xp-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        font-family: 'Press Start 2P', monospace;
        font-size: 0.6rem;
        text-shadow: 1px 1px 2px black;
    }
    .hp-bar-outer {
        background: #1a1a2e;
        border: 2px solid #e74c3c;
        height: 25px;
        border-radius: 3px;
        overflow: hidden;
    }
    .hp-bar-inner {
        background: linear-gradient(90deg, #c0392b, #e74c3c, #ff6b6b);
        height: 100%;
    }
    .stat-box {
        background: #111927;
        border: 1px solid #4361ee;
        border-radius: 4px;
        padding: 15px;
        text-align: center;
        font-family: 'Orbitron', monospace;
    }
    .rank-badge {
        font-family: 'Press Start 2P', monospace;
        font-size: 1.5rem;
        padding: 5px 15px;
        border-radius: 4px;
        display: inline-block;
        margin: 5px;
    }
    .rank-e { background: #333; color: #888; border: 2px solid #555; }
    .rank-d { background: #1a3a1a; color: #55ff55; border: 2px solid #55ff55; }
    .rank-c { background: #1a1a3a; color: #5555ff; border: 2px solid #5555ff; }
    .rank-b { background: #3a1a3a; color: #ff55ff; border: 2px solid #ff55ff; }
    .rank-a { background: #3a3a1a; color: #ffaa00; border: 2px solid #ffaa00; }
    .rank-s { background: #3a1a1a; color: #ff3333; border: 2px solid #ff3333;
              box-shadow: 0 0 20px rgba(255,51,51,0.5); }
    .pixel-title {
        font-family: 'Press Start 2P', monospace;
        color: #00b4d8;
        text-shadow: 2px 2px 0px #4361ee;
        margin: 10px 0;
    }
    .minecraft-block {
        background: #2d5a27;
        border: 3px solid #1a3a15;
        border-top-color: #4a8a40;
        border-left-color: #4a8a40;
        padding: 15px;
        margin: 5px 0;
        font-family: 'VT323', monospace;
        font-size: 1.1rem;
        color: white;
        image-rendering: pixelated;
    }
    .resource-link {
        background: #111927;
        border: 1px solid #1e3a5f;
        border-radius: 4px;
        padding: 10px 15px;
        margin: 4px 0;
        display: block;
        font-family: 'VT323', monospace;
        font-size: 1.1rem;
    }
    .resource-link a {
        color: #00b4d8;
        text-decoration: none;
    }
    .resource-link a:hover {
        color: #00ff88;
    }
    .review-card {
        background: linear-gradient(180deg, #1a0a28 0%, #0d1f3c 100%);
        border: 2px solid #9b59b6;
        border-radius: 4px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 15px rgba(155, 89, 182, 0.2);
    }
    div[data-testid="stMetric"] {
        background: #111927;
        border: 1px solid #4361ee;
        border-radius: 4px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# DATA PERSISTENCE
# ============================================
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "player_name": "Player",
        "xp": 0,
        "weights": {},
        "daily_quests": {},
        "workout_done": {},
        "water_intake": {},
        "reviews": {},
        "fiverr_earnings": [],
        "deliverables": {},
    }


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ============================================
# GAME SYSTEM
# ============================================
def get_level(xp):
    return max(1, int(math.sqrt(xp / 20)) + 1)


def get_xp_for_level(level):
    return ((level - 1) ** 2) * 20


def get_rank(level):
    if level >= 51:
        return "S", "Shadow Monarch of AI", "rank-s"
    if level >= 41:
        return "A", "LLM Architect", "rank-a"
    if level >= 31:
        return "B", "Transformer Sage", "rank-b"
    if level >= 21:
        return "C", "Neural Knight", "rank-c"
    if level >= 11:
        return "D", "Algorithm Hunter", "rank-d"
    return "E", "Shadow Initiate", "rank-e"


def get_hp(data):
    today = date.today().strftime("%Y-%m-%d")
    hp = 100
    checks = data.get("daily_quests", {}).get(today, [])
    if checks:
        done = sum(1 for c in checks if c)
        total = len(checks)
        hp = int((done / max(total, 1)) * 100)
    return hp


def add_xp(data, amount, reason=""):
    data["xp"] = data.get("xp", 0) + amount
    return data


XP_REWARDS = {
    "workout": 20,
    "study_session": 15,
    "fiverr": 15,
    "water_target": 5,
    "clean_eating": 5,
    "sleep_on_time": 10,
    "quest_complete": 10,
}

SYSTEM_MESSAGES = [
    "⚔️ [SYSTEM] A new quest has arrived.",
    "⚔️ [SYSTEM] Your shadow army grows stronger.",
    "⚔️ [SYSTEM] Arise. Train. Conquer.",
    "⚔️ [SYSTEM] The dungeon awaits, Hunter.",
    "⚔️ [SYSTEM] Consistency is your greatest weapon.",
    "⚔️ [SYSTEM] You have leveled up your resolve.",
    "⚔️ [SYSTEM] The weak die. The strong survive. CODE.",
    "⚔️ [SYSTEM] Daily quest completion rate affects your rank.",
    "⚔️ [SYSTEM] Your future self is watching. Make him proud.",
    "⚔️ [SYSTEM] IIT Patna + AI skills = S-Rank Hunter.",
    "⚔️ [SYSTEM] 75 → 65 kg. The body dungeon WILL be cleared.",
    "⚔️ [SYSTEM] Every line of code = +1 INT stat.",
]


# ============================================
# SCHEDULE DATA
# ============================================
def get_weekday_schedule():
    return [
        ("05:30", "05:45", "Wake Up + Warm Water", "wake", "🔔"),
        ("05:45", "06:30", "TRAINING: Workout", "workout", "🏋️"),
        ("06:30", "07:00", "Shower + Get Ready", "rest", "🚿"),
        ("07:00", "07:30", "Fuel Up: Breakfast", "food", "🍳"),
        ("07:30", "08:30", "DUNGEON: AI/ML Session 1", "study", "📖"),
        ("08:30", "09:00", "Travel to College", "travel", "🚶"),
        ("09:00", "15:00", "ACADEMY: College Classes", "college", "🎓"),
        ("15:00", "15:30", "Walk Back + Healthy Snack", "travel", "🍎"),
        ("15:30", "16:00", "REST: Power Nap", "rest", "😴"),
        ("16:00", "17:30", "DUNGEON: AI/ML Session 2", "study", "💻"),
        ("17:30", "19:00", "GUILD: Fiverr Work", "fiverr", "💰"),
        ("19:00", "19:30", "TRAINING: Evening Walk", "workout", "🚶"),
        ("19:30", "20:00", "Fuel Up: Dinner", "food", "🍽️"),
        ("20:00", "20:30", "DUNGEON: AI/ML Review", "study", "📝"),
        ("20:30", "21:30", "ACADEMY: Homework", "college", "📚"),
        ("21:30", "22:00", "Free Time", "free", "📱"),
        ("22:00", "05:30", "RECOVERY: Sleep", "sleep", "😴"),
    ]


def get_weekend_schedule():
    return [
        ("06:00", "06:15", "Wake Up", "wake", "🔔"),
        ("06:15", "07:15", "TRAINING: Workout (1 hr)", "workout", "🏋️"),
        ("07:15", "08:00", "Shower + Breakfast", "food", "🍳"),
        ("08:00", "10:30", "DUNGEON: Deep Study Session", "study", "📖"),
        ("10:30", "11:00", "Break + Snack", "rest", "☕"),
        ("11:00", "13:00", "GUILD: Fiverr Work", "fiverr", "💰"),
        ("13:00", "13:30", "Fuel Up: Lunch", "food", "🍽️"),
        ("13:30", "14:30", "REST: Nap", "rest", "😴"),
        ("14:30", "17:00", "DUNGEON: Project Work", "study", "💻"),
        ("17:00", "18:00", "TRAINING: Sports", "workout", "🏏"),
        ("18:00", "19:00", "ACADEMY: College Prep", "college", "🎓"),
        ("19:00", "20:00", "Walk + Dinner", "food", "🍽️"),
        ("20:00", "22:00", "Free Time", "free", "📱"),
        ("22:00", "06:00", "RECOVERY: Sleep", "sleep", "😴"),
    ]


def time_to_min(t):
    h, m = map(int, t.split(":"))
    return h * 60 + m


def get_current_block():
    now = datetime.now()
    cm = now.hour * 60 + now.minute
    is_wknd = now.weekday() >= 5
    sched = get_weekend_schedule() if is_wknd else get_weekday_schedule()
    for start, end, name, cat, icon in sched:
        s, e = time_to_min(start), time_to_min(end)
        if e < s:
            if cm >= s or cm < e:
                return name, cat, icon
        elif s <= cm < e:
            return name, cat, icon
    return "Free Time", "free", "📱"


# ============================================
# MONTHLY PLAN DATA
# ============================================
MONTHLY_PLANS = {
    3: {
        "name": "March", "topic": "Python Programming",
        "icon": "🐍", "weight": (75, 74),
        "fiverr": "3K-5K",
        "videos": [
            ("CS50P - Harvard (Full Course)", "https://www.youtube.com/watch?v=nLRL_NcnK-4", "Week 1-2"),
            ("Keith Galli - NumPy", "https://www.youtube.com/watch?v=QUT1VHiLmmI", "Week 3"),
            ("Keith Galli - Pandas", "https://www.youtube.com/watch?v=vmEHCJofslg", "Week 3"),
            ("Corey Schafer - Matplotlib", "https://www.youtube.com/playlist?list=PL-osiE80TeTvipOqomVEeZ1HRrcEvtZB_", "Week 4"),
        ],
        "readings": [
            ("w3schools Python", "https://www.w3schools.com/python/"),
            ("Automate the Boring Stuff (Free Book)", "https://automatetheboringstuff.com/"),
            ("Kaggle Pandas Course", "https://www.kaggle.com/learn/pandas"),
            ("Kaggle Data Viz Course", "https://www.kaggle.com/learn/data-visualization"),
            ("Python Data Science Handbook", "https://jakevdp.github.io/PythonDataScienceHandbook/"),
        ],
        "tasks": [
            "Complete CS50P course",
            "Solve 50 HackerRank Python problems",
            "Learn NumPy + Pandas + Matplotlib",
            "Earn Kaggle Python Certificate",
            "Earn Kaggle Pandas Certificate",
            "Earn Kaggle Data Viz Certificate",
            "Build 1 EDA project on GitHub",
        ],
        "workout": "Beginner: Push-ups 3x15 | Pull-ups 3x5 | Squats 3x20 | Run 20min | Plank 30s",
        "diet": "2 eggs+2roti breakfast | 2roti+dal+sabzi lunch | fruit+nuts snack | light dinner | 3-4L water | NO junk",
    },
    4: {
        "name": "April", "topic": "Mathematics for ML",
        "icon": "📐", "weight": (74, 73),
        "fiverr": "5K-8K",
        "videos": [
            ("3B1B - Essence of Linear Algebra", "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab", "Week 1"),
            ("3B1B - Essence of Calculus", "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr", "Week 2"),
            ("StatQuest - Statistics Fundamentals", "https://www.youtube.com/playlist?list=PLblh5JKOoLUK0FLuzwntyYI10UQFUhsY9", "Week 3"),
        ],
        "readings": [
            ("Khan Academy - Linear Algebra", "https://www.khanacademy.org/math/linear-algebra"),
            ("Khan Academy - Calculus", "https://www.khanacademy.org/math/calculus-1"),
            ("Khan Academy - Statistics", "https://www.khanacademy.org/math/statistics-probability"),
            ("Mathematics for ML (Free Book)", "https://mml-book.github.io/"),
            ("Seeing Theory (Interactive)", "https://seeing-theory.brown.edu/"),
        ],
        "tasks": [
            "Complete 3B1B Linear Algebra playlist",
            "Complete 3B1B Calculus playlist",
            "Complete StatQuest Statistics playlist",
            "Finish Khan Academy exercises",
            "Read MML Book Chapters 2-6",
            "Explain: matrices, derivatives, Bayes theorem",
        ],
        "workout": "Push-ups 3x20 | Pull-ups 3x8 | Squats 3x25 | Run 25min | Plank 45s | Jump rope 5min",
        "diet": "Same + peanut butter breakfast | soya chunks 2-3x/week | replace 1 roti with salad | green tea 2x",
    },
    5: {
        "name": "May", "topic": "Machine Learning - Part 1",
        "icon": "🤖", "weight": (73, 71),
        "fiverr": "8K-12K",
        "videos": [
            ("Andrew Ng - ML Specialization", "https://www.coursera.org/specializations/machine-learning-introduction", "All month"),
            ("StatQuest - Linear Regression", "https://www.youtube.com/watch?v=PaFPbb66DxQ", "Week 1"),
            ("StatQuest - Logistic Regression", "https://www.youtube.com/watch?v=yIYKR4sgzI8", "Week 3"),
            ("StatQuest - Decision Trees", "https://www.youtube.com/watch?v=_L39rN6gz7Y", "Week 3"),
            ("StatQuest - Random Forest", "https://www.youtube.com/watch?v=J4Wdy0Wc_xQ", "Week 3"),
            ("StatQuest - SVM", "https://www.youtube.com/watch?v=efR1C6CvhmE", "Week 4"),
        ],
        "readings": [
            ("Stanford CS229 Cheat Sheets", "https://stanford.edu/~shervine/teaching/cs-229/"),
            ("Kaggle Intro to ML", "https://www.kaggle.com/learn/intro-to-machine-learning"),
            ("Scikit-learn User Guide", "https://scikit-learn.org/stable/user_guide.html"),
            ("ISLR (Free ML Textbook)", "https://www.statlearning.com/"),
        ],
        "tasks": [
            "Start Andrew Ng ML Course 1",
            "Earn Kaggle 'Intro to ML' Certificate",
            "Understand Linear/Logistic Regression",
            "Understand Decision Trees, Random Forest, SVM, KNN",
            "Train 3 models on Kaggle datasets",
            "Read ISLR Chapters 1-6",
        ],
        "workout": "Push-ups 4x20 | Pull-ups 3x10 | Squats 4x25 | Run 30min | HIIT 7 rounds | Jump rope 10min",
        "diet": "3 egg whites+1 whole | 1.5 roti+extra dal+salad | chaas+fruit | 1 roti dinner | NO rice | 4-5L water",
    },
    6: {
        "name": "June", "topic": "Machine Learning - Part 2",
        "icon": "🤖", "weight": (71, 70),
        "fiverr": "10K-15K",
        "videos": [
            ("Andrew Ng - Course 2 and 3", "https://www.coursera.org/specializations/machine-learning-introduction", "Week 1-2"),
            ("StatQuest - K-Means", "https://www.youtube.com/watch?v=4b5d3muPQmA", "Week 1"),
            ("StatQuest - PCA", "https://www.youtube.com/watch?v=FgakZw6K1QQ", "Week 1"),
            ("StatQuest - XGBoost", "https://www.youtube.com/watch?v=OtD8wVaFm6E", "Week 2"),
        ],
        "readings": [
            ("Kaggle Intermediate ML", "https://www.kaggle.com/learn/intermediate-machine-learning"),
            ("Kaggle Feature Engineering", "https://www.kaggle.com/learn/feature-engineering"),
            ("Stanford Unsupervised Cheat Sheet", "https://stanford.edu/~shervine/teaching/cs-229/cheatsheet-unsupervised-learning"),
        ],
        "tasks": [
            "Finish ALL 3 Andrew Ng courses",
            "Earn Kaggle Intermediate ML Certificate",
            "Earn Kaggle Feature Engineering Certificate",
            "House Price Prediction project",
            "Titanic Survival project",
            "Customer Segmentation project",
            "Push all projects to GitHub",
        ],
        "workout": "Push-ups 4x25 | Pull-ups 3x12 | Run 35min | Jump rope 12min",
        "diet": "Add paneer 3x/week | soya daily | post-workout banana+milk | protein 80-90g/day",
    },
    7: {
        "name": "July", "topic": "Deep Learning - Part 1",
        "icon": "🧠", "weight": (70, 69),
        "fiverr": "15K-20K",
        "videos": [
            ("3B1B - Neural Networks", "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi", "Week 1"),
            ("Karpathy - NN: Zero to Hero", "https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ", "Week 1"),
            ("Daniel Bourke - PyTorch Full", "https://www.youtube.com/watch?v=Z_ikDlimN6A", "Week 2-3"),
        ],
        "readings": [
            ("learnpytorch.io (Free Course)", "https://www.learnpytorch.io/"),
            ("Stanford CS231n Notes", "https://cs231n.github.io/"),
            ("Dive into Deep Learning", "https://d2l.ai/"),
            ("CS230 DL Cheat Sheets", "https://stanford.edu/~shervine/teaching/cs-230/"),
            ("Kaggle Computer Vision", "https://www.kaggle.com/learn/computer-vision"),
        ],
        "tasks": [
            "Understand neural networks from scratch",
            "Complete PyTorch course",
            "Build CNN image classifier",
            "Earn Kaggle CV Certificate",
            "Read d2l.ai Chapters 1-8",
            "Push image project to GitHub",
        ],
        "workout": "Push-ups 5x25 | Pull-ups 4x12 | Squats 4x30 | Run 40min | Plank 90s | 100 push-ups challenge",
        "diet": "Increase protein (keep muscle) | curd+paneer at dinner | sprouts snack | 1800-1900 cal",
    },
    8: {
        "name": "August", "topic": "Deep Learning - Part 2 (Transformers)",
        "icon": "⚡", "weight": (69, 68),
        "fiverr": "20K-25K",
        "videos": [
            ("StatQuest - RNN", "https://www.youtube.com/watch?v=AsNTP8Kwu80", "Week 1"),
            ("StatQuest - LSTM", "https://www.youtube.com/watch?v=YCzL96nL7j0", "Week 1"),
            ("3B1B - Transformers", "https://www.youtube.com/watch?v=wjZofJX0v4M", "Week 3"),
            ("StatQuest - Transformer", "https://www.youtube.com/watch?v=zxQyTK8quyY", "Week 3"),
            ("Karpathy - Lets Build GPT", "https://www.youtube.com/watch?v=kCc8FmEb1nY", "Week 4"),
        ],
        "readings": [
            ("Illustrated Transformer (MUST READ)", "https://jalammar.github.io/illustrated-transformer/"),
            ("Illustrated GPT-2", "https://jalammar.github.io/illustrated-gpt2/"),
            ("Illustrated BERT", "https://jalammar.github.io/illustrated-bert/"),
            ("Annotated Transformer", "https://nlp.seas.harvard.edu/annotated-transformer/"),
        ],
        "tasks": [
            "Understand RNNs and LSTMs",
            "FULLY understand Transformer architecture",
            "Code Transformer from scratch",
            "Read ALL Jay Alammar guides",
            "Read d2l.ai Chapters 9-11",
            "Explain: self-attention, multi-head, positional encoding",
        ],
        "workout": "Slower reps | resistance bands | Run 40min 3days + HIIT 2days | Focus: lean AND fit",
        "diet": "Calories 1900-2000 | Protein 90-100g/day | milk before bed | chana snack | 7 KG DOWN!",
    },
    9: {
        "name": "September", "topic": "NLP",
        "icon": "📝", "weight": (68, 67),
        "fiverr": "25K-30K",
        "videos": [
            ("Stanford CS224n (First 8 Lectures)", "https://www.youtube.com/playlist?list=PLoROMvodv4rMFqRtEuo6SGjY4XbRIVRd4", "Week 1-2"),
        ],
        "readings": [
            ("Hugging Face NLP Course", "https://huggingface.co/learn/nlp-course"),
            ("spaCy Free Course", "https://course.spacy.io/en/"),
            ("Kaggle NLP Course", "https://www.kaggle.com/learn/natural-language-processing"),
            ("Speech and Language Processing (Free)", "https://web.stanford.edu/~jurafsky/slp3/"),
            ("NLP Course by Lena Voita", "https://lena-voita.github.io/nlp_course.html"),
        ],
        "tasks": [
            "Watch CS224n first 8 lectures",
            "Complete Hugging Face NLP Course",
            "Complete spaCy Course",
            "Earn Kaggle NLP Certificate",
            "Build sentiment analysis project",
            "Deploy on Hugging Face Spaces",
        ],
        "workout": "Diamond push-ups 4x15 | Archer push-ups 3x8 | Pull-ups 4x12 weighted | Plank 2min",
        "diet": "Fine-tune based on feel | 1900-2000 cal | if stalled drop to 1750 | protein 100g+",
    },
    10: {
        "name": "October", "topic": "LLMs and Generative AI",
        "icon": "🤖", "weight": (67, 66),
        "fiverr": "30K-40K",
        "videos": [
            ("Karpathy - Lets Build GPT", "https://www.youtube.com/watch?v=kCc8FmEb1nY", "Week 1"),
        ],
        "readings": [
            ("Prompt Engineering Guide", "https://www.promptingguide.ai/"),
            ("LangChain Docs", "https://python.langchain.com/docs/"),
            ("Microsoft GenAI Course (18 Lessons)", "https://github.com/microsoft/generative-ai-for-beginners"),
            ("LLMs from Scratch Code", "https://github.com/rasbt/LLMs-from-scratch"),
            ("Chip Huyen - LLM Engineering", "https://huyenchip.com/2023/04/11/llm-engineering.html"),
            ("DeepLearning.AI Short Courses", "https://www.deeplearning.ai/short-courses/"),
        ],
        "tasks": [
            "Understand how GPT/LLMs work",
            "Complete 5+ DeepLearning.AI short courses",
            "Build RAG chatbot project",
            "Build AI Resume Screener",
            "Learn LangChain basics",
            "Push both projects to GitHub",
        ],
        "workout": "Focus: muscle definition | ab work (V-ups, hanging leg raises) | compound movements",
        "diet": "1800-1900 cal | Protein 100g/day | 1 cheat meal/week (earned it!)",
    },
    11: {
        "name": "November", "topic": "MLOps + Computer Vision",
        "icon": "🚀", "weight": (66, 65),
        "fiverr": "40K-50K",
        "videos": [
            ("Data Professor - Streamlit", "https://www.youtube.com/watch?v=JwSS70SZdyM", "Week 1"),
            ("freeCodeCamp - FastAPI", "https://www.youtube.com/watch?v=tLKKmouUams", "Week 1"),
            ("TechWorld Nana - Docker", "https://www.youtube.com/watch?v=3c-iBn73dDE", "Week 2"),
            ("freeCodeCamp - OpenCV", "https://www.youtube.com/watch?v=oXlwWbU8l2o", "Week 3"),
        ],
        "readings": [
            ("Made With ML (BEST MLOps)", "https://madewithml.com/"),
            ("Streamlit Docs", "https://docs.streamlit.io/"),
            ("FastAPI Docs", "https://fastapi.tiangolo.com/"),
            ("Docker Get Started", "https://docs.docker.com/get-started/"),
            ("Ultralytics YOLO Docs", "https://docs.ultralytics.com/"),
        ],
        "tasks": [
            "Deploy 2 projects online (live URLs!)",
            "Learn Docker basics",
            "Complete Made With ML course",
            "Build object detection app (YOLOv8)",
            "All projects on GitHub with READMEs",
            "HIT 65 KG TARGET!",
        ],
        "workout": "GOAL HIT! Maintain 65 + build muscle | push-ups 50 in a row | pull-ups 15 in a row",
        "diet": "MAINTENANCE: 2000-2100 cal | Protein 100-110g/day | 1-2 cheat meals/week OK",
    },
    12: {
        "name": "December", "topic": "Portfolio Projects",
        "icon": "📂", "weight": (65, 65),
        "fiverr": "40K-50K",
        "videos": [],
        "readings": [
            ("GitHub Profile Guide", "https://docs.github.com/en/account-and-profile"),
        ],
        "tasks": [
            "Build 5-6 polished projects with live demos",
            "GitHub profile looks professional",
            "LinkedIn profile optimized",
            "Start posting on LinkedIn",
            "Earn ALL Kaggle certificates (8+)",
        ],
        "workout": "Maintain 65kg | workout 5-6 days/week",
        "diet": "Maintenance | clean eating is lifestyle now",
    },
    1: {
        "name": "January", "topic": "Interview Preparation",
        "icon": "🎤", "weight": (65, 65),
        "fiverr": "50K+",
        "videos": [],
        "readings": [
            ("ML Interviews Book (FREE)", "https://huyenchip.com/ml-interviews-book/"),
            ("DL Interview Book (400p)", "https://arxiv.org/abs/2201.00650"),
            ("ML Interview Questions", "https://github.com/khangich/machine-learning-interview"),
            ("Stanford Cheat Sheets", "https://stanford.edu/~shervine/teaching/"),
        ],
        "tasks": [
            "Read ML Interviews Book completely",
            "Practice 200+ interview questions",
            "Apply to 50+ positions",
            "Resume polished - 1 page",
            "GitHub + LinkedIn optimized",
            "Mock interviews with peers",
        ],
        "workout": "Maintain 65 kg",
        "diet": "Maintenance",
    },
    2: {
        "name": "February", "topic": "Advanced + Job Hunting",
        "icon": "🏆", "weight": (65, 65),
        "fiverr": "Job Offers!",
        "videos": [],
        "readings": [
            ("Papers With Code", "https://paperswithcode.com/"),
            ("DeepLearning.AI Short Courses", "https://www.deeplearning.ai/short-courses/"),
        ],
        "tasks": [
            "Interviewed at 5-10 companies",
            "Got at least 1-2 offers",
            "Contributed to open source",
            "Participated in Kaggle competition",
            "YOU ARE NOW AN AI/ML ENGINEER!",
        ],
        "workout": "Fitness is lifestyle now",
        "diet": "Intuitive clean eating",
    },
}


def get_plan():
    m = datetime.now().month
    if m in MONTHLY_PLANS:
        return MONTHLY_PLANS[m]
    return MONTHLY_PLANS[3]


# ============================================
# PAGE: PLAYER STATUS (HOME)
# ============================================
def page_status():
    data = load_data()
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    plan = get_plan()

    # System message
    st.markdown(f"""
    <div class="system-alert">
        {random.choice(SYSTEM_MESSAGES)}
    </div>
    """, unsafe_allow_html=True)

    # Player name setup
    if data.get("player_name", "Player") == "Player":
        name = st.text_input("⚔️ Enter your Hunter name:", placeholder="Sung Jin-Woo")
        if name:
            data["player_name"] = name
            save_data(data)
            st.rerun()
        return

    # Calculate stats
    xp = data.get("xp", 0)
    level = get_level(xp)
    rank_letter, rank_title, rank_class = get_rank(level)
    current_level_xp = get_xp_for_level(level)
    next_level_xp = get_xp_for_level(level + 1)
    xp_progress = xp - current_level_xp
    xp_needed = max(next_level_xp - current_level_xp, 1)
    xp_pct = min(int((xp_progress / xp_needed) * 100), 100)
    hp = get_hp(data)
    current_block, current_cat, current_icon = get_current_block()

    # Workout streak
    streak = 0
    check = date.today()
    while data.get("workout_done", {}).get(check.strftime("%Y-%m-%d"), False):
        streak += 1
        check -= timedelta(days=1)

    # Weight
    weights = data.get("weights", {})
    current_weight = "??"
    if weights:
        latest_key = sorted(weights.keys())[-1]
        current_weight = weights[latest_key]

    # STATUS WINDOW
    st.markdown(f"""
    <div class="status-window">
        <div style="text-align:center; margin-bottom:15px;">
            <span class="pixel-title" style="font-size:0.8rem;">
                — S T A T U S  W I N D O W —
            </span>
        </div>
        <table style="width:100%; color:white; font-family:'Orbitron',monospace;">
            <tr>
                <td style="padding:5px;"><span style="color:#888;">NAME:</span></td>
                <td style="padding:5px;"><b>{data['player_name']}</b></td>
                <td style="padding:5px;"><span style="color:#888;">RANK:</span></td>
                <td style="padding:5px;"><span class="rank-badge {rank_class}">{rank_letter}-Rank</span></td>
            </tr>
            <tr>
                <td style="padding:5px;"><span style="color:#888;">LEVEL:</span></td>
                <td style="padding:5px;"><b style="color:#00b4d8; font-size:1.5rem;">{level}</b></td>
                <td style="padding:5px;"><span style="color:#888;">TITLE:</span></td>
                <td style="padding:5px;"><span style="color:#bb86fc;">{rank_title}</span></td>
            </tr>
        </table>
        <br>
        <div style="color:#888; font-size:0.8rem; margin-bottom:3px;">HP (Daily Quests)</div>
        <div class="hp-bar-outer">
            <div class="hp-bar-inner" style="width:{hp}%;"></div>
        </div>
        <div style="text-align:right; color:#e74c3c; font-size:0.8rem;">{hp}/100</div>
        <div style="color:#888; font-size:0.8rem; margin-bottom:3px;">XP (Level {level} → {level+1})</div>
        <div class="xp-bar-outer">
            <div class="xp-bar-inner" style="width:{xp_pct}%;"></div>
            <div class="xp-text">{xp_progress} / {xp_needed} XP</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("⚔️ Total XP", f"{xp}")
    col2.metric("⚖️ Weight", f"{current_weight} kg")
    col3.metric("🔥 Streak", f"{streak} days")
    col4.metric("📅 Day", now.strftime("%a, %b %d"))

    # Current activity
    st.markdown(f"""
    <div class="quest-active">
        {current_icon} <b>CURRENT QUEST:</b> {current_block}
    </div>
    """, unsafe_allow_html=True)

    # Current month dungeon
    st.markdown(f"""
    <div class="minecraft-block">
        ⛏️ CURRENT DUNGEON: {plan['icon']} {plan['topic']} <br>
        📊 Weight Target: {plan['weight'][0]} → {plan['weight'][1]} kg <br>
        💰 Fiverr Target: Rs {plan['fiverr']}/month
    </div>
    """, unsafe_allow_html=True)


# ============================================
# PAGE: DAILY QUESTS
# ============================================
def page_quests():
    data = load_data()
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    cm = now.hour * 60 + now.minute
    is_wknd = now.weekday() >= 5

    st.markdown('<div class="pixel-title" style="font-size:1rem;">⚔️ DAILY QUESTS</div>', unsafe_allow_html=True)
    st.markdown(f"**{now.strftime('%A, %B %d, %Y')}** — {'Weekend' if is_wknd else 'Weekday'}")

    sched = get_weekend_schedule() if is_wknd else get_weekday_schedule()

    quest_names = [f"{icon} {name}" for _, _, name, _, icon in sched]

    if today not in data.get("daily_quests", {}):
        data.setdefault("daily_quests", {})[today] = [False] * len(quest_names)

    checks = data["daily_quests"][today]
    while len(checks) < len(quest_names):
        checks.append(False)

    xp_earned_today = 0

    for i, (start, end, name, cat, icon) in enumerate(sched):
        s, e = time_to_min(start), time_to_min(end)
        is_current = False
        if e < s:
            is_current = cm >= s or cm < e
        else:
            is_current = s <= cm < e

        col1, col2 = st.columns([1, 8])
        with col1:
            new_val = st.checkbox("", value=checks[i], key=f"q_{today}_{i}")
            if new_val and not checks[i]:
                data = add_xp(data, XP_REWARDS["quest_complete"])
                xp_earned_today += XP_REWARDS["quest_complete"]
            checks[i] = new_val

        with col2:
            if checks[i]:
                css = "quest-done"
                label = f"✅ [{start}-{end}] {icon} {name}"
            elif is_current:
                css = "quest-active"
                label = f"▶️ [{start}-{end}] {icon} {name} ← NOW"
            else:
                css = "quest-card"
                label = f"[{start}-{end}] {icon} {name}"
            st.markdown(f'<div class="{css}">{label}</div>', unsafe_allow_html=True)

    data["daily_quests"][today] = checks
    save_data(data)

    done = sum(checks)
    total = len(checks)
    st.markdown("---")
    st.progress(done / total, text=f"⚔️ {done}/{total} Quests Completed")

    if done == total:
        st.markdown("""
        <div class="system-alert">
            ⚔️ [SYSTEM] ALL DAILY QUESTS COMPLETED!<br>
            You have received bonus XP. The Shadow Monarch approves. 🏆
        </div>
        """, unsafe_allow_html=True)
        st.balloons()


# ============================================
# PAGE: TRAINING (WORKOUT)
# ============================================
def page_training():
    data = load_data()
    today = date.today().strftime("%Y-%m-%d")
    plan = get_plan()

    st.markdown('<div class="pixel-title" style="font-size:1rem;">🏋️ TRAINING GROUNDS</div>', unsafe_allow_html=True)

    # Workout status
    workout_done = data.get("workout_done", {}).get(today, False)

    st.markdown(f"""
    <div class="status-window">
        <div style="color:#888;">TODAY'S TRAINING</div>
        <div style="color:white; font-family:'VT323',monospace; font-size:1.2rem; margin-top:10px;">
            {plan['workout']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    new_val = st.checkbox("⚔️ I completed my training today!", value=workout_done, key="train_today")
    if new_val and not workout_done:
        data = add_xp(data, XP_REWARDS["workout"])
        st.markdown("""
        <div class="system-alert">⚔️ [SYSTEM] Training complete. +20 XP gained. STR increased.</div>
        """, unsafe_allow_html=True)
        st.balloons()
    data.setdefault("workout_done", {})[today] = new_val

    st.markdown("---")

    # Water intake
    st.markdown('<div class="pixel-title" style="font-size:0.8rem;">💧 HYDRATION METER</div>', unsafe_allow_html=True)
    water = data.get("water_intake", {}).get(today, 0)
    water_val = st.slider("Glasses of water (250ml each)", 0, 16, water, key="water_slider")
    data.setdefault("water_intake", {})[today] = water_val

    liters = water_val * 0.25
    water_pct = min(int((water_val / 12) * 100), 100)
    color = "#00ff88" if water_pct >= 100 else "#00b4d8"

    st.markdown(f"""
    <div class="xp-bar-outer" style="border-color:{color};">
        <div class="xp-bar-inner" style="width:{water_pct}%; background:{color};"></div>
        <div class="xp-text">{liters:.1f}L / 3.0L</div>
    </div>
    """, unsafe_allow_html=True)

    if water_pct >= 100:
        if not data.get("water_target_hit", {}).get(today, False):
            data = add_xp(data, XP_REWARDS["water_target"])
            data.setdefault("water_target_hit", {})[today] = True
        st.success("💧 Hydration target HIT! +5 XP")

    st.markdown("---")

    # Workout Streak
    streak = 0
    check = date.today()
    while data.get("workout_done", {}).get(check.strftime("%Y-%m-%d"), False):
        streak += 1
        check -= timedelta(days=1)

    st.markdown(f"""
    <div class="minecraft-block">
        🔥 TRAINING STREAK: {streak} DAYS<br>
        {'🏆 LEGENDARY! Keep it going!' if streak >= 30
         else '💪 GREAT! Dont break the chain!' if streak >= 7
         else '⚔️ Build your streak, Hunter!'}
    </div>
    """, unsafe_allow_html=True)

    # Diet
    st.markdown("---")
    st.markdown('<div class="pixel-title" style="font-size:0.8rem;">🍽️ FUEL PROTOCOL</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="status-window">
        <div style="color:white; font-family:'VT323',monospace; font-size:1.2rem;">
            {plan['diet']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    ate_clean = st.checkbox("🍽️ I ate clean today (no junk!)", key="clean_eat")
    if ate_clean:
        data = add_xp(data, XP_REWARDS["clean_eating"])

    save_data(data)


# ============================================
# PAGE: DUNGEON (AI/ML STUDY)
# ============================================
def page_dungeon():
    data = load_data()
    plan = get_plan()
    month = datetime.now().month

    st.markdown(f"""
    <div class="pixel-title" style="font-size:1rem;">
        ⚔️ DUNGEON: {plan['icon']} {plan['topic'].upper()}
    </div>
    """, unsafe_allow_html=True)

    # Weight target
    st.markdown(f"""
    <div class="minecraft-block">
        📅 Month: {plan['name']} | ⚖️ Weight: {plan['weight'][0]} → {plan['weight'][1]} kg |
        💰 Fiverr: Rs {plan['fiverr']}
    </div>
    """, unsafe_allow_html=True)

    # Videos
    if plan["videos"]:
        st.markdown("### 🎥 Watch These")
        for title, url, week in plan["videos"]:
            st.markdown(f"""
            <div class="resource-link">
                <a href="{url}" target="_blank">▶️ {title}</a>
                <span style="color:#888; float:right;">{week}</span>
            </div>
            """, unsafe_allow_html=True)

    # Readings
    if plan["readings"]:
        st.markdown("### 📖 Read These")
        for title, url in plan["readings"]:
            st.markdown(f"""
            <div class="resource-link">
                <a href="{url}" target="_blank">📖 {title}</a>
            </div>
            """, unsafe_allow_html=True)

    # Deliverables
    st.markdown("### 🎯 Month Deliverables (Dungeon Objectives)")
    month_key = f"del_{month}"

    if month_key not in data.get("deliverables", {}):
        data.setdefault("deliverables", {})[month_key] = [False] * len(plan["tasks"])

    checks = data["deliverables"][month_key]
    while len(checks) < len(plan["tasks"]):
        checks.append(False)

    for i, task in enumerate(plan["tasks"]):
        new_val = st.checkbox(task, value=checks[i], key=f"del_{month}_{i}")
        if new_val and not checks[i]:
            data = add_xp(data, 25)
        checks[i] = new_val

    data["deliverables"][month_key] = checks
    save_data(data)

    done = sum(checks)
    total = len(checks)
    st.progress(done / total, text=f"⚔️ Dungeon Progress: {done}/{total}")

    if done == total:
        st.markdown("""
        <div class="system-alert">
            ⚔️ [SYSTEM] DUNGEON CLEARED!<br>
            All objectives completed. The Hunter grows stronger. 🏆
        </div>
        """, unsafe_allow_html=True)


# ============================================
# PAGE: STATS (WEIGHT + PROGRESS)
# ============================================
def page_stats():
    data = load_data()

    st.markdown('<div class="pixel-title" style="font-size:1rem;">📊 HUNTER STATS</div>', unsafe_allow_html=True)

    # Weight Logger
    st.markdown("### ⚖️ Body Stats")
    col1, col2 = st.columns(2)
    with col1:
        w_date = st.date_input("Date", value=date.today(), key="w_date")
    with col2:
        w_val = st.number_input("Weight (kg)", min_value=50.0, max_value=100.0, value=75.0, step=0.1)

    if st.button("💾 Log Weight", type="primary"):
        data.setdefault("weights", {})[w_date.strftime("%Y-%m-%d")] = w_val
        save_data(data)
        st.success(f"✅ Logged {w_val} kg for {w_date.strftime('%b %d')}")
        data = add_xp(data, 5)
        save_data(data)

    # Weight chart
    weights = data.get("weights", {})
    if weights:
        sorted_dates = sorted(weights.keys())
        chart_data = {d: weights[d] for d in sorted_dates}

        st.markdown("### 📈 Weight Journey")
        st.line_chart(chart_data, use_container_width=True)

        latest = weights[sorted_dates[-1]]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current", f"{latest} kg")
        col2.metric("Start", "75 kg")
        col3.metric("Lost", f"{75 - latest:.1f} kg")
        col4.metric("To Goal", f"{latest - 65:.1f} kg left")

    # Target table
    st.markdown("### 🎯 Monthly Weight Targets")
    targets = [
        ["Mar", "75→74", "1 kg"], ["Apr", "74→73", "1 kg"],
        ["May", "73→71", "2 kg"], ["Jun", "71→70", "1 kg"],
        ["Jul", "70→69", "1 kg"], ["Aug", "69→68", "1 kg"],
        ["Sep", "68→67", "1 kg"], ["Oct", "67→66", "1 kg"],
        ["Nov", "66→65", "1 kg"], ["Dec", "65", "Maintain"],
        ["Jan", "65", "Maintain"], ["Feb", "65", "Maintain"],
    ]
    current_m = datetime.now().strftime("%b")
    for row in targets:
        marker = " ← YOU ARE HERE" if row[0] == current_m else ""
        icon = "🟢" if "Maintain" in row[2] else "🔵"
        st.markdown(f"`{icon} {row[0]}` **{row[1]}** kg — Lose: {row[2]}{marker}")

    st.markdown("---")

    # Overall progress
    st.markdown("### 🏆 Dungeon Completion")
    month_order = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2]
    total_done = 0
    total_all = 0

    for m in month_order:
        p = MONTHLY_PLANS[m]
        month_key = f"del_{m}"
        checks = data.get("deliverables", {}).get(month_key, [])
        d = sum(checks) if checks else 0
        t = len(p["tasks"])
        total_done += d
        total_all += t
        pct = d / t if t > 0 else 0
        status = "✅ CLEARED" if d == t else f"{d}/{t}"
        st.progress(pct, text=f"{p['icon']} {p['name']}: {p['topic']} — {status}")

    overall = total_done / total_all if total_all > 0 else 0
    st.markdown(f"**Overall: {total_done}/{total_all} ({overall*100:.0f}%)**")


# ============================================
# PAGE: GUILD (FIVERR)
# ============================================
def page_guild():
    data = load_data()
    plan = get_plan()

    st.markdown('<div class="pixel-title" style="font-size:1rem;">💰 GUILD MISSIONS (FIVERR)</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="minecraft-block">
        💰 This Month Target: Rs {plan['fiverr']}
    </div>
    """, unsafe_allow_html=True)

    # Log earning
    col1, col2, col3 = st.columns(3)
    with col1:
        e_date = st.date_input("Date", value=date.today(), key="earn_date")
    with col2:
        e_amt = st.number_input("Amount (Rs)", min_value=0, max_value=100000, value=0, step=100)
    with col3:
        e_desc = st.text_input("Gig", placeholder="Python script")

    if st.button("💰 Log Earning", type="primary"):
        data.setdefault("fiverr_earnings", []).append({
            "date": e_date.strftime("%Y-%m-%d"),
            "amount": e_amt,
            "description": e_desc,
        })
        data = add_xp(data, XP_REWARDS["fiverr"])
        save_data(data)
        st.success(f"✅ Logged Rs {e_amt}! +15 XP")

    st.markdown("---")

    earnings = data.get("fiverr_earnings", [])
    if earnings:
        total = sum(e["amount"] for e in earnings)
        this_month = sum(
            e["amount"] for e in earnings
            if datetime.strptime(e["date"], "%Y-%m-%d").month == datetime.now().month
        )
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total Earned", f"Rs {total:,}")
        col2.metric("📅 This Month", f"Rs {this_month:,}")
        col3.metric("📦 Total Orders", len(earnings))

        st.markdown("### Recent Missions")
        for e in reversed(earnings[-10:]):
            st.markdown(f"""
            <div class="quest-done">
                📦 {e['date']} — Rs {e['amount']:,} — {e['description']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("⚔️ No guild missions completed yet. Get that first order, Hunter!")


# ============================================
# PAGE: END OF DAY REVIEW
# ============================================
def page_review():
    data = load_data()
    today = date.today().strftime("%Y-%m-%d")

    st.markdown('<div class="pixel-title" style="font-size:1rem;">🌙 END OF DAY REVIEW</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="system-alert">
        ⚔️ [SYSTEM] Daily quest report required.<br>
        The Shadow Monarch demands accountability.
    </div>
    """, unsafe_allow_html=True)

    existing = data.get("reviews", {}).get(today, {})

    # Daily ratings
    st.markdown("### Rate Your Day")

    col1, col2 = st.columns(2)
    with col1:
        workout_rating = st.select_slider(
            "🏋️ Training", options=["Skipped", "Light", "Medium", "Hard", "Beast Mode"],
            value=existing.get("workout", "Medium"), key="rev_workout"
        )
        study_rating = st.select_slider(
            "📖 Study", options=["0 hrs", "1 hr", "2 hrs", "3 hrs", "3+ hrs"],
            value=existing.get("study", "2 hrs"), key="rev_study"
        )
    with col2:
        diet_rating = st.select_slider(
            "🍽️ Diet", options=["Junk", "Mixed", "Clean", "Very Clean", "Perfect"],
            value=existing.get("diet", "Clean"), key="rev_diet"
        )
        sleep_rating = st.select_slider(
            "😴 Sleep Plan", options=["After 12", "11-12", "10-11", "By 10", "By 9:30"],
            value=existing.get("sleep", "By 10"), key="rev_sleep"
        )

    mood = st.select_slider(
        "🧠 Overall Mood", options=["Terrible", "Bad", "Okay", "Good", "Amazing"],
        value=existing.get("mood", "Good"), key="rev_mood"
    )

    accomplishment = st.text_area(
        "⚔️ What did you accomplish today?",
        value=existing.get("accomplishment", ""),
        placeholder="I completed 2 lectures and solved 5 problems...",
        key="rev_acc"
    )

    tomorrow = st.text_area(
        "🎯 Top 3 goals for tomorrow?",
        value=existing.get("tomorrow", ""),
        placeholder="1. Watch lecture 3\n2. Solve 10 problems\n3. 30 min workout",
        key="rev_tom"
    )

    if st.button("💾 Save Review & Claim XP", type="primary"):
        review = {
            "workout": workout_rating,
            "study": study_rating,
            "diet": diet_rating,
            "sleep": sleep_rating,
            "mood": mood,
            "accomplishment": accomplishment,
            "tomorrow": tomorrow,
        }
        data.setdefault("reviews", {})[today] = review

        # Calculate XP
        xp_gained = 10  # base for doing review
        if workout_rating in ["Hard", "Beast Mode"]:
            xp_gained += 10
        if study_rating in ["3 hrs", "3+ hrs"]:
            xp_gained += 10
        if diet_rating in ["Very Clean", "Perfect"]:
            xp_gained += 5
        if sleep_rating in ["By 10", "By 9:30"]:
            xp_gained += 5

        data = add_xp(data, xp_gained)
        save_data(data)

        st.markdown(f"""
        <div class="system-alert">
            ⚔️ [SYSTEM] Daily report accepted.<br>
            +{xp_gained} XP earned. Rest well, Hunter.<br>
            Tomorrow, we hunt again. ⚔️
        </div>
        """, unsafe_allow_html=True)
        st.balloons()

    # Past reviews
    reviews = data.get("reviews", {})
    if len(reviews) > 1:
        st.markdown("---")
        st.markdown("### 📜 Past Reports")
        for d in sorted(reviews.keys(), reverse=True)[:7]:
            if d == today:
                continue
            r = reviews[d]
            with st.expander(f"📅 {d} — Mood: {r.get('mood', '?')}"):
                st.write(f"🏋️ Training: {r.get('workout', '?')}")
                st.write(f"📖 Study: {r.get('study', '?')}")
                st.write(f"🍽️ Diet: {r.get('diet', '?')}")
                st.write(f"⚔️ Accomplished: {r.get('accomplishment', '?')}")


# ============================================
# PAGE: RESOURCES
# ============================================
def page_resources():
    st.markdown('<div class="pixel-title" style="font-size:1rem;">📚 INVENTORY (RESOURCES)</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📚 Books", "🎥 Courses", "📝 Cheat Sheets", "🛠️ Tools"])

    with tab1:
        books = [
            ("Automate the Boring Stuff", "https://automatetheboringstuff.com/", "Python"),
            ("Python DS Handbook", "https://jakevdp.github.io/PythonDataScienceHandbook/", "Data"),
            ("Mathematics for ML", "https://mml-book.github.io/", "Math"),
            ("ISLR (ML Textbook)", "https://www.statlearning.com/", "ML"),
            ("Dive into Deep Learning", "https://d2l.ai/", "DL"),
            ("Deep Learning - Goodfellow", "https://www.deeplearningbook.org/", "DL"),
            ("Neural Networks and DL", "http://neuralnetworksanddeeplearning.com/", "DL"),
            ("Speech and Language Processing", "https://web.stanford.edu/~jurafsky/slp3/", "NLP"),
            ("ML Interviews Book", "https://huyenchip.com/ml-interviews-book/", "Interview"),
        ]
        for title, url, topic in books:
            st.markdown(f"""
            <div class="resource-link">
                <a href="{url}" target="_blank">📖 {title}</a>
                <span style="color:#888; float:right;">{topic}</span>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        courses = [
            ("CS50P - Harvard", "https://www.youtube.com/watch?v=nLRL_NcnK-4"),
            ("Andrew Ng ML", "https://www.coursera.org/specializations/machine-learning-introduction"),
            ("3B1B - Neural Networks", "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi"),
            ("Karpathy - NN Zero to Hero", "https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ"),
            ("Daniel Bourke - PyTorch", "https://www.youtube.com/watch?v=Z_ikDlimN6A"),
            ("Stanford CS224n (NLP)", "https://www.youtube.com/playlist?list=PLoROMvodv4rMFqRtEuo6SGjY4XbRIVRd4"),
            ("Hugging Face NLP", "https://huggingface.co/learn/nlp-course"),
            ("DeepLearning.AI Courses", "https://www.deeplearning.ai/short-courses/"),
        ]
        for title, url in courses:
            st.markdown(f"""
            <div class="resource-link">
                <a href="{url}" target="_blank">🎥 {title}</a>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        sheets = [
            ("Stanford CS229 ML", "https://stanford.edu/~shervine/teaching/cs-229/"),
            ("Stanford CS230 DL", "https://stanford.edu/~shervine/teaching/cs-230/"),
            ("Stanford CS231n CNN", "https://cs231n.github.io/"),
            ("Jay Alammar Visual Guides", "https://jalammar.github.io/"),
            ("learnpytorch.io", "https://www.learnpytorch.io/"),
            ("ML Glossary", "https://ml-glossary.readthedocs.io/"),
            ("Prompt Engineering Guide", "https://www.promptingguide.ai/"),
        ]
        for title, url in sheets:
            st.markdown(f"""
            <div class="resource-link">
                <a href="{url}" target="_blank">📝 {title}</a>
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        tools = [
            ("Google Colab (Free GPU)", "https://colab.research.google.com/"),
            ("Kaggle", "https://www.kaggle.com/"),
            ("Hugging Face", "https://huggingface.co/"),
            ("GitHub", "https://github.com/"),
            ("HackerRank Python", "https://www.hackerrank.com/domains/python"),
            ("Streamlit Cloud (Deploy)", "https://streamlit.io/cloud"),
        ]
        for title, url in tools:
            st.markdown(f"""
            <div class="resource-link">
                <a href="{url}" target="_blank">🛠️ {title}</a>
            </div>
            """, unsafe_allow_html=True)


# ============================================
# MAIN APP
# ============================================
def main():
    data = load_data()

    # Sidebar
    xp = data.get("xp", 0)
    level = get_level(xp)
    rank_letter, rank_title, rank_class = get_rank(level)

    st.sidebar.markdown(f"""
    <div style="text-align:center; padding:10px;">
        <div class="pixel-title" style="font-size:0.7rem;">SHADOW SYSTEM</div>
        <div class="rank-badge {rank_class}" style="font-size:1rem; margin:10px 0;">
            {rank_letter}-Rank
        </div>
        <div style="color:white; font-family:'Orbitron',monospace;">
            {data.get('player_name', 'Player')}
        </div>
        <div style="color:#888; font-size:0.8rem;">
            Level {level} | {xp} XP
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "⚔️ Navigate",
        [
            "🏠 Status Window",
            "⚔️ Daily Quests",
            "🏋️ Training",
            "📖 Dungeon (Study)",
            "📊 Hunter Stats",
            "💰 Guild (Fiverr)",
            "🌙 End of Day",
            "📚 Inventory",
        ],
    )

    # Sidebar quick info
    st.sidebar.markdown("---")
    now = datetime.now()
    st.sidebar.markdown(f"📅 {now.strftime('%a, %b %d')}")
    st.sidebar.markdown(f"🕐 {now.strftime('%I:%M %p')}")

    block_name, _, block_icon = get_current_block()
    st.sidebar.markdown(f"{block_icon} {block_name}")

    weights = data.get("weights", {})
    if weights:
        latest = weights[sorted(weights.keys())[-1]]
        st.sidebar.metric("⚖️ Weight", f"{latest} kg")

    # Route
    if page == "🏠 Status Window":
        page_status()
    elif page == "⚔️ Daily Quests":
        page_quests()
    elif page == "🏋️ Training":
        page_training()
    elif page == "📖 Dungeon (Study)":
        page_dungeon()
    elif page == "📊 Hunter Stats":
        page_stats()
    elif page == "💰 Guild (Fiverr)":
        page_guild()
    elif page == "🌙 End of Day":
        page_review()
    elif page == "📚 Inventory":
        page_resources()


if __name__ == "__main__":
    main()