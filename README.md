# 🌲 Catch the Forest

Catch the Forest is a location-based web application inspired by real-world travel exploration.

The idea is simple — discover interesting places, go there in real life, and prove it using your GPS location. Each visited location unlocks progress and rewards.

---

## 🚀 Live Demo
https://catch-the-forest.onrender.com

---

## 🧠 Main Idea

This project simulates a small exploration game where users:
- Browse different locations
- Visit them in real life
- Validate their position using GPS
- Unlock progress and earn badges

---

## ⚙️ Tech Stack

- Python
- Django
- HTML / CSS
- SQLite (development) / PostgreSQL (production ready)
- JavaScript (for GPS requests)

---

## 🔑 Features

- User authentication (register / login)
- Location-based validation using GPS coordinates
- Distance calculation (Haversine formula)
- Catch system (users can “capture” locations)
- Order creation flow after successful validation
- Badge system for unlocked locations
- Clean UI with a simple user flow

---

## 🧩 How It Works

1. User selects a location
2. Browser requests GPS position
3. Backend validates distance to target location
4. If within allowed radius → location is "caught"
5. User can proceed with next actions (order / progress)

---

## 🛠️ Setup (Local)

```bash
git clone https://github.com/seaman2000/Catch_the_forest
cd Catch_the_forest

python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
