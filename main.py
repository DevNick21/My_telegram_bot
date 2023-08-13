import requests
import os
import logging
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


def the_joke():
    joke = Jokes()
    the_joke = joke.generate_normal_jokes()
    return the_joke


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Welcome to Nicholas's bot!\nIt is still in development though but i hope you are excited to use it\n")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Just testing")


async def jokes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(the_joke())


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
    football_keywords_fixtures = ["matches", "match", "schedule",
                                  "fixtures", "next match", "next game", "today match", "today game"]
    greeting_keywords = ["greetings", "hello", "hi", "good morning",
                         "good evening", "good afternoon", "howdy", "hey"]
    jokes_keywords = ["joke", "jokes", "a joke", "another joke", "tell me a joke", "crack a joke",
                      "give me a good joke", "i wan laugh", "make i laugh small", "abeg yarn me joke", "wetin dey funny", "wey go burst my belle", "Laugh dey hungry me", "say something funny",]

    football_keywords_standings = ["league position", "standings",
                                   "table", "top of the league", "teams", "first place", "bottom of the league", "bottom league"]
    res = any(
        footy_table_response in processed for footy_table_response in football_keywords_standings)
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
        footy_response in processed for footy_response in football_keywords_fixtures)
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
    for response in greeting_keywords:
        if response in processed:
            return "Hi there! How can I assist you today?"
    for joke_response in jokes_keywords:
        if joke_response in processed:
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
