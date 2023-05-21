from youtube_search import YoutubeSearch
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle, input_message_content
import hashlib
from config import TOKEN

def searcher(text):
    return f"{YoutubeSearch(text, max_results=10).to_dict()}"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапишите мне что-нибудь!")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напишите мне что-нибудь, и я отправлю этот текст Вам в ответ!")

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)

@dp.inline_handler()
async def inline_handler(query : types.InlineQuery):
    text = query.query or 'echo'
    links = searcher(text)

    articles = [types.InlineQueryResultArticle(
        id = hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),
        title = f'{link["title"]}',
        url = f'{website} {link["id"]}',
        thumb_url = f'{link["thumbnails"][0]}',
        input_message_content=types.InputTextMessageContent(
            message_text=f'{website} {link["id"]}')
    ) for link in links]
    website = "https://www.youtube.com/watch?v="
    await query.answer(articles, cache_time=60, is_personal=True)

executor.start_polling(dp, skip_updates=True)
