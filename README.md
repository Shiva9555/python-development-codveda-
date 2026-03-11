# 🐍 Codveda Python Development Internship

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-4.x-green?style=for-the-badge&logo=django)
![Cryptography](https://img.shields.io/badge/Cryptography-Fernet-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)
![Internship](https://img.shields.io/badge/Codveda-Internship-purple?style=for-the-badge)

---

## 📌 About This Repository

This repository contains all tasks completed during the **Python Development Internship** at **Codveda Technologies**.  
The internship is structured into **3 levels** — Basic, Intermediate, and Advanced — with **3 tasks per level**.

> ✅ All 3 levels completed | 9 Tasks Total

---

## 🗂️ Project Structure

```
codveda-python-internship/
│
├── Level_1_Basic/
│   ├── task1_calculator.py
│   ├── task2_guessing_game.py
│   └── task3_word_counter.py
│
├── Level_2_Intermediate/
│   ├── task1_todo_app.py
│   ├── task2_data_scraper.py
│   └── task3_api_integration.py
│
├── Level_3_Advanced/
│   ├── setup_django_project.py       ← Auto-generates full Django app
│   ├── task2_file_encryption.py
│   └── task3_nqueens.py
│
└── README.md
```

---

## 📚 Level 1 — Basic

### ✅ Task 1: Simple Calculator
A command-line calculator supporting addition, subtraction, multiplication, and division.

**Features:**
- Separate functions for each arithmetic operation
- Takes two user inputs and lets them choose the operation
- Handles division by zero with clear error messages
- Asks user to calculate again after each result

**Run:**
```bash
python task1_calculator.py
```

---

### ✅ Task 2: Number Guessing Game
A fun terminal game where the user guesses a randomly generated number between 1–100.

**Features:**
- Uses Python's `random` module to generate the secret number
- Gives "Too High" / "Too Low" hints after each guess
- Shows remaining attempts every round
- Exits after correct guess or 10 failed attempts

**Run:**
```bash
python task2_guessing_game.py
```

---

### ✅ Task 3: Word Counter
A Python script that reads a text file and counts words, lines, and characters.

**Features:**
- Reads any `.txt` file provided by the user
- Counts total words, lines, and characters
- Shows Top 5 most frequent words (bonus feature)
- Handles `FileNotFoundError` and other exceptions gracefully
- Auto-creates a `sample.txt` for quick testing

**Run:**
```bash
python task3_word_counter.py
```

---

## 📚 Level 2 — Intermediate

### ✅ Task 1: To-Do List Application
A full-featured command-line To-Do app that saves tasks to a JSON file.

**Features:**
- Add, View, Delete, and Mark tasks as Done
- Persists all tasks in `tasks.json` using `json.load()` / `json.dump()`
- Each task stores: ID, title, description, status, and created date
- Error handling for deleting non-existent tasks
- Re-numbers task IDs after deletion

**Run:**
```bash
python task1_todo_app.py
```

---

### ✅ Task 2: Data Scraper
A web scraper that extracts quotes, authors, and tags from a live website and saves them to CSV.

**Features:**
- Uses `requests` to fetch web pages
- Parses HTML using `BeautifulSoup`
- Scrapes multiple pages automatically
- Saves all data to a timestamped `.csv` file
- Handles connection errors and HTTP errors

**Install & Run:**
```bash
pip install requests beautifulsoup4
python task2_data_scraper.py
```

**Target Site:** `http://quotes.toscrape.com`

---

### ✅ Task 3: API Integration — Crypto Price Tracker
A real-time cryptocurrency tracker using the free CoinGecko API (no API key needed).

**Features:**
- Fetches live Top 10 / Top 20 crypto prices in USD
- Shows 24h price change with 🟢🔴 indicators
- Search any specific coin (bitcoin, ethereum, dogecoin, etc.)
- Displays market cap, current price, and % change
- Full error handling for network failures

**Install & Run:**
```bash
pip install requests
python task3_api_integration.py
```

**API Used:** [CoinGecko Public API](https://www.coingecko.com/en/api) — Free, no key required

---

## 📚 Level 3 — Advanced

### ✅ Task 1: Django Web Application with Authentication

A fully functional **Blog Web Application** built with Django, featuring complete user authentication, role-based access control, and password reset via email.

**Features:**
- ✅ User Registration, Login, Logout
- ✅ Secure passwords using Django's built-in auth system
- ✅ User Roles: **Admin**, **Editor**, **Viewer**
- ✅ Admin Panel to change any user's role live
- ✅ Password Reset via email (console backend for dev)
- ✅ Change Password page
- ✅ Blog Posts: Create, Edit, Delete
- ✅ Comments on posts (login required)
- ✅ User Dashboard with personal post history
- ✅ Responsive Bootstrap 5 UI

**Project Structure (auto-generated):**
```
codveda_blog/
├── manage.py
├── core/               ← settings, urls, wsgi
├── accounts/           ← register, login, logout, roles, dashboard
├── blog/               ← posts, comments
└── templates/          ← all HTML templates
```

**Install & Run:**
```bash
pip install django
python setup_django_project.py   # auto-creates all project files

cd codveda_blog
python manage.py makemigrations accounts blog
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open in browser: **http://127.0.0.1:8000/**

| URL | Description |
|-----|-------------|
| `/` | Blog home — all posts |
| `/accounts/register/` | Create new account |
| `/accounts/login/` | Login |
| `/dashboard/` | User dashboard |
| `/profile/` | Edit profile & role |
| `/admin-panel/` | Manage users (admin only) |
| `/post/create/` | Write a new post |
| `/accounts/password_reset/` | Forgot password |
| `/admin/` | Django admin panel |

---

### ✅ Task 2: File Encryption / Decryption

A Python tool that encrypts and decrypts text files using two methods: **Caesar Cipher** and **Fernet (AES-128)** encryption.

**Features:**
- 🔐 **Caesar Cipher** — classic shift-based encryption (shift 1–25)
- 🔐 **Fernet Encryption** — production-grade AES-128 CBC + HMAC-SHA256
- Generates and saves a `fernet_secret.key` file
- Encrypts any text file → saves as new encrypted file
- Decrypts back to original with one command
- Handles `InvalidToken` error (wrong key / corrupted file)
- Auto-creates sample `.txt` files for quick testing
- Lists all files in the current directory

**Install & Run:**
```bash
pip install cryptography
python task2_file_encryption.py
```

**Quick Test Workflow:**
```
Option 6 → Create sample files
Option 1 → Caesar encrypt sample1.txt (shift=13)
Option 2 → Caesar decrypt sample1_caesar_encrypted.txt
Option 3 → Generate Fernet key
Option 4 → Fernet encrypt sample1.txt
Option 5 → Fernet decrypt sample1.txt.fernet
```

---

### ✅ Task 3: N-Queens Problem

Solves the classic N-Queens problem using the **Backtracking algorithm** — places N queens on an N×N chessboard so no two queens attack each other.

**Features:**
- Solves for any board size N (recommended: 1–12)
- Finds **all possible solutions**, not just one
- Displays each solution as a visual chessboard with queen positions
- Shows solution count, expected count, and time taken
- Handles N=2 and N=3 (no solutions exist — proven mathematically)
- **No external libraries needed** — pure Python

**Run:**
```bash
python task3_nqueens.py
```

**Algorithm (3 core functions):**

```python
is_safe(board, row, col, n)    # checks column + both diagonals
solve(board, row, n, solutions) # recursive backtracking engine
solve_nqueens(n)                # creates board, calls solve()
```

**Known Solutions:**

| N | Solutions |
|---|-----------|
| 4 | 2 |
| 5 | 10 |
| 6 | 4 |
| 8 | 92 |
| 10 | 724 |
| 12 | 14,200 |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.8+ | Core programming language |
| Django 4.x | Web framework (Level 3 Task 1) |
| cryptography | Fernet encryption (Level 3 Task 2) |
| requests | HTTP requests for API & scraper |
| BeautifulSoup4 | HTML parsing for web scraper |
| JSON | Task storage for To-Do app |
| CSV | Data export for web scraper |
| Bootstrap 5 | Frontend UI for Django app |

---

## ⚙️ Installation

**Clone the repository:**
```bash
git clone https://github.com/Shiva9555/python-development-codveda-.git
cd python-development-codveda-
```

**Install all dependencies:**
```bash
pip install django requests beautifulsoup4 cryptography
```

---

## 📋 Requirements

```
Python >= 3.8
django >= 4.0
requests >= 2.28
beautifulsoup4 >= 4.11
cryptography >= 38.0
```

---

## 👨‍💻 Author

** 
kuruva shiva**  
Python Development Intern — Codveda Technologies  
🔗 [LinkedIn](https://www.linkedin.com/in/kuruva-siva-413503333)  
💻 [GitHub](https://github.com/Shiva9555/python-development-codveda-)

---

## 🏢 About Codveda Technologies

Codveda Technology offers a diverse range of services including web development, app development, digital marketing, SEO optimization, AI/ML automation, and data analysis.

🌐 [www.codveda.com](https://www.codveda.com)  
📧 support@codveda.com  
🔗 [@codveda](https://www.linkedin.com/company/codveda)

---

## 🏷️ Tags

`#CodvedaJourney` `#CodvedaExperience` `#FutureWithCodveda`  
`#CodvedaProjects` `#CodvedaAchievements` `#PythonDevelopment`

---

⭐ *If you found this helpful, consider giving the repo a star!*
