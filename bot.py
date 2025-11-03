from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# === EDIT HERE LATER WHEN YOU GET AFFILIATE IDs ===
AMAZON_TAG = ""  # example: ?tag=yourtag-21
FLIPKART_TAG = ""  # example: &affid=yourid

# SerpAPI key (Get free key from serpapi.com)
SERP_API_KEY = "0a4b70f0123eb65030be9139796af839f59de269f87883ef75e2d9ee8fd84e48"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi 👋 Send me a product name to compare prices!")

async def search_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"Searching for: *{query}* 🔍", parse_mode="Markdown")

    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": SERP_API_KEY
    }

    r = requests.get(url, params=params).json()

    try:
        product = r["shopping_results"][0]
        title = product["title"]
        price = product.get("extracted_price", "N/A")
        image = product.get("thumbnail", "")
        link = product["link"]

        amazon_link = link + AMAZON_TAG
        flipkart_link = link + FLIPKART_TAG

        buttons = [
            [InlineKeyboardButton("Buy on Amazon 🛒", url=amazon_link)],
            [InlineKeyboardButton("Buy on Flipkart 📦", url=flipkart_link)]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        await update.message.reply_photo(
            photo=image,
            caption=f"📦 *{title}*\n💰 Price: ₹{price}\n\nBest deal links 👇",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except:
        await update.message.reply_text("❌ No results found. Try another product.")

def main():
    app = ApplicationBuilder().token("8253092712:AAFEYO5eNxeN_PHzwaTDAyN0KTHVJLy-ijs").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_product))
    app.run_polling()

if __name__ == "__main__":
    main()
