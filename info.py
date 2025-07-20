import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from decouple import config
import requests
from telegram import ReplyKeyboardMarkup, KeyboardButton

KINOPOISK_API_KEY = config('KINOPOISK_API_KEY') # Ваш api с кинопоиска, который можно получить вот по этой ссылке https://kinopoisk.dev/

GENRE_TRANSLATE = {
    "боевик": "боевик",
    "комедия": "комедия",
    "драма": "драма",
    "триллер": "триллер",
    "ужасы": "ужасы",
    "мелодрама": "мелодрама",
    "фантастика": "фантастика",
    "мультфильм": "мультфильм",
    "приключения": "приключения",
    "криминал": "криминал",
    "детектив": "детектив",
    "фэнтези": "фэнтези",
    "биография": "биография",
    "документальный": "документальный",
    "семейный": "семейный",
    "история": "история",
    "музыка": "музыка",
    "военный": "военный",
    "вестерн": "вестерн",
    "спорт": "спорт"
}

def get_genre_keyboard():
    genres = [
        ["боевик", "комедия", "драма"],
        ["триллер", "ужасы", "мелодрама"],
        ["фантастика", "мультфильм", "приключения"],
        ["криминал", "детектив", "фэнтези"],
        ["биография", "документальный", "семейный"],
        ["история", "музыка", "военный"],
        ["вестерн", "спорт"]
    ]
    return ReplyKeyboardMarkup(
        [[KeyboardButton(genre) for genre in row] for row in genres],
        resize_keyboard=True
    )

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def get_kinopoisk_info(title):
    url = f"https://api.kinopoisk.dev/v1.4/movie/search"
    headers = {"X-API-KEY": KINOPOISK_API_KEY}
    params = {"query": title, "limit": 1}
    r = requests.get(url, headers=headers, params=params)
    data = r.json()
    if data.get("docs"):
        movie = data["docs"][0]
        name = movie.get("name", "Без названия")
        year = movie.get("year", "N/A")
        genres = ', '.join([g['name'] for g in movie.get("genres", [])])
        rating = movie.get("rating", {}).get("kp", "N/A")
        description = movie.get("description", "")
        url = f"https://www.kinopoisk.ru/film/{movie.get('id')}/"
        return f"{name} ({year})\nЖанр: {genres}\nРейтинг: {rating}\n{description}\nПодробнее: {url}"
    else:
        return "Фильм не найден."

def get_kinopoisk_by_genre(genre_input):
    genre = GENRE_TRANSLATE.get(genre_input.lower())
    if not genre:
        return "Жанр не найден."
    url = f"https://api.kinopoisk.dev/v1.4/movie"
    headers = {"X-API-KEY": KINOPOISK_API_KEY}
    params = {"genres.name": genre, "limit": 10, "sortField": "rating.kp", "sortType": "-1"}
    r = requests.get(url, headers=headers, params=params)
    data = r.json()
    if not data.get("docs"):
        return "Фильмы не найдены."
    reply = f"Топ фильмов в жанре {genre}:\n"
    for movie in data["docs"]:
        reply += f"- {movie.get('name', 'Без названия')} ({movie.get('year', 'N/A')})\n"
    return reply

async def handle_genre_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    genre_input = update.message.text.lower()
    if genre_input in GENRE_TRANSLATE:
        reply = get_kinopoisk_by_genre(genre_input)
        await update.message.reply_text(reply, reply_markup=get_genre_keyboard())


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie = ' '.join(context.args)
    info = get_kinopoisk_info(movie)
    await update.message.reply_text(info)

async def genre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Выберите жанр:",
            reply_markup=get_genre_keyboard()
        )
        return
    genre_input = ' '.join(context.args).lower()
    reply = get_kinopoisk_by_genre(genre_input)
    await update.message.reply_text(reply, reply_markup=get_genre_keyboard())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Отправь мне название фильма через /name <название> или жанр через /genre <жанр>.')


def main():
    application = ApplicationBuilder().token(config('API_KEY')).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler("name", name))
    application.add_handler(CommandHandler("genre", genre))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_genre_button))
    application.run_polling()

if __name__ == '__main__':
    main()