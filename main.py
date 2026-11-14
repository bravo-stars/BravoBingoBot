
import os
import sqlite3
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler,
    MessageHandler, ContextTypes, filters
)

TOKEN = os.getenv("BOT_TOKEN")

db = sqlite3.connect("bingo.db", check_same_thread=False)

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

game_menu = [
    ["🎮 Play - 10 ብር"],
    ["🎯 SuperBingo - 50 ብር"],
    ["⚽ BravoBingo Bonus"],
    ["⬅️ Back"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    db.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user.id,)
    )
    db.commit()

    await update.message.reply_text(
        "🎉 Welcome to Bravo Bingo!\n\nChoose an option:",
        reply_markup=ReplyKeyboardMarkup(
            menu, resize_keyboard=True
        )
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    msg = update.message.text

    if msg == "🎮 Play":
        await update.message.reply_text(
            "🎮 Bravo Bingo - Choose Your Game:",
            reply_markup=ReplyKeyboardMarkup(
                game_menu, resize_keyboard=True
            )
        )

    elif msg == "🎮 Play - 10 ብር":
        await update.message.reply_text(
            "🎮 Super Bingo\n\n"
            "የ10 ብር ጨዋታን መርጠሃል።\n"
            "ጨዋታው ገና አልተጀመረም።"
        )

    elif msg == "🎯 SuperBingo - 50 ብር":
        await update.message.reply_text(
            "🎯 SuperBingo\n\n"
            "የ50 ብር ጨዋታን መርጠሃል።\n"
            "ጨዋታው ገና አልተጀመረም።"
        )

    elif msg == "⚽ BravoBingo Bonus":
        await update.message.reply_text(
            "⚽ BravoBingo Bonus\n\n"
            "🏆 የታቀደው ሽልማት: 10,000 ብር\n"
            "ብዙ አሸናፊዎች ሊኖሩ ይችላሉ።\n"
            "ጨዋታው ገና አልተጀመረም።"
        )

    elif msg == "⬅️ Back":
        await update.message.reply_text(
            "Main Menu:",
            reply_markup=ReplyKeyboardMarkup(
                menu, resize_keyboard=True
            )
        )

    elif msg == "📝 Register":
        db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,)
        )
        db.commit()
        await update.message.reply_text(
            "✅ Registration successful!"
        )

    elif msg == "💰 Check your balance":
        row = db.execute(
            "SELECT balance FROM users WHERE user_id=?",
            (user_id,)
        ).fetchone()
        balance = row[0] if row else 0
        await update.message.reply_text(
            f"💰 Balance: {balance} Birr"
        )

    elif msg == "💳 Deposit":
        await update.message.reply_text(
            "💳 Deposit\n\n"
            "Please contact the administrator."
        )

    elif msg == "🏧 Withdrawal":
        await update.message.reply_text(
            "🏧 Withdrawal\n\n"
            "Please contact the administrator."
        )

    elif msg == "📜 Transaction History":
        await update.message.reply_text(
            "📜 Transaction History is not active yet."
        )

    elif msg == "📖 Instruction":
        await update.message.reply_text(
            "📖 Bravo Bingo Instructions\n\n"
            "1. Register\n"
            "2. Check your balance\n"
            "3. Choose Play\n"
            "4. Select a Bingo game"
        )

    else:
        await update.message.reply_text(
            "Please choose from the menu."
        )

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is missing!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle)
    )

    print("Bravo Bingo Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
