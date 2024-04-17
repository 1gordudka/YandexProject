import logging
import time
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
import sqlite3


BOT_TOKEN = "7139603494:AAGt8dTpHeWREpHXnutdVBcJryop0EhXwOk"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/book', '/film', "/help"]]
reply_keyboard_2 = [['/book_help', '/back']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
markup_for_books = ReplyKeyboardMarkup(reply_keyboard_2, one_time_keyboard=False)

is_book = False

con = sqlite3.connect("books and films.db")
cur = con.cursor()


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот, который поможет вам выбрать фильм или книгу.Сначала выберите, что именно я должен вам посоветовать.",
    reply_markup=markup)



async def help(update, context):
    await update.message.reply_text(
        "Я бот-советчик. Могу посоветовать вам фильм или книгу")


async def book(update, context):
    is_book = True
    await update.message.reply_text(
        "Отлично. Перейдем к выбору книги.", reply_markup=markup_for_books)


def book_by_author(author):
    res = cur.execute("""SELECT * FROM Books
            WHERE author = ?""", (author,)).fetchall()
    res_2 = "Вот какие произведения этого автора мне удалось найти:\n"
    for i in range(len(res)):
        res_2 += res[i][1] + ", " + res[i][5] + ", " + str(res[i][6]) + "\n"
    return res_2
    
    


async def analys(update, context):
    #if is_book is True:
    if "Автор: " in update.message.text:
        author = update.message.text.split()
        
        author = " ".join(author[1:])
        await update.message.reply_text(book_by_author(author))
    else:
        await update.message.reply_text("Простите, но вы не выбрали, что я вам должен советовать.")

async def film(update, context):
    await update.message.reply_text(
        "Прекрасно. Приступим к выбору фильма.")

async def back(update, context):
    is_book = False
    await start(update, context)

async def book_help(update, context):
    await update.message.reply_text(
        "Способы отбора: По автору: Введите Автор: <Имя автора сокращенное до инициалов и полной фамилии в именительном падеже> например Автор: Г. Уэллс")




def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, analys)
    application.add_handler(text_handler)
    application.add_handler(CommandHandler("book", book))
    application.add_handler(CommandHandler("book_help", book_help))
    application.add_handler(CommandHandler("back", back))
    application.add_handler(CommandHandler("film", film))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("start", start))
    application.run_polling()


if __name__ == '__main__':
    main()
