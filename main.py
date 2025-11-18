import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

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
    except:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Crypto Bot LIVE\nType any coin: btc eth sol ton doge")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    coin_id = COIN_IDS.get(text, text.replace(" ", "-"))
    data = get_price(coin_id)
    if not data:
        await update.message.reply_text("Not found")
        return
    p = data["usd"]
    c = data.get("usd_24h_change", 0)
    await update.message.reply_text(f"{text.upper()}\n${p:,.2f}\n24h: {'Up' if c>0 else 'Down'} {abs(c):.2f}%")

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, price))
    print("BOT IS RUNNING!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
