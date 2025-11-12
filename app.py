



import streamlit as st
import json
import os
import time
import random
from datetime import datetime
import streamlit.components.v1 as components

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Smart Quiz App", page_icon="🎯", layout="centered")

# -------------------- CSS STYLES --------------------
st.markdown("""
<style>
body {
    background: linear-gradient(-45deg, #f9d423, #ff4e50, #a1c4fd, #c2e9fb);
    background-size: 400% 400%;
    animation: gradientShift 12s ease infinite;
    font-family: 'Poppins', sans-serif;
}
@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
h1, h2, h3 {
    text-align: center;
    color: #333;
}
.login-box {
    background: rgba(255,255,255,0.9);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 6px 25px rgba(0,0,0,0.3);
    width: 90%;
    max-width: 400px;
    margin: auto;
    animation: fadeIn 1s ease-in;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(25px);}
    to {opacity: 1; transform: translateY(0);}
}
.stButton>button {
    background: linear-gradient(to right, #667eea, #764ba2);
    color: white;
    border-radius: 8px;
    font-size: 16px;
    padding: 8px 18px;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {
    background: linear-gradient(to right, #764ba2, #667eea);
    transform: scale(1.05);
}
.quiz-logo {
    display: block;
    margin: 0 auto 10px auto;
    width: 120px;
    animation: spin 12s linear infinite;
}
@keyframes spin {
    from {transform: rotate(0deg);}
    to {transform: rotate(360deg);}
}
.timer {
    color: #d32f2f;
    font-weight: bold;
    font-size: 20px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -------------------- DATA FILES --------------------
USER_FILE = "users.json"
LEADERBOARD_FILE = "leaderboard.json"

def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

users = load_data(USER_FILE)
leaderboard = load_data(LEADERBOARD_FILE)

# -------------------- QUIZ BANK --------------------
quizzes = {
    "Programming": [
        {"question": "Which company developed Java?", "options": ["Microsoft", "Oracle", "Sun Microsystems", "Google"], "answer": "Sun Microsystems"},
        {"question": "Which symbol is used for comments in Python?", "options": ["#", "//", "/* */", "<!-- -->"], "answer": "#"},
        {"question": "HTML stands for?", "options": ["Hyper Text Markup Language", "HighText Machine Language", "Hyperlinks and Text Markup Language", "None"], "answer": "Hyper Text Markup Language"},
        {"question": "CSS stands for?", "options": ["Cascading Style Sheets", "Color Style Syntax", "Coding Style System", "Central Sheet Style"], "answer": "Cascading Style Sheets"},
        {"question": "Which keyword is used to create a function in Python?", "options": ["def", "func", "lambda", "function"], "answer": "def"},
        {"question": "Which tag is used to link CSS in HTML?", "options": ["<css>", "<style>", "<link>", "<script>"], "answer": "<link>"}
    ],
    "Maths": [
        {"question": "What is 12 × 8?", "options": ["80", "96", "88", "108"], "answer": "96"},
        {"question": "The square root of 144 is?", "options": ["10", "11", "12", "13"], "answer": "12"},
        {"question": "What is 15% of 200?", "options": ["25", "30", "35", "20"], "answer": "30"},
        {"question": "Solve: (10 + 2) × 3", "options": ["30", "36", "25", "40"], "answer": "36"},
        {"question": "What is 7 + 6 × 5?", "options": ["65", "37", "35", "47"], "answer": "37"}
    ],
    "General Knowledge": [
        {"question": "Who was the first President of India?", "options": ["Dr. Rajendra Prasad", "Jawaharlal Nehru", "Indira Gandhi", "APJ Abdul Kalam"], "answer": "Dr. Rajendra Prasad"},
        {"question": "Which is the national bird of India?", "options": ["Sparrow", "Peacock", "Crow", "Parrot"], "answer": "Peacock"},
        {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "answer": "Mars"},
        {"question": "Who wrote the National Anthem?", "options": ["Rabindranath Tagore", "Bankim Chandra", "Sarojini Naidu", "Mahatma Gandhi"], "answer": "Rabindranath Tagore"},
        {"question": "Which is the largest ocean on Earth?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": "Pacific"}
    ]
}

# -------------------- LOGIN SYSTEM --------------------
if "user" not in st.session_state:
    st.session_state.user = None

def register_user(username, password):
    if not username or not password:
        return False, "Please enter username and password."
    if username in users:
        return False, "⚠️ Username already exists!"
    users[username] = {"password": password, "scores": []}
    save_data(USER_FILE, users)
    return True, "✅ Registration successful!"

def login_user(username, password):
    if username in users and users[username]["password"] == password:
        st.session_state.user = username
        return True, "✅ Login successful!"
    return False, "❌ Invalid credentials."

# -------------------- LOGIN / REGISTER SLIDES --------------------
if st.session_state.user is None:
    slide = st.radio("Select Page:", ["🌟 Login", "📝 Register"], horizontal=True)
    if slide == "🌟 Login":
        st.image("https://i.pinimg.com/originals/2f/d8/0b/2fd80b21c1ff8022a2b6c1e5de032eb5.gif", caption="Welcome Back!", use_container_width=True)
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.subheader("🔐 Login to Continue")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            ok, msg = login_user(username, password)
            st.info(msg)
            if ok:
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.image("https://i.pinimg.com/originals/d3/06/7e/d3067e2d7d2d6f9a12dfbd00b9985b07.gif", caption="Create Your Account", use_container_width=True)
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.subheader("📝 Register")
        username = st.text_input("Choose Username")
        password = st.text_input("Choose Password", type="password")
        if st.button("Register"):
            ok, msg = register_user(username, password)
            st.info(msg)
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# -------------------- MAIN QUIZ LOGIC --------------------
st.sidebar.success(f"👤 Logged in as: {st.session_state.user}")
if st.sidebar.button("🚪 Logout"):
    st.session_state.user = None
    for k in ["category", "difficulty", "page", "score", "quiz", "answers", "start_time"]:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()

st.title("🧩 Smart Quiz Application")
st.markdown("Test your skills — choose category and difficulty, then start!")

if st.session_state.get("quiz") is None:
    cat = st.selectbox("📚 Select Category", list(quizzes.keys()))
    diff = st.selectbox("🎚️ Select Difficulty", ["Easy", "Medium", "Hard"])
    max_q = len(quizzes[cat])
    num_q = st.number_input(f"Number of questions (1 to {max_q})", 1, max_q, min(5, max_q))

    if st.button("Start Quiz ▶️"):
        selected = random.sample(quizzes[cat], num_q)
        st.session_state.quiz = selected
        st.session_state.page = 0
        st.session_state.score = 0
        st.session_state.answers = {}
        st.session_state.category = cat
        st.session_state.difficulty = diff
        st.session_state.start_time = time.time()
        st.rerun()
    st.stop()

quiz = st.session_state.quiz
page = st.session_state.get("page", 0)
total = len(quiz)
timer_limit = {"Easy": 25, "Medium": 15, "Hard": 10}[st.session_state.get("difficulty", "Medium")]

if page >= total:
    st.balloons()
    st.success(f"🎉 Quiz Completed — Score: {st.session_state.get('score',0)}/{total}")
    percent = (st.session_state.get('score',0) / total) * 100
    feedback = "🌟 Excellent!" if percent == 100 else "👏 Great job!" if percent >= 75 else "🙂 Keep learning!" if percent >= 50 else "😅 Try again!"
    st.info(feedback)
    username = st.session_state.user
    users.setdefault(username, {"password": users.get(username, {}).get("password",""), "scores": []})
    score_data = {"score": st.session_state.get('score',0), "total": total, "category": st.session_state.get('category'), "difficulty": st.session_state.get('difficulty'), "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    users[username]["scores"].append(score_data)
    save_data(USER_FILE, users)
    leaderboard[username] = max(s["score"] for s in users[username]["scores"])
    save_data(LEADERBOARD_FILE, leaderboard)
    st.subheader("🏆 Leaderboard (Top 5)")
    for i, (u, sc) in enumerate(sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)[:5], 1):
        st.write(f"{i}. **{u}** — {sc} points")
    st.markdown("### 📊 Your Past Scores:")
    for entry in users[username]["scores"]:
        st.write(f"🕒 {entry['date']} — **{entry['score']} / {entry['total']}** ({entry['category']} / {entry['difficulty']})")
    if st.button("🔁 Restart Quiz"):
        for k in ["category", "difficulty", "page", "score", "quiz", "answers", "start_time"]:
            if k in st.session_state: del st.session_state[k]
        st.rerun()
    st.stop()

# -------------------- QUESTION SECTION --------------------
q = quiz[page]
st.markdown(f"### Q{page+1}. {q['question']}")
elapsed = int(time.time() - st.session_state.get("start_time", time.time()))
remaining = max(0, timer_limit - elapsed)

# Build JS safely with .format and escaped JS braces
js = """
<div class='timer'>⏳ Time Left: <span id='cd'>{}</span> seconds</div>
<script>
let t={};
const el=document.getElementById('cd');
const interval=setInterval(function() {{
    t--;
    if (t <= 0) {{
        clearInterval(interval);
        // trigger auto-next by reloading with param
        const url = new URL(window.location.href);
        url.searchParams.set('auto_next', '1');
        window.location.href = url.toString();
    }}
    el.innerText = t;
}}, 1000);
</script>
""".format(remaining, remaining)

components.html(js, height=90)

choice = st.radio("Choose an answer:", q["options"], key=f"q{page}")
if st.button("Next ➡️"):
    st.session_state.answers[page] = choice
    if choice == q["answer"]:
        st.session_state.score = st.session_state.get("score", 0) + 1
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Wrong! Correct answer: {q['answer']}")
    st.session_state.page = page + 1
    st.session_state.start_time = time.time()
    st.rerun()
