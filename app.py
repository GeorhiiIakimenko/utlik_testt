import asyncio
import logging
import openai
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

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

# Database setup using SQLAlchemy
Base = declarative_base()
engine = create_engine('sqlite:///client_data.db')  # SQLite database
Session = sessionmaker(bind=engine)
session = Session()

# OpenAI API key
openai.api_key = 'API-key'

# Database setup using SQLAlchemy
metadata = MetaData()

client_data_table = Table(
    'client_data', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('surname', String),
    Column('first_name', String),
    Column('patronymic', String),
    Column('mobile_phone', String),
    Column('additional_phone', String),
    Column('email', String),
    Column('birth_date', String),
    Column('personal_number', String),
    Column('leasing_item', String),
    Column('leasing_cost', String),
    Column('leasing_quantity', String),
    Column('leasing_advance', String),
    Column('leasing_currency', String),
    Column('leasing_duration', String),
    Column('place_of_birth', String),
    Column('gender', String),
    Column('criminal_record', String),
    Column('document', String),
    Column('citizenship', String),
    Column('series', String),
    Column('number', String),
    Column('issue_date', String),
    Column('expiration_date', String),
    Column('issued_by', String),
    Column('registration_index', String),
    Column('registration_country', String),
    Column('registration_region', String),
    Column('registration_district', String),
    Column('registration_locality', String),
    Column('registration_street', String),
    Column('registration_house', String),
    Column('registration_building', String),
    Column('registration_apartment', String),
    Column('residence_index', String),
    Column('residence_country', String),
    Column('residence_region', String),
    Column('residence_district', String),
    Column('residence_locality', String),
    Column('residence_street', String),
    Column('residence_house', String),
    Column('residence_building', String),
    Column('residence_apartment', String),
    Column('workplace_name', String),
    Column('position', String),
    Column('work_experience', String),
    Column('income', String),
    Column('hr_phone', String),
    Column('marital_status', String),
    Column('dependents_count', String),
    Column('education', String),
    Column('military_duty', String),
    Column('relative_surname', String),
    Column('relative_first_name', String),
    Column('relative_patronymic', String),
    Column('relative_phone', String),
    Column('passport_main_page', String),
    Column('passport_30_31_page', String),
    Column('passport_registration_page', String),
    extend_existing=True
)

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
    birth_date = Column(String)
    personal_number = Column(String)
    leasing_item = Column(String)
    leasing_cost = Column(String)
    leasing_quantity = Column(String)
    leasing_advance = Column(String)
    leasing_currency = Column(String)
    leasing_duration = Column(String)
    place_of_birth = Column(String)
    gender = Column(String)
    criminal_record = Column(String)
    document = Column(String)
    citizenship = Column(String)
    series = Column(String)
    number = Column(String)
    issue_date = Column(String)
    expiration_date = Column(String)
    issued_by = Column(String)
    registration_index = Column(String)
    registration_country = Column(String)
    registration_region = Column(String)
    registration_district = Column(String)
    registration_locality = Column(String)
    registration_street = Column(String)
    registration_house = Column(String)
    registration_building = Column(String)
    registration_apartment = Column(String)
    residence_index = Column(String)
    residence_country = Column(String)
    residence_region = Column(String)
    residence_district = Column(String)
    residence_locality = Column(String)
    residence_street = Column(String)
    residence_house = Column(String)
    residence_building = Column(String)
    residence_apartment = Column(String)
    workplace_name = Column(String)
    position = Column(String)
    work_experience = Column(String)
    income = Column(String)
    hr_phone = Column(String)
    marital_status = Column(String)
    dependents_count = Column(String)
    education = Column(String)
    military_duty = Column(String)
    relative_surname = Column(String)
    relative_first_name = Column(String)
    relative_patronymic = Column(String)
    relative_phone = Column(String)
    passport_main_page = Column(String)
    passport_30_31_page = Column(String)
    passport_registration_page = Column(String)


Base.metadata.create_all(engine)


# Labels for client data fields with mandatory information
fields = [
    ("surname", "Фамилия*", True, False),
    ("first_name", "Имя*", True, False),
    ("patronymic", "Отчество*", True, False),
    ("mobile_phone", "Мобильный телефон*", True, False),
    ("additional_phone", "Дополнительный телефон", False, False),
    ("email", "Email", False, False),
    ("birth_date", "Дата рождения*", True, False),
    ("personal_number", "Личный номер*", True, False),
    ("leasing_item", "Наименование предмета лизинга*", True, False),
    ("leasing_cost", "Стоимость*", True, False),
    ("leasing_quantity", "Количество*", True, False),
    ("leasing_advance", "Аванс", False, False),
    ("leasing_currency", "Валюта договора*", True, False),
    ("leasing_duration", "Срок договора*", True, False),
    ("place_of_birth", "Место рождения", False, False),
    ("gender", "Пол*", True, False),
    ("criminal_record", "Наличие судимости*", True, False),
    ("document", "Документ, удостоверяющий личность (паспорт, ВНЖ)", False, False),
    ("citizenship", "Гражданство", False, False),
    ("series", "Серия (паспорта, ВНЖ)*", True, False),
    ("number", "Номер (паспорта, ВНЖ)*", True, False),
    ("issue_date", "Дата Выдачи (паспорта, ВНЖ)*", True, False),
    ("expiration_date", "Срок действия (паспорта, ВНЖ)*", True, False),
    ("issued_by", "Кем выдан (паспорт, ВНЖ)*", True, False),
    ("registration_index", "Индекс по прописке", False, False),
    ("registration_country", "Страна по прописке*", True, False),
    ("registration_region", "Область по прописке", False, False),
    ("registration_district", "Район по прописке", False, False),
    ("registration_locality", "Населенный пункт по прописке*", True, False),
    ("registration_street", "Улица по прописке*", True, False),
    ("registration_house", "Дом по прописке*", True, False),
    ("registration_building", "Строение, корпус по прописке", False, False),
    ("registration_apartment", "Квартира по прописке", False, False),
    ("residence_index", "Индекс фактического места жительства", False, False),
    ("residence_country", "Страна фактического места жительства*", True, False),
    ("residence_region", "Область фактического места жительства", False, False),
    ("residence_district", "Район фактического места жительства", False, False),
    ("residence_locality", "Населенный пункт фактического места жительства*", True, False),
    ("residence_street", "Улица фактического места жительства*", True, False),
    ("residence_house", "Дом фактического места жительства*", True, False),
    ("residence_building", "Строение, корпус фактического места жительства", False, False),
    ("residence_apartment", "Квартира фактического места жительства", False, False),
    ("workplace_name", "Наименование организации, в которой работаете в данный момент*", True, False),
    ("position", "Должность*", True, False),
    ("work_experience", "Стаж*", True, False),
    ("income", "Доход*", True, False),
    ("hr_phone", "Телефон отдела кадров или бухгалтерии*", True, False),
    ("marital_status", "Семейное положение*", True, False),
    ("dependents_count", "Количество иждивенцев", False, False),
    ("education", "Образование*", True, False),
    ("military_duty", "Воинская обязанность*", True, False),
    ("relative_surname", "Фамилия близкого родственника, либо супруга/супруги*", True, False),
    ("relative_first_name", "Имя близкого родственника, либо супруга/супруги*", True, False),
    ("relative_patronymic", "Отчество близкого родственника, либо супруга/супруги*", True, False),
    ("relative_phone", "Телефон близкого родственника, либо супруга/супруги*", True, False),
    ("passport_main_page", "Главный разворот (паспорта, ВНЖ)*", True, True),
    ("passport_30_31_page", "Разворот 30-31 (паспорта, ВНЖ)*", True, True),
    ("passport_registration_page", "Разворот с регистрацией (паспорта, ВНЖ)*", True, True),
]


# Функция отправки данных в Bitrix24
async def send_data_to_bitrix(data):
    bitrix_webhook_url = 'https://b24-kw5z35.bitrix24.by/rest/1/re2olb9c6h83be03/'
    lead_data = {
        'fields': {
            'TITLE': f"{data.get('surname')} {data.get('first_name')} {data.get('patronymic')}",
            'NAME': data.get('first_name'),
            'LAST_NAME': data.get('surname'),
            'SECOND_NAME': data.get('patronymic'),
            'PHONE': [
                {'VALUE': data.get('mobile_phone'), 'VALUE_TYPE': 'WORK'},
                {'VALUE': data.get('additional_phone'), 'VALUE_TYPE': 'HOME'}
            ],
            'EMAIL': [{'VALUE': data.get('email'), 'VALUE_TYPE': 'WORK'}],
            'COMMENTS': (
                f"Дата рождения: {data.get('birth_date')}\n"
                f"Личный номер: {data.get('personal_number')}\n"
                f"Место рождения: {data.get('place_of_birth')}\n"
                f"Пол: {data.get('gender')}\n"
                f"Судимость: {data.get('criminal_record')}\n"
                f"Документ: {data.get('document')}\n"
                f"Гражданство: {data.get('citizenship')}\n"
                f"Серия: {data.get('series')}\n"
                f"Номер: {data.get('number')}\n"
                f"Дата выдачи: {data.get('issue_date')}\n"
                f"Срок действия: {data.get('expiration_date')}\n"
                f"Кем выдан: {data.get('issued_by')}\n"
                f"Наименование предмета лизинга: {data.get('leasing_item')}\n"
                f"Стоимость: {data.get('leasing_cost')}\n"
                f"Количество: {data.get('leasing_quantity')}\n"
                f"Аванс: {data.get('leasing_advance')}\n"
                f"Валюта договора: {data.get('leasing_currency')}\n"
                f"Срок договора: {data.get('leasing_duration')}\n"
                f"Наименование организации: {data.get('workplace_name')}\n"
                f"Должность: {data.get('position')}\n"
                f"Стаж: {data.get('work_experience')}\n"
                f"Доход: {data.get('income')}\n"
                f"Телефон отдела кадров или бухгалтерии: {data.get('hr_phone')}\n"
                f"Семейное положение: {data.get('marital_status')}\n"
                f"Количество иждивенцев: {data.get('dependents_count')}\n"
                f"Образование: {data.get('education')}\n"
                f"Воинская обязанность: {data.get('military_duty')}\n"
                f"Фамилия родственника: {data.get('relative_surname')}\n"
                f"Имя родственника: {data.get('relative_first_name')}\n"
                f"Отчество родственника: {data.get('relative_patronymic')}\n"
                f"Телефон родственника: {data.get('relative_phone')}\n"
                f"Главный разворот паспорта: {data.get('passport_main_page')}\n"
                f"Разворот 30-31 паспорта: {data.get('passport_30_31_page')}\n"
                f"Разворот с регистрацией паспорта: {data.get('passport_registration_page')}"
            ),
            'UF_CRM_1591122334': data.get('registration_index'),
            'UF_CRM_1591122335': data.get('registration_country'),
            'UF_CRM_1591122336': data.get('registration_region'),
            'UF_CRM_1591122337': data.get('registration_district'),
            'UF_CRM_1591122338': data.get('registration_locality'),
            'UF_CRM_1591122339': data.get('registration_street'),
            'UF_CRM_1591122340': data.get('registration_house'),
            'UF_CRM_1591122341': data.get('registration_building'),
            'UF_CRM_1591122342': data.get('registration_apartment'),
            'UF_CRM_1591122343': data.get('residence_index'),
            'UF_CRM_1591122344': data.get('residence_country'),
            'UF_CRM_1591122345': data.get('residence_region'),
            'UF_CRM_1591122346': data.get('residence_district'),
            'UF_CRM_1591122347': data.get('residence_locality'),
            'UF_CRM_1591122348': data.get('residence_street'),
            'UF_CRM_1591122349': data.get('residence_house'),
            'UF_CRM_1591122350': data.get('residence_building'),
            'UF_CRM_1591122351': data.get('residence_apartment')
        }
    }

    async with aiohttp.ClientSession() as session1:
        async with session1.post(bitrix_webhook_url, json=lead_data) as response:
            if response.status == 200:
                return await response.json()
            else:
                logger.error(f"Error sending data to Bitrix24: {response.status}")
                return None


# Обработчики состояний для сохранения данных в базе
async def save_data_db(state: FSMContext):
    data = await state.get_data()
    # Remove temporary state data
    data.pop('current_field', None)
    data.pop('current_index', None)
    data.pop('is_image', None)

    try:
        new_entry = ClientData(**data)
        session.add(new_entry)
        session.commit()
    except TypeError as e:
        logger.error(f"Error saving data to database: {str(e)}")
        return False

    bitrix_response = await send_data_to_bitrix(data)
    if bitrix_response:
        logger.info("Data successfully sent to Bitrix24.")
    else:
        logger.error("Failed to send data to Bitrix24.")
        return False
    return True



@router.message(Command("start"))
async def start_message(message: Message):
    initial_prompt = "Привет! Чем я могу вам помочь?"
    await message.answer(initial_prompt)
    response = await fetch_gpt_response(initial_prompt)
    await message.answer(response)


# Общий обработчик для всех состояний
@router.message(Command("lead"))
async def start_lead(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать! Начнем сбор вашей информации.")
    await process_next_field(message, state, 0)


async def process_next_field(message: Message, state: FSMContext, index: int):
    if index < len(fields):
        field, label, mandatory, is_image = fields[index]
        await state.update_data(current_field=field, current_index=index, is_image=is_image)
        await message.answer(f"Пожалуйста, предоставьте {label}")
    else:
        success = await save_data_db(state)
        if success:
            await message.answer("Спасибо, что предоставили всю информацию! Данные успешно отправлены в Bitrix24.")
            await continue_conversation(message)
        else:
            await message.answer("Произошла ошибка при сохранении данных. Пожалуйста, попробуйте снова.")




async def continue_conversation(message: Message):
    initial_prompt = "Чем еще я могу вам помочь?"
    response = await fetch_gpt_response(initial_prompt)
    await message.answer(response)



@router.message(Command("info"))
async def info_handler(message: Message):
    await message.answer("Это команда-заглушка для /info. Здесь будет информация.")


# Функция получения ответа от GPT-4
async def fetch_gpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Act as a friendly manager from https://yoowills.by and respond to user queries.You can say to user write command /lead to start registration or /info for information"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Error generating GPT-4 response: {str(e)}")
        return "Извините, произошла ошибка при обработке вашего запроса."


@router.message()
async def generic_message_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    if 'current_field' in data and 'current_index' in data:
        current_field = data.get('current_field')
        current_index = data.get('current_index')
        is_image = data.get('is_image', False)

        if is_image and message.photo:
            photo = message.photo[-1]  # Get the highest resolution photo
            photo_file = await bot.get_file(photo.file_id)
            photo_dir = 'photos'
            if not os.path.exists(photo_dir):
                os.makedirs(photo_dir)
            photo_path = f"{photo_dir}/{photo.file_id}.jpg"
            await bot.download_file(photo_file.file_path, photo_path)
            await state.update_data({current_field: photo_path})
        elif not is_image:
            await state.update_data({current_field: message.text})
        else:
            await message.answer("Пожалуйста, отправьте изображение.")

        await process_next_field(message, state, current_index + 1)
    else:
        if message.text.startswith('/'):
            return  # Ignore other commands

        prompt = message.text
        response = await fetch_gpt_response(prompt)
        await message.answer(response)


#Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
