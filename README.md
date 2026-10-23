# CodeDuel ⚔️

A real-time 1v1 competitive programming arena where you can duel friends or random players on classic Data Structures & Algorithms problems.

Built because practicing LeetCode alone gets boring — racing someone live with a timer and passing test cases in real-time is way more fun.

---

## What you can do

- **1v1 Live Duels**: Create a private room and send the 6-letter room code to a friend, or jump into the ranked matchmaking queue to get paired automatically.
- **In-Browser Monaco Editor**: Full VS Code-like coding workspace with syntax highlighting, auto-indentation, and multi-language support (**Python**, **C++**, **C**, and **JavaScript**).
- **Instant Test Evaluation**: Code runs in an isolated runner with strict timeouts. You see your output, expected output, and execution time in milliseconds.
- **20 Curated DSA Problems**: From Easy warmups (Two Sum, Valid Parentheses, Binary Search) to Medium classics (Longest Substring, 3Sum, Coin Change) and Hard challenges (Trapping Rain Water, Edit Distance).
- **Elo Ratings & Leaderboard**: Earn points when you win ranked matches, build win streaks, and climb the leaderboard.
- **Guest Mode / Instant Play**: You don't even have to sign up to test it — click **"Instant Guest Play"** and start coding right away.

---

## Quick Setup (Run it locally)

### 1. Backend (Django + WebSockets)

Make sure you have **Python 3.10+** installed.

```bash
cd backend

# Create and activate a virtual environment
# Windows:
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux:
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations & seed the 20 problems + demo user
python manage.py migrate
python manage.py seed_problems

# Start server with Daphne (handles both HTTP & WebSockets)
daphne -b 127.0.0.1 -p 8000 codeduel.asgi:application
```

The backend will be running at `http://127.0.0.1:8000`.

> **Note on logging in:** If you want to sign in immediately without registering, use the pre-seeded demo account:
> - **Username**: `demo_coder`
> - **Password**: `password123`
> Or click **"Instant Guest Play"** in the app.

---

### 2. Frontend (React + Vite)

In a separate terminal:

```bash
cd frontend

# Install packages
npm install

# Start the dev server
npm run dev
```

Open your browser at `http://localhost:5173`. That's it!

---

## Included Problems (20 Total)

The database comes pre-seeded with 20 classic algorithmic challenges:

| Level | Problems |
|---|---|
| **Easy** | Two Sum, Valid Parentheses, Palindrome Number, Best Time to Buy and Sell Stock, Reverse String, Valid Anagram, Binary Search, Climbing Stairs, Merge Two Sorted Arrays |
| **Medium** | Maximum Subarray, Container With Most Water, Longest Substring Without Repeating Characters, Coin Change, 3Sum, Rotate Image, Longest Palindromic Substring, Word Break |
| **Hard** | Trapping Rain Water, Median of Two Sorted Arrays, Edit Distance |

Each problem includes clear input/output rules, constraints, sample test cases, hidden evaluation tests, and starter code for Python, C++, and JavaScript.

---

## Tech Stack

- **Frontend**: React 19, Vite, Monaco Editor, Lucide Icons, Canvas Confetti.
- **Backend**: Python, Django 5, Django REST Framework, Django Channels (WebSockets).
- **ASGI Server**: Daphne.
- **Database**: SQLite locally, PostgreSQL on production via `DATABASE_URL`.
- **Code Execution**: Isolated subprocess runner with CPU & timeout safety limits.

---

## Project Structure

```text
CodeDuel/
├── backend/
│   ├── authentication/     # Login, register, guest mode, leaderboard
│   ├── battles/            # 1v1 rooms, matchmaking queue, WebSockets
│   ├── problems/           # 20 seeded DSA problems and test suites
│   ├── submissions/        # Code execution engine (Python, C++, C, JS)
│   ├── codeduel/           # Django settings, asgi, and urls
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # BattleLobby, BattleRoom, CodeWorkspace, ProblemLibrary, etc.
│   │   ├── services/       # REST API & WebSocket managers
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
└── README.md
```

---

## Deployment Notes

- **Backend**: Ready for [Render](https://render.com) using the included `render.yaml` and `build.sh`.
- **Frontend**: Ready for [Vercel](https://vercel.com) using the included `frontend/vercel.json`. Just set `VITE_API_URL` to your backend URL.

---

## Contributing & Feedback

Feel free to open an issue or pull request if you want to add more problems, support new languages, or improve the UI!
