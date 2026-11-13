import os
import sqlite3
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler,
    MessageHandler, ContextTypes, filters
)

TOKEN = os.getenv("BOT_TOKEN")

db = sqlite3.connect("bingo.db")
db.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance REAL DEFAULT 0
)
""")
db.commit()

menu = [
    ["🎮 Play", "💰 Check your balance"],
    ["💳 Deposit", "🏧 Withdrawal"],
    ["📜 Transaction History", "📖 Instruction"],
    ["📝 Register"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user.id,)
    )
    db.commit()

    await update.message.reply_text(
        "🎉 Welcome to Bravo Bingo!\n\n"
        "Choose an option below:",
        reply_markup=ReplyKeyboardMarkup(
            menu, resize_keyboard=True
        )
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    msg = update.message.text

    if msg == "📝 Register":
        db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,)
        )
        db.commit()
        await update.message.reply_text("✅ Registration successful!")

    elif msg == "💰 Check your balance":
        row = db.execute(
            "SELECT balance FROM users WHERE user_id=?",
            (user_id,)
        ).fetchone()
        balance = row[0] if row else 0
        await update.message.reply_text(f"💰 Balance: {balance} Birr")

    elif msg == "🎮 Play":
        await update.message.reply_text(
            "🎮 Welcome to Bravo Bingo!\n\n"
            "Choose your game:\n"
            "10 Birr - Super Bingo\n"
            "50 Birr - Super Bingo\n\n"
            "Game entry is not active yet."
        )

    elif msg == "💳 Deposit":
        await update.message.reply_text(
            "💳 Deposit\n\n"
            "Please contact the administrator for deposit instructions."
        )

    elif msg == "🏧 Withdrawal":
        await update.message.reply_text(
            "🏧 Withdrawal\n\n"
            "Please contact the administrator for withdrawal instructions."
        )

    elif msg == "📜 Transaction History":
        await update.message.reply_text(
            "📜 Your transaction history will appear here."
        )

    elif msg == "📖 Instruction":
        await update.message.reply_text(
            "📖 Bravo Bingo Instructions\n\n"
            "1. Register\n"
            "2. Check your balance\n"
            "3. Choose Play\n"
            "4. Follow the game instructions"
        )

    else:
        await update.message.reply_text("Please choose from the menu.")

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is missing!")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("Bravo Bingo Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
