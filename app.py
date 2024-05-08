import asyncio
import logging
import openai
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import whisper

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram bot token
TOKEN = '7040780745:AAFYiU11m-zR1toUYAFRU9tsig6eVKjcd14'
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)

model = whisper.load_model("tiny")

# OpenAI API key
openai.api_key = 'Api Key'


greeted_users = set()

# Database setup using SQLAlchemy
Base = declarative_base()
engine = create_engine('sqlite:///client_data.db')  # SQLite database
Session = sessionmaker(bind=engine)
session = Session()


# Define a model to store client data
class ClientData(Base):
    __tablename__ = 'client_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String)
    first_name = Column(String)
    patronymic = Column(String)
    mobile_phone = Column(String)
    additional_phone = Column(String)
    email = Column(String)
    passport_data = Column(String)
    birth_date = Column(String)
    personal_number = Column(String)


Base.metadata.create_all(engine)


# FSM states
class ClientDataForm(StatesGroup):
    surname = State()
    first_name = State()
    patronymic = State()
    mobile_phone = State()
    additional_phone = State()
    email = State()
    passport_data = State()
    birth_date = State()
    personal_number = State()


# Функция генерации вопросов с помощью GPT-4 на русском языке
async def generate_question(current_state_label):
    prompt = f"Сформулируй вопрос для получения {current_state_label} от клиента."
    response = await fetch_gpt_response(prompt)
    return response if response else f"Предоставьте, пожалуйста, {current_state_label}."


# Получение ответа от GPT-4
async def fetch_gpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Составляй вопросы на русском языке для сбора персональных данных.Сбор данных обязателен,если человек не хочет отвечать ,постарайся чтоб он ответил"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Error generating GPT-4 response: {str(e)}")
        return None


# Обработчики состояний для сохранения данных в базе
async def save_data(state: FSMContext):
    data = await state.get_data()
    new_entry = ClientData(**data)
    session.add(new_entry)
    session.commit()


@router.message(Command("start"))
async def start_message(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать! Начнем сбор вашей информации.")
    await state.set_state(ClientDataForm.surname)
    question = await generate_question("фамилия")
    await message.answer(question)


@router.message(ClientDataForm.surname)
async def process_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(ClientDataForm.first_name)
    question = await generate_question("имя")
    await message.answer(question)


@router.message(ClientDataForm.first_name)
async def process_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(ClientDataForm.patronymic)
    question = await generate_question("отчество")
    await message.answer(question)


@router.message(ClientDataForm.patronymic)
async def process_patronymic(message: Message, state: FSMContext):
    await state.update_data(patronymic=message.text)
    await state.set_state(ClientDataForm.mobile_phone)
    question = await generate_question("мобильный телефон")
    await message.answer(question)


@router.message(ClientDataForm.mobile_phone)
async def process_mobile_phone(message: Message, state: FSMContext):
    await state.update_data(mobile_phone=message.text)
    await state.set_state(ClientDataForm.additional_phone)
    question = await generate_question("дополнительный телефон")
    await message.answer(question)


@router.message(ClientDataForm.additional_phone)
async def process_additional_phone(message: Message, state: FSMContext):
    await state.update_data(additional_phone=message.text)
    await state.set_state(ClientDataForm.email)
    question = await generate_question("email")
    await message.answer(question)


@router.message(ClientDataForm.email)
async def process_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(ClientDataForm.passport_data)
    question = await generate_question("паспортные данные")
    await message.answer(question)


@router.message(ClientDataForm.passport_data)
async def process_passport_data(message: Message, state: FSMContext):
    await state.update_data(passport_data=message.text)
    await state.set_state(ClientDataForm.birth_date)
    question = await generate_question("дату рождения")
    await message.answer(question)


@router.message(ClientDataForm.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await state.set_state(ClientDataForm.personal_number)
    question = await generate_question("личный номер")
    await message.answer(question)


@router.message(ClientDataForm.personal_number)
async def process_personal_number(message: Message, state: FSMContext):
    await state.update_data(personal_number=message.text)
    await save_data(state)
    await message.answer("Спасибо, что предоставили всю информацию!")


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    