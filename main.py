import requests
import os
import logging
import random
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, Updater
from telegram import Update, Bot
from dotenv import load_dotenv
from jokes import Jokes
from football import Football
load_dotenv()

TOKEN = os.getenv("telegram_api_key")
BOT_USERNAME = os.getenv("telegram_bot_username")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Commands for the bot
football = Football()


def get_joke():
    joke = Jokes()
    main = joke.normal_joke()
    return main


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Welcome to Nicholas's bot!\nIt is still in development though but i hope you are excited to use it\n")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Just testing")


async def jokes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_joke())


async def premier_league_table(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(football.get_table(football.PL))


async def la_liga_table(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(football.get_table(football.LA_LIGA))


async def serie_a_table(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(football.get_table(football.SERIE_A))


async def bundesliga_table(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(football.get_table(football.BUNDESLIGA))


def handle_response(text: str):
    processed: str = text.lower()

    FIXTURES_WORDS = ["matches", "match", "schedule",
                      "fixtures", "next match", "next game", "today match", "today game"]
    GREETINGS = ["Hello!", "Hey there!", "Hi!",
                 "Greetings!", "Howdy!", "Good day!"]
    GREETING_KEYWORDS = ["greetings", "hello", "hi", "good morning",
                         "good evening", "good afternoon", "howdy", "hey"]
    JOKES_KEYWORDS = ["joke", "jokes", "a joke", "another joke", "tell me a joke", "crack a joke",
                      "give me a good joke", "i wan laugh", "make i laugh small", "abeg yarn me joke", "wetin dey funny", "wey go burst my belle", "Laugh dey hungry me", "say something funny",]

    STANDINGS_WORDS = ["league position", "standings",
                       "table", "top of the league", "teams", "first place", "bottom of the league", "bottom league"]
    PLEASANTIES_KEYWORDS = ["how are you", "what's up", "what is going on"]

    res = any(
        footy_table_response in processed for footy_table_response in STANDINGS_WORDS)
    if res:
        if "premier league" in processed:
            return f"{football.get_table(football.PL)}"
        elif "la liga" in processed:
            return f"{football.get_table(football.LA_LIGA)}"
        elif "serie a" in processed:
            return f"{football.get_table(football.SERIE_A)}"
        elif "bundesliga" in processed:
            return f"{football.get_table(football.BUNDESLIGA)}"
    res_fix = any(
        footy_response in processed for footy_response in FIXTURES_WORDS)
    if res_fix:
        if "premier league" in processed:
            return f"{football.get_fixtures(football.PL)}"
        elif "champions league" in processed:
            return f"{football.get_fixtures(football.UCL)}"
        elif "ucl" in processed:
            return f"{football.get_fixtures(football.UCL)}"
        elif "la liga" in processed:
            return f"{football.get_fixtures(football.LA_LIGA)}"
        elif "serie a" in processed:
            return f"{football.get_fixtures(football.SERIE_A)}"
        elif "bundesliga" in processed:
            return f"{football.get_fixtures(football.BUNDESLIGA)}"
        elif "efl" in processed:
            return f"{football.get_fixtures(football.EFL)}"
        elif "carabao" in processed:
            return f"{football.get_fixtures(football.EFL)}"
        elif "europa" in processed:
            return f"{football.get_fixtures(football.EUROPA)}"
        elif "fa cup" in processed:
            return f"{football.get_fixtures(football.FA_CUP)}"
    for response in GREETING_KEYWORDS:
        if response in processed:
            selected_greeting = random.choice(GREETINGS)
            return f"{selected_greeting} there! How can I assist you today?"
    for joke_response in JOKES_KEYWORDS:
        if joke_response in processed:
            return f"{get_joke()}"

    for pleasanties in PLEASANTIES_KEYWORDS:
        if pleasanties in processed:
            return "I am doing fine, Thank you"
    if "greatest footballer" in processed:
        return "Cristiano Ronaldo is the greatest footballer of all time"
    return "i don't understand, please refer to help, to know what i can do"


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

    await update.message.reply_text("Sorry, Something went wrong\nPlease try again later")


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("joke", jokes))
    app.add_handler(CommandHandler(
        "premierleague", premier_league_table))
    app.add_handler(CommandHandler("laliga", la_liga_table))
    app.add_handler(CommandHandler("serie_a", serie_a_table))
    app.add_handler(CommandHandler("bundesliga", bundesliga_table))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    # app.add_handler(MessageHandler(filters.TEXT, handle_fixture_response))
    # app.add_handler(MessageHandler(filters.TEXT, handle_league_response))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling bot...")
    app.run_polling(poll_interval=3)
