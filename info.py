import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from decouple import config

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Dummy movie data
movies = {
    'Inception': 'A mind-bending thriller by Christopher Nolan.',
    'The Matrix': 'A sci-fi classic about reality and simulation.',
    'Interstellar': 'A journey through space and time to save humanity.',
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Send me a movie name to get information.')

async def get_movie_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = update.message.text.strip()
    info = movies.get(movie_name, 'Sorry, I have no information about that movie.')
    await update.message.reply_text(info)

def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
    application = ApplicationBuilder().token(config('API_KEY')).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_movie_info))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()