# ⚔️ CodeDuel — Real-Time Competitive Programming Arena

[![React](https://img.shields.io/badge/React-19.3-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-8.3-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django Channels](https://img.shields.io/badge/Channels-WebSockets-20B2AA?logo=websocket&logoColor=white)](https://channels.readthedocs.io/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Monaco Editor](https://img.shields.io/badge/Monaco_Editor-4.7-blue?logo=visualstudiocode&logoColor=white)](https://microsoft.github.io/monaco-editor/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **CodeDuel** is a high-speed, real-time 1v1 competitive programming platform and algorithmic arena. Go head-to-head against friends or match with peers globally, write code in the in-browser Monaco IDE, pass test cases against a low-latency sandboxed execution engine, and climb the global Elo leaderboard.

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [🧩 Curated Problem Library (20 Problems)](#-curated-problem-library-20-problems)
- [🏗️ System Architecture](#️-system-architecture)
- [🛠️ Tech Stack](#️-tech-stack)
- [📂 Project Structure](#-project-structure)
- [🚀 Quick Start & Local Setup](#-quick-start--local-setup)
  - [Prerequisites](#prerequisites)
  - [1. Backend Setup (Django + Channels)](#1-backend-setup-django--channels)
  - [2. Frontend Setup (React + Vite)](#2-frontend-setup-react--vite)
- [⚙️ Environment Variables](#️-environment-variables)
- [📡 API & WebSocket Reference](#-api--websocket-reference)
- [🚢 Production Deployment](#-production-deployment)
  - [Backend Deployment (Render)](#backend-deployment-render)
  - [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

- **⚔️ Real-Time 1v1 Battle Arena**:
  - **Quick Matchmaking Queue**: One-click matchmaking with difficulty preference (`EASY`, `MEDIUM`, `HARD`, or `ANY`).
  - **Custom Room Codes**: Create private battle rooms, share unique codes with friends, and start duels seamlessly.
  - **Synchronized Battle Timers & Countdowns**: Simultaneous countdown and match timers powered by WebSockets.
  - **Instant Victory Resolution**: Real-time winner determination the second all hidden and sample tests pass.

- **💻 High-Performance Code Workspace**:
  - Integrated with **Monaco Editor** (the engine behind VS Code) with syntax highlighting, automatic indentation, and code completion.
  - Multi-language support: **Python 3**, **C++ (g++)**, **C (gcc)**, and **JavaScript (Node.js)**.
  - Clean starter templates provided for every supported language and problem.

- **🧪 Sandboxed Code Execution Engine**:
  - Multi-tier isolated execution with strict timeouts (default 2.0s limit per test case).
  - Instant verdicts: `ACCEPTED`, `WRONG_ANSWER`, `TIME_LIMIT_EXCEEDED`, `COMPILATION_ERROR`, and `RUNTIME_ERROR`.
  - Comprehensive sample and hidden test case evaluation with execution time metrics (ms).

- **🏆 Elo Rating System & Leaderboard**:
  - Dynamic Elo rating updates (+/- rating) calculated based on opponent rating differentials.
  - Detailed user profiles displaying total battles, wins, losses, win rates, and ranking tier badges.

- **🌐 Live Presence & Real-Time Sync**:
  - Live indicator of online programmers and active matches.
  - Full-duplex WebSocket channels delivering opponent submission notifications, verdict flashes, and match results.
  - Interactive confetti animations on victory!

---

## 🧩 Curated Problem Library (20 Problems)

CodeDuel features **20 battle-tested DSA problems** with sample and hidden test cases, complete starter code in Python, C++, and JavaScript, and input/output specifications.

| # | Problem Title | Difficulty | Algorithm / Pattern | Description Summary |
|---|---|:---:|---|---|
| **1** | [Two Sum](#-features) | `EASY` | Hash Map / Arrays | Find two numbers in an array that sum to a target value. |
| **2** | [Valid Parentheses](#-features) | `EASY` | Stack / Strings | Check if brackets `()`, `{}`, `[]` are properly opened and closed in order. |
| **3** | [Palindrome Number](#-features) | `EASY` | Math / Two Pointers | Determine if an integer reads the same backward as forward. |
| **4** | [Best Time to Buy & Sell Stock](#-features) | `EASY` | Greedy / Dynamic Programming | Maximize profit by picking the optimal single day to buy and sell. |
| **5** | [Maximum Subarray](#-features) | `MEDIUM` | Kadane's Algorithm | Find the contiguous subarray with the largest sum. |
| **6** | [Container With Most Water](#-features) | `MEDIUM` | Two Pointers | Compute the maximum water a pair of vertical lines can trap. |
| **7** | [Longest Substring Without Repeating](#-features) | `MEDIUM` | Sliding Window / Hash Set | Find the length of the longest substring with all unique characters. |
| **8** | [Coin Change](#-features) | `MEDIUM` | Dynamic Programming / BFS | Fewest coins needed to make up a given amount, or -1 if impossible. |
| **9** | [Trapping Rain Water](#-features) | `HARD` | Two Pointers / Prefix Max | Compute how much rain water an elevation map can trap. |
| **10** | [Median of Two Sorted Arrays](#-features) | `HARD` | Binary Search / Divide & Conquer | Find the combined median of two sorted arrays in O(log(m+n)). |
| **11** | [Reverse String](#-features) | `EASY` | Strings / Two Pointers | Reverse a given string in-place with standard I/O. |
| **12** | [Valid Anagram](#-features) | `EASY` | Hash Table / Frequency Counting | Determine whether string `t` is an anagram of string `s`. |
| **13** | [Binary Search](#-features) | `EASY` | Binary Search | Search target in a sorted array in `O(log n)` time. |
| **14** | [Climbing Stairs](#-features) | `EASY` | Dynamic Programming / Fibonacci | Count distinct ways to climb `n` stairs taking 1 or 2 steps. |
| **15** | [Merge Two Sorted Arrays](#-features) | `EASY` | Two Pointers / Sorting | Merge two sorted arrays into a single sorted list. |
| **16** | [3Sum](#-features) | `MEDIUM` | Two Pointers / Arrays | Count unique triplets that sum to 0 without duplicates. |
| **17** | [Rotate Image](#-features) | `MEDIUM` | 2D Matrix / Linear Algebra | Rotate an `n x n` 2D image matrix clockwise by 90 degrees. |
| **18** | [Longest Palindromic Substring](#-features) | `MEDIUM` | Expand Around Center / DP | Find the length of the longest palindromic substring. |
| **19** | [Word Break](#-features) | `MEDIUM` | Dynamic Programming / Trie | Check if a string can be segmented into words from a dictionary. |
| **20** | [Edit Distance](#-features) | `HARD` | 2D Dynamic Programming (Levenshtein) | Minimum insert, delete, and replace steps to convert word1 to word2. |

---

## 🏗️ System Architecture

```mermaid
graph TD
    UserA["👤 Player 1"] -->|HTTP / REST| Frontend["⚛️ React 19 + Vite Frontend"]
    UserB["👤 Player 2"] -->|HTTP / REST| Frontend
    
    Frontend <-->|WebSockets (ws:// / wss://)| Daphne["⚡ Daphne ASGI Server"]
    Frontend <-->|REST API (/api/)| Django["🐍 Django 5.0 Core Engine"]
    
    subgraph Backend Services
        Daphne --> Channels["Django Channels (Room Groups)"]
        Django --> Auth["JWT Authentication (SimpleJWT)"]
        Django --> Matchmaker["Matchmaking & Battle Controller"]
        Django --> Problems["Problem Library & Test Suites"]
        Django --> Executor["🛡️ Isolated Subprocess Code Executor"]
        Django --> DB[("SQLite (Dev) / PostgreSQL (Prod)")]
    end

    Executor -->|Compile & Run (g++, gcc, python, node)| Sandbox["Sandbox Subprocess (CPU & Time Capped)"]
    Sandbox -->|Output, Verdict, Timing| Executor
```

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: [React 19](https://react.dev/) + [Vite](https://vitejs.dev/)
- **Code Editor**: [@monaco-editor/react](https://github.com/suren-atoyan/monaco-react)
- **Icons**: [lucide-react](https://lucide.dev/)
- **Animations**: [canvas-confetti](https://www.npmjs.com/package/canvas-confetti)
- **Styling**: Vanilla CSS tokens with modern dark mode aesthetic & glassmorphism
- **Real-Time Client**: Native WebSocket API with automatic reconnect & room management

### Backend
- **Framework**: [Django 5.0](https://www.djangoproject.com/) + [Django REST Framework](https://www.django-rest-framework.org/)
- **ASGI & WebSockets**: [Daphne](https://github.com/django/daphne) + [Django Channels 4](https://channels.readthedocs.io/)
- **Authentication**: JWT authentication with [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/)
- **Database**: SQLite (Local development) / PostgreSQL via [dj-database-url](https://pypi.org/project/dj-database-url/) (Production)
- **Execution Sandbox**: Subprocess engine with timeout watchdog supporting Python 3, Node.js, C (gcc), and C++ (g++)

---

## 📂 Project Structure

```text
CodeDuel/
├── backend/
│   ├── authentication/         # User registration, login, JWT, profiles & leaderboard
│   ├── battles/                # Matchmaking queue, rooms, battle state & WebSocket consumers
│   │   ├── consumers.py        # Real-time WebSocket battle consumer
│   │   ├── routing.py          # WebSocket URL routes (/ws/battle/<room_code>/)
│   │   └── views.py            # Battle creation, join & matchmaking endpoints
│   ├── codeduel/               # Project configuration (settings, asgi, wsgi, urls)
│   ├── problems/               # Problem definitions, test cases & seed scripts
│   │   ├── models.py           # Problem & TestCase models
│   │   └── management/commands/seed_problems.py  # 20 problem seed command
│   ├── submissions/            # Submission tracking & isolated execution sandbox
│   │   └── executor.py         # Multi-language code runner & test validator
│   ├── build.sh                # Production build & migration script (Render)
│   ├── manage.py               # Django CLI utility
│   └── requirements.txt        # Backend dependencies
├── frontend/
│   ├── public/                 # Static assets
│   ├── src/
│   │   ├── components/         # UI components
│   │   │   ├── AuthModal.jsx        # Login & registration modal
│   │   │   ├── BattleLobby.jsx      # Room creation, joining & queue lobby
│   │   │   ├── BattleRoom.jsx       # Real-time 1v1 battle arena
│   │   │   ├── CodeWorkspace.jsx    # Monaco editor, test case runner & submit
│   │   │   ├── Leaderboard.jsx      # Global Elo rankings & stats
│   │   │   ├── Navbar.jsx           # App navigation & user presence
│   │   │   ├── OnlinePresenceBar.jsx# Real-time player counts
│   │   │   └── ProblemLibrary.jsx   # Curated problem catalog & solo sandbox
│   │   ├── services/
│   │   │   ├── api.js          # REST API client
│   │   │   └── websocket.js    # Battle WebSocket connection manager
│   │   ├── App.jsx             # Main routing & state container
│   │   ├── index.css           # Global design system & typography
│   │   └── main.jsx            # React root mount
│   ├── package.json            # Frontend dependencies
│   ├── vercel.json             # Vercel SPA routing configuration
│   └── vite.config.js          # Vite build config
├── render.yaml                 # Render infrastructure-as-code deployment blueprint
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

---

## 🚀 Quick Start & Local Setup

### Prerequisites
- **Python**: 3.10 or higher
- **Node.js**: 18.x or higher (with npm)
- *(Optional)* **g++ / gcc**: If compiling and running C/C++ solutions locally.

---

### 1. Backend Setup (Django + Channels)

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**:
   - **Windows**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Seed the 20 Algorithmic Problems**:
   ```bash
   python manage.py seed_problems
   ```
   *Output: `Successfully seeded 20 comprehensive DSA problems with sample & hidden test cases!`*

6. **Start the ASGI server (Daphne)**:
   ```bash
   daphne -b 127.0.0.1 -p 8000 codeduel.asgi:application
   ```
   *(Alternatively, you can run `python manage.py runserver`, though Daphne is recommended for full WebSocket performance).*

The backend API will be live at `http://127.0.0.1:8000/`.

---

### 2. Frontend Setup (React + Vite)

1. **Open a new terminal and navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install frontend dependencies**:
   ```bash
   npm install
   ```

3. **(Optional) Configure environment variables**:
   Create a `.env` file in the `frontend` folder if you wish to point to a custom backend:
   ```env
   VITE_API_URL=http://127.0.0.1:8000
   ```
   *(If not set, it defaults automatically to `http://localhost:8000`).*

4. **Start the development server**:
   ```bash
   npm run dev
   ```

5. Open your browser and visit: **`http://localhost:5173`**

---

## ⚙️ Environment Variables

### Backend (`backend/.env` or Render Dashboard)
| Variable | Default Value | Description |
|---|---|---|
| `DEBUG` | `True` | Set to `False` in production. |
| `SECRET_KEY` | *(django-insecure dev key)* | Unique secret key for session and cryptographic signing. |
| `DATABASE_URL` | `sqlite:///backend/db.sqlite3` | PostgreSQL connection string in production (e.g., Render/Supabase). |
| `PORT` | `8000` | Port for Daphne to bind to. |

### Frontend (`frontend/.env` or Vercel Dashboard)
| Variable | Default Value | Description |
|---|---|---|
| `VITE_API_URL` | `http://localhost:8000` | Backend API base URL (uses `wss://` automatically if URL is `https://`). |

---

## 📡 API & WebSocket Reference

### Core REST Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register/` | Register new user account & obtain JWT tokens |
| `POST` | `/api/auth/login/` | Authenticate with username & password |
| `GET` | `/api/auth/me/` | Fetch current authenticated user & Elo rating |
| `GET` | `/api/auth/leaderboard/` | Retrieve top ranked players sorted by rating |
| `GET` | `/api/auth/online-stats/` | Live stats (online users, active battles) |
| `GET` | `/api/problems/` | List all 20 available coding challenges |
| `GET` | `/api/problems/<id>/` | Retrieve problem statement, constraints & sample tests |
| `POST` | `/api/submissions/` | Submit code for sandboxed evaluation |
| `GET` | `/api/submissions/?problem=<id>` | Fetch submission history for problem |
| `POST` | `/api/battles/create/` | Create a new duel room with optional problem ID |
| `POST` | `/api/battles/join/` | Join an existing room via 6-character room code |
| `POST` | `/api/battles/matchmaking/join/` | Enqueue into the automated matchmaking queue |
| `GET` | `/api/battles/matchmaking/status/` | Poll for matched opponent room code |
| `POST` | `/api/battles/matchmaking/leave/` | Cancel queue search |

### WebSocket Protocol

- **Route**: `ws://<host>/ws/battle/<room_code>/`
- **Actions Broadcasted**:
  - `player_joined`: Sent when opponent enters the room.
  - `countdown_started`: Synchronized 5-second match countdown.
  - `battle_started`: Battle timer triggers; code editors unlock.
  - `opponent_submission`: Real-time notification of opponent's test case verdict.
  - `battle_finished`: Duel concluded with winner, execution times, and Elo updates.

---

## 🚢 Production Deployment

### Backend Deployment (Render)
This repository includes a [`render.yaml`](render.yaml) blueprint ready for 1-click deployment on Render:
1. Push your repository to GitHub.
2. In the [Render Dashboard](https://dashboard.render.com/), choose **New > Blueprint**.
3. Connect your GitHub repository:
   - Render automatically executes `bash build.sh` (runs pip install, migrations, and `seed_problems`).
   - Starts Daphne: `daphne -b 0.0.0.0 -p $PORT codeduel.asgi:application`.

### Frontend Deployment (Vercel)
This repository includes [`frontend/vercel.json`](frontend/vercel.json) for seamless Single-Page App rewrites:
1. Import the repository in [Vercel](https://vercel.com/).
2. Set the **Root Directory** to `frontend`.
3. Add Environment Variable:
   - `VITE_API_URL` = `https://your-render-backend-url.onrender.com`
4. Deploy!

---

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute new problems, enhance the execution sandbox, or add new languages:

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/new-problems
   ```
3. **Commit your changes**:
   ```bash
   git commit -m "Add graph algorithms to problem library"
   ```
4. **Push to branch**:
   ```bash
   git push origin feature/new-problems
   ```
5. **Open a Pull Request**

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for details.

---

<p align="center">
  Built with ❤️ for competitive programmers and software engineers worldwide.
</p>
