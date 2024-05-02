import asyncio
import logging
import openai
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.dispatcher.router import Router
import whisper

# Set up logging to display information in the console.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token obtained from BotFather in Telegram.
TOKEN = 'token'
bot = Bot(token=TOKEN)
router = Router()

model = whisper.load_model("tiny")

# Set your OpenAI API key here
openai.api_key = 'key'


greeted_users = set()


@router.message(Command("start"))
async def start_message(message: Message):
    greeted_users.add(message.from_user.id)
    await message.answer("Здравствуйте, как я могу к вам обращаться?")

@router.message()
async def handle_message(message: Message):
    if message.voice:
        await handle_voice(message)
    elif message.text:
        if message.from_user.id in greeted_users:
            # Check if this is the first time the user provides their name
            if message.from_user.id not in user_names:
                user_names[message.from_user.id] = message.text.strip()
                reply = f"Приятно познакомиться, {message.text.strip()}. Можем ли мы приступить к получению ваших данных?"
                await message.answer(reply)
            else:
                await handle_text_message(message, message.text)
        else:
            greeted_users.add(message.from_user.id)
            await message.answer("Здравствуйте, как я могу к вам обращаться?")

async def handle_voice(message: Message):
    file_info = await bot.get_file(message.voice.file_id)
    file_path = await bot.download_file(file_info.file_path)
    with open("voice_message.ogg", "wb") as f:
        f.write(file_path.read())
    result = model.transcribe("voice_message.ogg")
    text = result['text']
    await handle_text_message(message, text)

async def handle_text_message(message: Message, text):
    user_question = text.lower()
    answer = await fetch_gpt_response(user_question)
    await send_long_message(message.chat.id, answer)

async def fetch_gpt_response(user_question):
    # Read questions directly from the file
    with open('1111.txt', 'r') as file:
        lines = file.readlines()
    mandatory_questions = [line.strip() for line in lines if line.strip().startswith('*')]
    optional_questions = [line.strip() for line in lines if not line.strip().startswith('*')]

    intro = '''Ты профессиональный менеджер по сбору информации.
    Общайся корректно, задавай вопросы по порядку.
    Если пользователь ответил на обязательный вопрос некорректно, скажи об этом пользователю и перезадай вопрос.
    Если пользователь некорректно ответил на дополнительный вопрос, скажи об этом пользователи и спроси, не хочет ли он пропустить этот вопрос.'''

    prompt = f'''{intro}
    
    Вот список обязательных вопросов:
    {mandatory_questions}
    
    Вот список дополнительных вопросов:
    {optional_questions}
    
    Первоначальный вопрос пользователя: {user_question}
    
    На основании ответов пользователя определите дальнейшие действия.
    
    Когда все вопросы заданы поблагодари пользователя за ответ, и попрощайся'''
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Please proceed with the necessary queries."}
            ],
            max_tokens=1000
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Error generating GPT-3 response: {str(e)}")
        return "Sorry, I encountered an error while generating a response."

def split_message(text, size=4096):
    return [text[i:i+size] for i in range(0, len(text), size)]

async def send_long_message(chat_id, text):
    parts = split_message(text)
    for part in parts:
        await bot.send_message(chat_id, part)

user_names = {}


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
