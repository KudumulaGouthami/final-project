

import streamlit as st
import json
import os
import time
from datetime import datetime
import streamlit.components.v1 as components

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Quiz Application",
    page_icon="🧩",
    layout="centered"
)

# -------------------- CUSTOM STYLES --------------------
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #b3e5fc 0%, #e1f5fe 100%);
        }
        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        h1, h2, h3 {
            text-align: center;
            color: #333333;
        }
        .timer {
            color: #e53935;
            font-weight: bold;
            font-size: 20px;
            text-align: center;
        }
        .stButton>button {
            background-color: #007BFF;
            color: white;
            border-radius: 10px;
            padding: 8px 18px;
            font-size: 16px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- QUIZ QUESTIONS --------------------
quiz = [
    {"question": "Which language is known as the brain of the computer?",
     "options": ["Python", "C", "Java", "CPU"], "answer": "CPU"},
    {"question": "Which of these is a Python web framework?",
     "options": ["Django", "TensorFlow", "NumPy", "Pandas"], "answer": "Django"},
    {"question": "HTML stands for?",
     "options": ["Hyper Trainer Marking Language", "Hyper Text Markup Language",
                 "Hyper Text Markdown Language", "None of these"], "answer": "Hyper Text Markup Language"},
    {"question": "What does CSS stand for?",
     "options": ["Cascading Style Sheets", "Computer Style Sheet",
                 "Creative Style System", "Colorful Style Sheet"], "answer": "Cascading Style Sheets"},
    {"question": "Which of the following is a database?",
     "options": ["MySQL", "NumPy", "React", "Pandas"], "answer": "MySQL"}
]

# -------------------- FILES --------------------
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

# -------------------- LOGIN / REGISTER --------------------
if "user" not in st.session_state:
    st.session_state.user = None


def register_user(username, password):
    if username in users:
        return False, "⚠️ Username already exists."
    users[username] = {"password": password, "scores": []}
    save_data(USER_FILE, users)
    return True, "✅ Registration successful! Please login."


def login_user(username, password):
    if username in users and users[username]["password"] == password:
        st.session_state.user = username
        return True, "✅ Login successful!"
    return False, "❌ Invalid username or password."


# -------------------- BACKGROUND MUSIC --------------------
st.markdown("""
    <audio autoplay loop>
        <source src="https://cdn.pixabay.com/audio/2022/03/15/audio_7e7e77b1b0.mp3" type="audio/mpeg">
    </audio>
""", unsafe_allow_html=True)

# -------------------- HANDLE auto_next param (triggered by client JS) --------------------
params = st.experimental_get_query_params()
if "auto_next" in params:
    # advance page automatically (record no answer)
    if "page" in st.session_state:
        # record unanswered as None so we keep history consistent
        idx = st.session_state.get("page", 0)
        st.session_state.answers[idx] = None
        st.session_state.page = idx + 1
    else:
        st.session_state.page = 1
    # reset start time for next question
    st.session_state.start_time = time.time()
    # clear query params and rerun
    st.experimental_set_query_params()
    st.experimental_rerun()

# -------------------- LOGIN PAGE --------------------
if st.session_state.user is None:
    st.title("🧩 Welcome to the Quiz App")
    menu = st.radio("Select Option:", ["Login", "Register"])

    if menu == "Login":
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            success, message = login_user(username, password)
            st.info(message)
            if success:
                time.sleep(1)
                st.experimental_rerun()

    elif menu == "Register":
        username = st.text_input("Choose Username", key="reg_username")
        password = st.text_input("Choose Password", type="password", key="reg_password")
        if st.button("Register"):
            success, message = register_user(username, password)
            st.info(message)

else:
    # -------------------- SIDEBAR --------------------
    st.sidebar.success(f"👤 Logged in as: {st.session_state.user}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.user = None
        for key in ["page", "score", "answers", "start_time"]:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()

    # -------------------- QUIZ LOGIC --------------------
    st.title("🎯 Quiz Application")
    st.markdown("### Test your knowledge with timer, music & leaderboard!")

    # initialize session state keys
    if "page" not in st.session_state:
        st.session_state.page = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    page = st.session_state.page
    total_questions = len(quiz)
    timer_limit = 15  # seconds per question

    # If all questions done, show results
    if page >= total_questions:
        st.balloons()
        st.success("🎉 Quiz Completed!")
        st.write(f"**Your Score: {st.session_state.score} / {total_questions}**")

        username = st.session_state.user
        if username not in users:
            users[username] = {"password": "", "scores": []}

        score_data = {
            "score": st.session_state.score,
            "total": total_questions,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        users[username].setdefault("scores", []).append(score_data)
        save_data(USER_FILE, users)

        # Update leaderboard
        leaderboard[username] = max(s["score"] for s in users[username]["scores"])
        save_data(LEADERBOARD_FILE, leaderboard)

        # Leaderboard display
        st.subheader("🏆 Leaderboard (Top 5)")
        sorted_lb = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
        for rank, (user, score) in enumerate(sorted_lb[:5], 1):
            st.write(f"{rank}. **{user}** — {score} points")

        # Past scores
        st.markdown("### 📊 Your Past Scores:")
        for entry in users[username]["scores"]:
            st.write(f"🕒 {entry['date']} — **{entry['score']} / {entry['total']}**")

        if st.button("🔁 Restart Quiz"):
            for key in ["page", "score", "answers", "start_time"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()
        st.stop()

    # Show question
    question = quiz[page]
    st.markdown(f"### Q{page+1}. {question['question']}")

    # compute remaining time (server-side)
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, timer_limit - elapsed)

    # Show JS-driven live timer and auto-redirect when time hits 0
    # We pass the remaining seconds and the auto-next URL param.
    # The JS counts down on the client; when it reaches 0 it sets ?auto_next=1 which we handled above.
    js_html = f"""
    <div style="text-align:center; font-weight:bold; font-size:20px; color:#e53935;">
      ⏳ Time left: <span id="countdown">{remaining}</span> seconds
    </div>
    <script>
      const start = Date.now();
      let remaining = {remaining};
      const el = document.getElementById("countdown");
      // update display every second
      const interval = setInterval(() => {{
          remaining -= 1;
          if (remaining <= 0) {{
              el.innerText = 0;
              clearInterval(interval);
              // redirect to same page adding auto_next param to trigger server-side advance
              const url = new URL(window.location.href);
              url.searchParams.set('auto_next', '1');
              window.location.href = url.toString();
          }} else {{
              el.innerText = remaining;
          }}
      }}, 1000);
    </script>
    """
    components.html(js_html, height=60)

    # present options
    choice = st.radio("Choose an answer:", question["options"], key=f"q{page}")

    # If user clicks Next: record answer and advance
    if st.button("Next ➡️"):
        st.session_state.answers[page] = choice
        if choice == question["answer"]:
            st.session_state.score += 1
        st.session_state.page += 1
        st.session_state.start_time = time.time()
        # remove any auto_next param if present (defensive)
        st.experimental_set_query_params()
        st.experimental_rerun()
