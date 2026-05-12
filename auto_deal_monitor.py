import time
import requests

BOT_TOKEN = "8820247177:AAFvJosIyrQ5C_Vk03LzLnlQyDsdM0UG7JA"
CHAT_ID = "5962811059"


seen = set()


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })


def score(name, buy, resale):

    fee = resale * 0.1325
    profit = resale - buy - fee - 10

    multiplier = 1.0

    n = name.lower()

    if "titleist" in n:
        multiplier = 1.25
    elif "ping" in n:
        multiplier = 1.2
    elif "taylormade" in n:
        multiplier = 1.15
    elif "callaway" in n:
        multiplier = 1.1

    return profit * multiplier


listings = [
    ("TaylorMade Stealth Driver", 210, 380),
    ("Ping G430 Driver", 230, 420),
    ("Callaway Paradym Driver", 180, 300),
    ("Titleist TSR2 Driver", 300, 520),
]

print("STARTING LIVE SCAN...\n")

while True:

    for item in listings:

        name, buy, resale = item

        score_val = score(name, buy, resale)

        if score_val > 120:

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