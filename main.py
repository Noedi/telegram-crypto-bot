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
        r.raise_for_status()  # This will raise an exception for bad status codes
        data = r.json()
        return data.get(coin_id)
    except Exception as e:
        print(f"Error fetching price for {coin_id}: {e}")
        return None

def fear_greed():
    try:
        r = requests.get("https://api.alternative.me/fng/?limit=1", timeout=10)
        r.raise_for_status()
        data = r.json()
        if "data" in data and len(data["data"]) > 0:
            return f"{data['data'][0]['value']} → {data['data'][0]['value_classification']}"
        return "N/A"
    except Exception as e:
        print(f"Error fetching fear/greed index: {e}")
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

    if not data or "usd" not in data:
        await update.message.reply_text(f"❌ {text.upper()} not found. Try btc, eth, sol, etc.")
        return

    price = data["usd"]
    change = data.get("usd_24h_change", 0)
    fg = fear_greed()

    # Format the price properly
    try:
        if price < 1:
            price_str = f"${price:.4f}"
        elif price < 1000:
            price_str = f"${price:.2f}"
        else:
            price_str = f"${price:,.2f}"
    except:
        price_str = f"${price}"

    msg = (
        f"💰 {text.upper()}\n"
        f"Price: {price_str}\n"
        f"24h: {'🟢 Up' if change > 0 else '🔴 Down'} {abs(change):.2f}%\n"
        f"Sentiment: {fg}\n\n"
        "Not financial advice – DYOR!"
    )
    await update.message.reply_text(msg)

if __name__ == "__main__":
    try:
        token = os.environ.get("BOT_TOKEN")
        if not token:
            print("❌ ERROR: BOT_TOKEN environment variable not set!")
            print("Please set your bot token with: export BOT_TOKEN='your_token_here'")
            exit(1)
            
        app = ApplicationBuilder().token(token).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, price_handler))

        print("🚀 CRYPTO BOT v22.5 LIVE – READY TO SELL FOR $300+!")
        app.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
