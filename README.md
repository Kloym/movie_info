🎬 Movie Info Telegram Bot

# Описание
Telegram-бот на Python, который парсит сайт IMDb и умеет:

По названию фильма выдавать жанр и рейтинг фильма.
По жанру выдавать список лучших фильмов и сериалов этого жанра.
# Как запустить
Установите зависимости через Poetry:

poetry install
# Создайте бота в Telegram:

Перейдите к @BotFather, введите
/start, затем /newbot
и следуйте инструкциям.
Получите токен и вставьте его в файл
.env
(пример —.env.example).
# Запустите скрипт:

poetry run python info.py
# Использование команд:

/start
— начать работу с ботом.
/name <название_фильма>
— получить жанр и рейтинг фильма (до 3 результатов).
/genre <жанр>
— получить список фильмов и сериалов по жанру.