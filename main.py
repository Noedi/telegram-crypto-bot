import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Coin mapping
COIN_IDS = {
    "bitcoin": "bitcoin", "btc": "bitcoin",
    "ethereum": "ethereum", "eth": "ethereum",
    "solana": "solana", "sol": "solana",
    "ton": "the-open-network", "toncoin": "the-open-network",
    "dogecoin": "dogecoin", "doge": "dogecoin",
    "bnb": "binancecoin", "ada": "cardano", "xrp": "ripple"
}

def get_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get(coin_id)
    except Exception:
        return None

def fear_greed():
    try:
        r = requests.get("https://api.alternative.me/fng/?limit=1", timeout=10)
        data = r.json()["data"][0]
        return f"{data['value']} → {data['value_classification']}"
    except Exception:
        return "N/A"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Crypto Price Bot LIVE!\n\n"
        "Type any coin (e.g., btc, eth, sol, ton, doge)\n\n"
        "Premium features coming soon!"
    )

async def price_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    if not text:
        await update.message.reply_text("Type a coin name (e.g., btc)")
        return

    coin_id = COIN_IDS.get(text, text.replace(" ", "-"))
    data = get_price(coin_id)

    if not data:
        await update.message.reply_text(f"❌ {text.upper()} not found. Try btc, eth, sol, etc.")
        return

    price = data["usd"]
    change = data.get("usd_24h_change", 0)
    fg = fear_greed()

    msg = (
        f"💰 {text.upper()}\n"
        f"Price: ${price:,.2f}\n"
        f"24h: {'🟢 Up' if change > 0 else '🔴 Down'} {abs(change):.2f}%\n"
        f"Sentiment: {fg}\n\n"
        "Not financial advice – DYOR!"
    )
    await update.message.reply_text(msg)

if __name__ == "__main__":
    token = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, price_handler))

    print("🚀 CRYPTO BOT v22.5 LIVE – READY TO SELL FOR $300+!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
