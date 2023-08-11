import requests
import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, Updater
from telegram import Update, Bot
from dotenv import load_dotenv
from jokes import Jokes
load_dotenv()

TOKEN = os.getenv("telegram_api_key")
BOT_USERNAME = os.getenv("telegram_bot_username")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Commands for the bot


def the_joke():
    joke = Jokes()
    the_joke = joke.generate_normal_jokes()
    return the_joke


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Welcome to Nicholas's bot!\nIt is still in development though but i hope you are excited to use it\nType 'jokes'")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Just testing")


async def jokes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(the_joke())


def handle_response(text: str) -> str:
    processed: str = text.lower()
    if "hello" in processed:
        return "Hello"
    if "howdy" in processed:
        return "Howdy"
    if "jokes" in processed:
        return f"{the_joke()}"
    if "anotherjokes" in processed.strip():
        return f"{the_joke()}"
    return "i don't understand"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat.id}) in {message_type}: '{text}'")

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print("Bot:", response)

    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update{update} caused an error{context.error}")


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("joke", jokes))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling bot...")
    app.run_polling(poll_interval=3)
