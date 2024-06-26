import logging
import time
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
import sqlite3
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

BOT_TOKEN = "7139603494:AAGt8dTpHeWREpHXnutdVBcJryop0EhXwOk"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/book', '/film', "/help", "/chat"]]
reply_keyboard_2 = [['/book_help', '/back']]
reply_keyboard_3 = [['/film_help', '/back']]
reply_keyboard_4 = [['/chat_help', '/back']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
markup_for_books = ReplyKeyboardMarkup(reply_keyboard_2, one_time_keyboard=False)
markup_for_films = ReplyKeyboardMarkup(reply_keyboard_3, one_time_keyboard=False)
markup_for_chat = ReplyKeyboardMarkup(reply_keyboard_4, one_time_keyboard=False)

is_book = False
is_film = False
is_chat = False
first_ask = True

con = sqlite3.connect("books and films.db")
cur = con.cursor()


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот, который поможет вам выбрать фильм или книгу. Сначала выберите, что именно я должен вам посоветовать.",
    reply_markup=markup)



async def help(update, context):
    await update.message.reply_text(
        "Я бот-советчик. Могу посоветовать вам фильм или книгу")


async def book(update, context):
    global is_book
    is_book = True
    await update.message.reply_text(
        "Отлично. Перейдем к выбору книги.", reply_markup=markup_for_books)


def book_by_author(author):
    global book_res
    global first_ask
    if first_ask:
        res = cur.execute("""SELECT * FROM Books
                WHERE author = ?""", (author,)).fetchall()
        book_res = res
        res_2 = "Вот какие произведения этого автора мне удалось найти:\n"
        if len(res) == 0:
            return "Мне ничего не удалось найти по вашему запросу. Извините."
        for i in range(len(res)):
            res_2 += res[i][1] + ", " + res[i][5] + ", " + str(res[i][6]) + "\n"
        res_2 += "Указанием дальнейших критериев вы будете уточнять результаты поиска"
        res_2 += "Для сброса критериев нажмите /book_reset"
        first_ask = False
        return res_2
    else:
        res = cur.execute("""SELECT * FROM Books
                WHERE author = ?""", (author,)).fetchall()
        res_2 = []
        if len(res) == 0:
            first_ask = True
            return "Мне ничего не удалось найти по вашему запросу. Извините. Критерии поиска сброшены."
        for i in range(len(res)):
            if res[i] in book_res:
                res_2.append(res[i])
        book_res = res_2
        res_3 = "Вот результат вашего запроса:\n"
        for i in range(len(res_2)):
            res_3 += res_2[i][1] + "," + res_2[i][2] + ", " + res_2[i][5] + ", " + str(res_2[i][6]) + "\n"
        return res_3


def book_by_name(name):
    global book_res
    global first_ask
    if first_ask:
        res = cur.execute("""SELECT * FROM Books
                WHERE name = ?""", (name,)).fetchall()
        book_res = res
        res_2 = "Вот какие книги с таким названием мне удалось найти:\n"
        if len(res) == 0:
            return "Мне ничего не удалось найти по вашему запросу. Извините."
        for i in range(len(res)):
            res_2 += res[i][1] + ", " + res[i][2] + ", " + res[i][5] + ", " + str(res[i][6]) + "\n"
        res_2 += "Указанием дальнейших критериев вы будете уточнять результаты поиска"
        res_2 += "Для сброса критериев нажмите /book_reset"
        first_ask = False
        return res_2
    else:
        res = cur.execute("""SELECT * FROM Books
                WHERE name = ?""", (name,)).fetchall()
        res_2 = []
        if len(res) == 0:
            first_ask = True
            return "Мне ничего не удалось найти по вашему запросу. Извините. Критерии поиска сброшены."
        for i in range(len(res)):
            if res[i] in book_res:
                res_2.append(res[i])
        book_res = res_2
        res_3 = "Вот результат вашего запроса:\n"
        for i in range(len(res_2)):
            res_3 += res_2[i][1] + "," + res_2[i][2] + ", " + res_2[i][5] + ", " + str(res_2[i][6]) + "\n"
        return res_3


def book_by_year(year):
    global book_res
    global first_ask
    if first_ask:
        res = cur.execute("""SELECT * FROM Books
                WHERE year = ?""", (year,)).fetchall()
        book_res = res
        res_2 = "Вот какие книги, вышедшие в этот год, мне удалось найти:\n"
        if len(res) == 0:
            return "Мне ничего не удалось найти по вашему запросу. Извините."
        for i in range(len(res)):
            res_2 += res[i][1] + ", " + res[i][2] + ", " + res[i][5] + "\n"
        res_2 += "Указанием дальнейших критериев вы будете уточнять результаты поиска"
        res_2 += "Для сброса критериев нажмите /book_reset"
        first_ask = False
        return res_2
    else:
        res = cur.execute("""SELECT * FROM Books
                WHERE year = ?""", (year,)).fetchall()
        res_2 = []
        if len(res) == 0:
            first_ask = True
            return "Мне ничего не удалось найти по вашему запросу. Извините. Критерии поиска сброшены."
        for i in range(len(res)):
            if res[i] in book_res:
                res_2.append(res[i])
        book_res = res_2
        res_3 = "Вот результат вашего запроса:\n"
        for i in range(len(res_2)):
            res_3 += res_2[i][1] + "," + res_2[i][2] + ", " + res_2[i][5] + ", " + str(res_2[i][6]) + "\n"
        return res_3


def book_by_series(series):
    global book_res
    global first_ask
    if first_ask:
        res = cur.execute("""SELECT * FROM Books
                WHERE series = ?""", (series,)).fetchall()
        book_res = res
        res_2 = "Вот какие произведения из этого цикла мне удалось найти:\n"
        if len(res) == 0:
            return "Мне ничего не удалось найти по вашему запросу. Извините."
        for i in range(len(res)):
            res_2 += res[i][1] + ", " + res[i][2] + ", " + res[i][5] + ", " + str(res[i][6]) + "\n"
        res_2 += "Указанием дальнейших критериев вы будете уточнять результаты поиска"
        res_2 += "Для сброса критериев нажмите /book_reset"
        first_ask = False
        return res_2
    else:
        res = cur.execute("""SELECT * FROM Books
                WHERE series = ?""", (series,)).fetchall()
        res_2 = []
        if len(res) == 0:
            first_ask = True
            return "Мне ничего не удалось найти по вашему запросу. Извините. Критерии поиска сброшены."
        for i in range(len(res)):
            if res[i] in book_res:
                res_2.append(res[i])
        book_res = res_2
        res_3 = "Вот результат вашего запроса:\n"
        for i in range(len(res_2)):
            res_3 += res_2[i][1] + "," + res_2[i][2] + ", " + res_2[i][5] + ", " + str(res_2[i][6]) + "\n"
        return res_3


def book_by_type(typ):
    global book_res
    global first_ask
    if first_ask:
        res = cur.execute("""SELECT * FROM Books
                WHERE type = ?""", (typ,)).fetchall()
        book_res = res
        res_2 = "Вот какие произведения этого жанра мне удалось найти:\n"
        if len(res) == 0:
            return "Мне ничего не удалось найти по вашему запросу. Извините."
        for i in range(len(res)):
            res_2 += res[i][1] + ", " + res[i][2] + ", " + str(res[i][6]) + "\n"
        res_2 += "Указанием дальнейших критериев вы будете уточнять результаты поиска"
        res_2 += "Для сброса критериев нажмите /book_reset"
        first_ask = False
        return res_2
    else:
        res = cur.execute("""SELECT * FROM Books
                WHERE type = ?""", (typ,)).fetchall()
        res_2 = []
        if len(res) == 0:
            first_ask = True
            return "Мне ничего не удалось найти по вашему запросу. Извините. Критерии поиска сброшены."
        for i in range(len(res)):
            if res[i] in book_res:
                res_2.append(res[i])
        book_res = res_2
        res_3 = "Вот результат вашего запроса:\n"
        for i in range(len(res_2)):
            res_3 += res_2[i][1] + "," + res_2[i][2] + ", " + res_2[i][5] + ", " + str(res_2[i][6]) + "\n"
        return res_3


def book_by_genre(genre):
    global book_res
    global first_ask
    if first_ask:
        res = cur.execute("""SELECT * FROM Books
                WHERE genre = ?""", (genre,)).fetchall()
        book_res = res
        res_2 = "Вот какие произведения этого направление мне удалось найти:\n"
        if len(res) == 0:
            return "Мне ничего не удалось найти по вашему запросу. Извините."
        for i in range(len(res)):
            res_2 += res[i][1] + ", " + res[i][2] + ", " + res[i][5] + ", " + str(res[i][6]) + "\n"
        res_2 += "Указанием дальнейших критериев вы будете уточнять результаты поиска"
        res_2 += "Для сброса критериев нажмите /book_reset"
        first_ask = False
        return res_2
    else:
        res = cur.execute("""SELECT * FROM Books
                WHERE genre = ?""", (genre,)).fetchall()
        res_2 = []
        if len(res) == 0:
            first_ask = True
            return "Мне ничего не удалось найти по вашему запросу. Извините. Критерии поиска сброшены."
        for i in range(len(res)):
            if res[i] in book_res:
                res_2.append(res[i])
        book_res = res_2
        res_3 = "Вот результат вашего запроса:\n"
        for i in range(len(res_2)):
            res_3 += res_2[i][1] + "," + res_2[i][2] + ", " + res_2[i][5] + ", " + str(res_2[i][6]) + "\n"
        return res_3


async def book_reset(update, context):
    global book_res
    global first_ask
    first_ask = True
    book_res = 0
    await update.message.reply_text("Критерии поиска сброшены")
    


async def analys(update, context):
    global is_book
    global is_film
    global is_chat

    if is_book is True or is_film is True or is_chat is True:
        if is_book is True:
            if update.message.text.split()[0] == "Автор:":
                author = update.message.text.split()
                author = " ".join(author[1:])
                await update.message.reply_text(book_by_author(author))
                
            elif update.message.text.split()[0] == "Название:":
                name = update.message.text.split()
                name = " ".join(name[1:])
                await update.message.reply_text(book_by_name(name))

            elif update.message.text.split()[0] == "Год:":
                year = update.message.text.split()
                year = " ".join(year[1:])
                await update.message.reply_text(book_by_year(year))

            elif update.message.text.split()[0] == "Цикл:":
                series = update.message.text.split()
                series = " ".join(series[1:])
                await update.message.reply_text(book_by_series(series))

            elif update.message.text.split()[0] == "Жанр:":
                typ = update.message.text.split()
                typ = " ".join(typ[1:])
                await update.message.reply_text(book_by_type(typ))

            elif update.message.text.split()[0] == "Направление:":
                genre = update.message.text.split()
                genre = " ".join(genre[1:])
                await update.message.reply_text(book_by_genre(genre))
            
            else:
                await update.message.reply_text("Простите, но я не понял вашего запроса")
        if is_film is True:
            if update.message.text.split()[0] == "Режиссер:":
                author = update.message.text.split()
                author = " ".join(author[1:])
                await update.message.reply_text(film_by_author(author))
            elif update.message.text.split()[0] == "Год:":
                year = update.message.text.split()
                year = " ".join(year[1:])
                await update.message.reply_text(film_by_year(year))
            elif update.message.text.split()[0] == "Жанр:":
                genre = update.message.text.split()
                genre = " ".join(genre[1:])
                await update.message.reply_text(film_by_type(genre))
            elif update.message.text.split()[0] == "Название:":
                name = update.message.text.split()
                name = " ".join(name[1:])
                await update.message.reply_text(film_by_name(name))
            elif update.message.text.split()[0] == "Серия:":
                series = update.message.text.split()
                series = " ".join(series[1:])
                await update.message.reply_text(film_by_series(series))
            else:
                await update.message.reply_text("Простите, но я не понял вашего запроса")
        if is_chat is True:
            chat = GigaChat(credentials='MjlhNDFhNTQtMDFlNC00OWQ1LTllOTAtNGFjZTZiNzU4MWJmOjNhM2ZhNTQ3LWY0YjctNGViMy04MzFlLTI3YjI4YTY0M2Q5Yw==', verify_ssl_certs=False)
            messages = [
                    SystemMessage(
                        content="Ты эмпатичный бот-советчик, который помогает найти все, что хочет пользователь"
                    )
                ]
            messages.append(HumanMessage(content=update.message.text))
            res = chat(messages)
            messages.append(res)
            await update.message.reply_text(res.content)
    else:
        await update.message.reply_text("Простите, но вы не выбрали, что я вам должен советовать.")

async def film(update, context):
    global is_film
    is_film = True
    await update.message.reply_text(
        "Прекрасно. Приступим к выбору фильма.", reply_markup=markup_for_films)
    
def film_by_author(author):
    res = cur.execute("""SELECT * FROM Films
            WHERE regisseur = ?""", (author,)).fetchall()
    res_2 = "Вот какие фильмы этого режиссера мне удалось найти:\n"
    if len(res) == 0:
        return "Мне ничего не удалось найти по вашему запросу. Извините."
    for i in range(len(res)):
        res_2 += str(res[i][1]) + ", " + str(res[i][5]) + ", " + str(res[i][6]) + "\n"
    return res_2

def film_by_year(year):
    res = cur.execute("""SELECT * FROM Films
            WHERE year = ?""", (year,)).fetchall()
    res_2 = "Вот какие фильмы, вышедшие в этот год, мне удалось найти:\n"
    if len(res) == 0:
        return "Мне ничего не удалось найти по вашему запросу. Извините."
    for i in range(len(res)):
        res_2 += str(res[i][1]) + ", " + str(res[i][5]) + ", " + str(res[i][6]) + "\n"
    return res_2

def film_by_name(name):
    res = cur.execute("""SELECT * FROM Films
            WHERE name = ?""", (name,)).fetchall()
    res_2 = "Вот какие фильмы по такому названию мне удалось найти:\n"
    if len(res) == 0:
        return "Мне ничего не удалось найти по вашему запросу. Извините."
    for i in range(len(res)):
        res_2 += str(res[i][1]) + ", " + str(res[i][5]) + ", " + str(res[i][6]) + "\n"
    return res_2

def film_by_series(series):
    res = cur.execute("""SELECT * FROM Films
            WHERE series = ?""", (series,)).fetchall()
    res_2 = "Вот какие фильмы этой серии мне удалось найти:\n"
    if len(res) == 0:
        return "Мне ничего не удалось найти по вашему запросу. Извините."
    for i in range(len(res)):
        res_2 += str(res[i][1]) + ", " + str(res[i][5]) + ", " + str(res[i][6]) + "\n"
    return res_2

def film_by_type(typ):
    res = cur.execute("""SELECT * FROM Films
            WHERE genre = ?""", (typ,)).fetchall()
    res_2 = "Вот какие фильмы этого жанра мне удалось найти:\n"
    if len(res) == 0:
        return "Мне ничего не удалось найти по вашему запросу. Извините."
    for i in range(len(res)):
        res_2 += str(res[i][1]) + ", " + str(res[i][5]) + ", " + str(res[i][6]) + "\n"
    return res_2
    
async def film_help(update, context):
    tex = "Способы отбора:\n \nПо режиссеру: Введите Режиссер: <Имя режиссера>"
    tex += "\nНапример: Режиссер: Стивен Спилберг\n"
    
    tex += "\nПо названию: Введите: Название: <название фильма>"
    tex += "\nНапример: Название: Война миров\n"
    
    tex += "\nПо году: Введите: Год: <год публикации фильма>"
    tex += "\nНапример: Год: 1954\n"

    tex += "\nПо циклу: Введите: Серия: <серия фильмов>"
    tex += "\nНапример: Серия: Гарри Поттер\n"

    tex += "\nПо жанру: Введите: Жанр: <жанр, к которому принадлежит фильм>"
    tex += "\nНапример: Жанр: Боевик\n"

    await update.message.reply_text(tex)

async def back(update, context):
    global is_book
    global is_film
    global is_chat
    is_film = False
    is_chat = False
    is_book = False
    await start(update, context)

async def book_help(update, context):
    tex = "Способы отбора:\n \nПо автору: Введите Автор: <Имя автора сокращенное"
    tex += "до инициалов и полной фамилии в именительном падеже>"
    tex += "\nНапример: Автор: Г. Уэллс\n"
    
    tex += "\nПо названию: Введите: Название: <название книги>"
    tex += "\nНапример: Название: Знак четырёх\n"
    
    tex += "\nПо году: Введите: Год: <год публикации произведения>"
    tex += "\nНапример: Год: 1954\n"

    tex += "\nПо циклу: Введите: Цикл: <цикл, к которому принадлежит книга>"
    tex += "\nНапример: Цикл: Властелин колец\n"

    tex += "\nПо жанру: Введите: Жанр: <жанр, к которому принадлежит книга>"
    tex += "\nНапример: Жанр: Повесть\n"

    tex += "\nПо направлению: Введите: Направление: <направление, к которому принадлежит книга>"
    tex += "\nНапример: Направление: Фэнтэзи"
    await update.message.reply_text(tex)

async def chat_help(update, context):
    tex = "Привет! Я чат-бот, который поможет тебе определиться\n"
    tex += "с выбором фильма или книги.\n"
    tex += "Просто начни фразу, например так:\n"
    tex += '"Посоветуй мне фильм, похожий на Гарри Поттера"\n'

    await update.message.reply_text(tex)

async def chat(update, context):
    global is_chat
    is_chat = True
    await update.message.reply_text(
        "Прекрасно. Подскажите, что посоветовать?", reply_markup=markup_for_chat)




def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, analys)
    application.add_handler(text_handler)
    application.add_handler(CommandHandler("book", book))
    application.add_handler(CommandHandler("book_help", book_help))
    application.add_handler(CommandHandler("book_reset", book_reset))
    application.add_handler(CommandHandler("film_help", film_help))
    application.add_handler(CommandHandler("chat_help", chat_help))
    application.add_handler(CommandHandler("back", back))
    application.add_handler(CommandHandler("film", film))
    application.add_handler(CommandHandler("chat", chat))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("start", start))
    application.run_polling()


if __name__ == '__main__':
    main()

