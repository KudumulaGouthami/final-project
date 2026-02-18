



# ---------------- QUIZ PAGE ----------------
if st.session_state.stage == "quiz" and st.session_state.user:

    st.sidebar.success(f"👤 Logged in as: {st.session_state.user}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.user = None
        st.session_state.stage = "home"
        st.rerun()

    st.title("🧩 Smart Quiz Application")
    st.markdown("Select a category and start your quiz!")

    # ---------------------------------------
    # START QUIZ SETUP (SHUFFLE + NO REPEAT)
    # ---------------------------------------
    if "quiz" not in st.session_state:

        cat = st.selectbox("📚 Category", list(quizzes.keys()))
        num_q = st.number_input(
            "Number of questions",
            1,
            len(quizzes[cat]),
            min(5, len(quizzes[cat]))
        )

        if st.button("Start Quiz ▶"):

            # track used questions
            if "used_questions" not in st.session_state:
                st.session_state.used_questions = []

            pool = [q for q in quizzes[cat]
                    if q not in st.session_state.used_questions]

            # reset if all used
            if len(pool) < num_q:
                st.session_state.used_questions = []
                pool = quizzes[cat].copy()

            random.shuffle(pool)
            selected = pool[:num_q]

            st.session_state.used_questions.extend(selected)

            st.session_state.quiz = selected
            st.session_state.page = 0
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.session_state.cat = cat

            st.rerun()

        st.stop()

    # ---------------------------------------
    # TIMER (AUTO REFRESH EVERY SECOND)
    # ---------------------------------------
    st.experimental_autorefresh(interval=1000, key="timer")

    quiz = st.session_state.quiz
    page = st.session_state.page
    total = len(quiz)

    total_time = 20
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, total_time - elapsed)

    st.markdown(
        f"<div class='timer'>⏳ Time Left: {remaining} seconds</div>",
        unsafe_allow_html=True
    )

    # auto next when time over
    if remaining <= 0:
        st.warning("⏰ Time's up!")
        st.session_state.page += 1
        st.session_state.start_time = time.time()
        st.rerun()

    # ---------------------------------------
    # FINISH PAGE
    # ---------------------------------------
    if page >= total:

        st.balloons()
        st.success(f"🎉 Quiz Completed — Score: {st.session_state.score}/{total}")

        username = st.session_state.user
        score_data = {
            "score": st.session_state.score,
            "total": total,
            "category": st.session_state.cat,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        users[username]["scores"].append(score_data)
        save_data(USER_FILE, users)

        leaderboard[username] = max(s["score"] for s in users[username]["scores"])
        save_data(LEADERBOARD_FILE, leaderboard)

        st.subheader("🏆 Leaderboard (Top 5)")
        for i, (u, sc) in enumerate(
            sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)[:5], 1
        ):
            st.write(f"{i}. {u} — {sc} points")

        if st.button("🔁 Restart"):
            for k in ["quiz", "page", "score", "cat", "start_time"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

        st.stop()

    # ---------------------------------------
    # QUESTION PAGE
    # ---------------------------------------
    q = quiz[page]

    st.markdown(f"### Q{page+1}. {q['question']}")

    choice = st.radio(
        "Choose an answer:",
        q["options"],
        key=f"q{page}"
    )

    if st.button("Next ➡"):

        if choice == q["answer"]:
            st.session_state.score += 1
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Wrong! Correct: {q['answer']}")

        time.sleep(1)

        st.session_state.page += 1
        st.session_state.start_time = time.time()

        st.rerun()
