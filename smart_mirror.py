import os
import time
import threading
from datetime import datetime
import random

# -----------------------------------------
# REQUIRED: Install requests for live API
# pip install requests
# -----------------------------------------
try:
    import requests
    HAS_REQUESTS = True
except:
    HAS_REQUESTS = False

# -----------------------------------------
# PUT YOUR REAL API KEYS HERE
# -----------------------------------------

OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"   # <-- paste your weather API key here
NEWSAPI_API_KEY     = "YOUR_NEWSAPI_API_KEY"       # <-- paste your news API key here

CITY = "Hyderabad"
TASK_FILE = "tasks.txt"
REFRESH = 1  # seconds

QUOTES = [
    "Believe you can and you're halfway there.",
    "Do something today that your future self will thank you for.",
    "Small steps every day lead to big results.",
    "Practice makes progress, not perfection.",
    "Your limitation—it's only your imagination."
]

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ---------------- WEATHER ----------------
def get_weather():
    if not HAS_REQUESTS or not OPENWEATHER_API_KEY:
        return None

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": CITY,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    try:
        r = requests.get(url, params=params, timeout=5)
        if r.status_code == 200:
            data = r.json()
            return {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "desc": data["weather"][0]["description"].capitalize()
            }
    except:
        return None
    return None

# ---------------- NEWS ----------------
def get_news():
    if not HAS_REQUESTS or not NEWSAPI_API_KEY:
        return None

    url = "https://newsapi.org/v2/top-headlines"
    params = {"country": "in", "pageSize": 1, "apiKey": NEWSAPI_API_KEY}

    try:
        r = requests.get(url, params=params, timeout=5)
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            if articles:
                return articles[0]["title"]
    except:
        return None
    return None

# ---------------- TASKS ----------------
def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []

    with open(TASK_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# ---------------- RENDER ----------------
def greeting(hour):
    if hour < 12: return "🌞 Good Morning"
    if hour < 17: return "🌤 Good Afternoon"
    return "🌙 Good Evening"

def show_dashboard(weather, news, tasks):
    now = datetime.now()
    date_str = now.strftime("%A, %d %B %Y")
    time_str = now.strftime("%I:%M:%S %p")

    print("┌" + "─"*60 + "┐")
    print(f"│  {greeting(now.hour)} | {date_str} | {time_str}  │")
    print("├" + "─"*60 + "┤")

    # WEATHER
    if weather:
        print(f"│ Weather: {weather['city']} | {weather['temp']}°C | {weather['desc']} | Humidity: {weather['humidity']}% │")
    else:
        print("│ Weather: No data — Add your OPENWEATHER_API_KEY │")

    # NEWS
    if news:
        print(f"│ News: {news[:55]}… │")
    else:
        print("│ News: No data — Add your NEWSAPI_API_KEY │")

    print("├" + "─"*60 + "┤")

    # QUOTE
    print(f"│ Quote: {random.choice(QUOTES)} │")

    print("├" + "─"*60 + "┤")

    # TASKS
    print("│ Today's Tasks:                                         │")
    if tasks:
        for i, t in enumerate(tasks, 1):
            print(f"│  {i}. {t}                                              │")
    else:
        print("│  No tasks found. Create tasks.txt                     │")

    print("└" + "─"*60 + "┘")
    print("\nPress CTRL + C to exit.")

# ---------------- MAIN LOOP ----------------
def main():
    print("Starting Smart Mirror...")

    weather = get_weather()
    news = get_news()
    tasks = load_tasks()

    try:
        while True:
            clear()
            show_dashboard(weather, news, tasks)
            time.sleep(REFRESH)
    except KeyboardInterrupt:
        print("\nGoodbye, Sindhu Manogna ✨")

if __name__ == "__main__":
    main()
