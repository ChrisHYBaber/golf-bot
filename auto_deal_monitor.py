import time
import requests
import os

# -----------------------
# CONFIG (ENV VARIABLES)
# -----------------------
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

seen = set()
running = True


# -----------------------
# TELEGRAM FUNCTION
# -----------------------
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })


# -----------------------
# SCORING ENGINE
# -----------------------
def score(name, buy, resale):

    fee = resale * 0.1325
    profit = resale - buy - fee - 10

    multiplier = 1.0
    n = name.lower()

    if "titleist" in n:
        multiplier = 1.3
    elif "ping" in n:
        multiplier = 1.25
    elif "taylormade" in n:
        multiplier = 1.2
    elif "callaway" in n:
        multiplier = 1.15

    if resale > 400:
        multiplier += 0.1

    if profit < 30:
        multiplier -= 0.2

    return profit * multiplier


# -----------------------
# DATA SOURCE (TEMP)
# -----------------------
def get_listings():
    # TEMP TEST DATA (replace later with eBay API)
    return [
        ("Test Ping Driver", 200, 400),
        ("TaylorMade Stealth Driver", 210, 380),
        ("Titleist TSR2 Driver", 300, 520),
    ]


# -----------------------
# TELEGRAM COMMANDS
# -----------------------
def check_commands():
    global running

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        data = requests.get(url).json()

        for item in data.get("result", []):
            msg = item.get("message", {}).get("text", "")

            if msg == "/stop":
                running = False
                send_telegram("🛑 Bot stopped")

            elif msg == "/start":
                running = True
                send_telegram("✅ Bot running")

            elif msg == "/status":
                send_telegram(f"Bot running: {running}")

    except:
        pass


# -----------------------
# MAIN LOOP
# -----------------------
print("STARTING LIVE SCAN...\n")

while True:

    check_commands()

    if not running:
        time.sleep(5)
        continue

    listings = get_listings()

    for item in listings:

        name, buy, resale = item

        score_val = score(name, buy, resale)

        if score_val > 110 and resale > 200:

            if name not in seen:

                message = f"""🔥 DEAL ALERT
{name}
Score: {round(score_val, 2)}
"""

                print(message)
                send_telegram(message)

                seen.add(name)

    print("Cycle complete. Waiting 10s...\n")
    time.sleep(10)
