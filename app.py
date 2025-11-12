from flask import Flask, render_template, request, redirect, session
import sqlite3, random, os

app = Flask(__name__)
app.secret_key = "animated_quiz_secret"
DB = "quiz.db"

# ---------- DATABASE SETUP ----------
def init_db():
    if not os.path.exists(DB):
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("CREATE TABLE questions(id INTEGER PRIMARY KEY, question TEXT, a TEXT, b TEXT, c TEXT, d TEXT, answer TEXT)")
        questions = [
            ("What is 2 + 2?", "3", "4", "5", "6", "b"),
            ("Which keyword defines a function in Python?", "func", "def", "lambda", "define", "b"),
            ("What is the capital of France?", "Berlin", "Madrid", "Paris", "Rome", "c"),
            ("HTML stands for?", "HighText Machine Language", "Hyper Text Markup Language", "Hyper Transfer Markup Language", "None", "b"),
            ("Which planet is known as the Red Planet?", "Earth", "Venus", "Mars", "Jupiter", "c")
        ]
        cur.executemany("INSERT INTO questions(question,a,b,c,d,answer) VALUES (?,?,?,?,?,?)", questions)
        con.commit()
        con.close()

# ---------- ROUTES ----------
@app.route('/')
def home():
    session.clear()
    return render_template('home.html')

@app.route('/start', methods=['POST'])
def start():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM questions")
    questions = cur.fetchall()
    con.close()

    random.shuffle(questions)
    session['questions'] = questions
    session['index'] = 0
    session['score'] = 0

    return redirect('/question')

@app.route('/question', methods=['GET', 'POST'])
def question():
    if 'questions' not in session:
        return redirect('/')
    index = session['index']
    questions = session['questions']

    if request.method == 'POST':
        selected = request.form.get('option')
        correct = questions[index - 1][6]
        if selected == correct:
            session['score'] += 1

    if index >= len(questions):
        return redirect('/result')

    q = questions[index]
    session['index'] += 1
    return render_template('question.html', q=q, index=index + 1, total=len(questions))

@app.route('/result')
def result():
    score = session.get('score', 0)
    total = len(session.get('questions', []))
    return render_template('result.html', score=score, total=total)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
