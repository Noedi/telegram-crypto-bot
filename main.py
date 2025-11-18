import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# ───── CONFIG ─────
COIN_IDS = {
    "bitcoin": "bitcoin", "btc": "bitcoin",
    "ethereum": "ethereum", "eth": "ethereum",
    "solana": "solana", "sol": "solana",
    "ton": "the-open-network", "toncoin": "the-open-network",
    "dogecoin": "dogecoin", "doge": "dogecoin",
    "binancecoin": "binancecoin", "bnb": "binancecoin",
    "cardano": "cardano", "ada": "cardano",
    "ripple": "ripple", "xrp": "ripple",
}

def get_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get(coin_id)
    except:
        return None

def fear_greed():
    try:
        r = requests.get("https://api.alternative.me/fng/?limit=1")
        data = r.json()["data"][0]
        return f"{data['value']} → {data['value_classification']}"
    except:
        return "N/A"

# ───── HANDLERS ─────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Crypto Price Bot LIVE\n\n"
        "Just type any coin:\n"
        "btc | eth | sol | ton | doge | ada | xrp\n\n"
        "More coins coming soon!"
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    coin_id = COIN_IDS.get(text, text.replace(" ", "-"))
    data = get_price(coin_id)

    if not data:
        await update.message.reply_text("Coin not found")
        return

    price = data["usd"]
    change = data.get("usd_24h_change", 0)

    msg = (
        f"{text.upper()}\n"
        f"Price: ${price:,.2f}\n"
        f"24h: {'Up' if change > 0 else 'Down'} {abs(change):.2f}%\n"
        f"Fear & Greed: {fear_greed()}"
    )
    await update.message.reply_text(msg)

# ───── MAIN ─────
if __name__ == "__main__":
    token = os.environ["BOT_TOKEN"]  # Railway reads this automatically
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, price))

    print("CRYPTO PRICE BOT IS RUNNING – READY TO SELL!")
      app.run_polling(
        allowed_updates=Update.ALL_TYPES
    )
