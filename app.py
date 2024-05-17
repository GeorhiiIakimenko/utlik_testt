import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from aiogram.filters.state import State, StatesGroup

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
    leasing_item = State()
    leasing_cost = State()
    leasing_quantity = State()
    leasing_advance = State()
    leasing_currency = State()
    leasing_duration = State()
    place_of_birth = State()
    gender = State()
    criminal_record = State()
    document = State()
    citizenship = State()
    series = State()
    number = State()
    issue_date = State()
    expiration_date = State()
    issued_by = State()
    registration_index = State()
    registration_country = State()
    registration_region = State()
    registration_district = State()
    registration_locality = State()
    registration_street = State()
    registration_house = State()
    registration_building = State()
    registration_apartment = State()
    residence_index = State()
    residence_country = State()
    residence_region = State()
    residence_district = State()
    residence_locality = State()
    residence_street = State()
    residence_house = State()
    residence_building = State()
    residence_apartment = State()
    workplace_name = State()
    position = State()
    work_experience = State()
    income = State()
    hr_phone = State()
    marital_status = State()
    dependents_count = State()
    education = State()
    military_duty = State()
    relative_surname = State()
    relative_first_name = State()
    relative_patronymic = State()
    relative_phone = State()
    passport_main_page = State()
    passport_30_31_page = State()
    passport_registration_page = State()

# Labels for client data fields with mandatory information
fields = [
    ("surname", "Фамилия*", True),
    ("first_name", "Имя*", True),
    ("patronymic", "Отчество*", True),
    ("mobile_phone", "Мобильный телефон*", True),
    ("additional_phone", "Дополнительный телефон", False),
    ("email", "Email", False),
    ("passport_data", "Паспортные данные", False),
    ("birth_date", "Дата рождения*", True),
    ("personal_number", "Личный номер*", True),
    ("leasing_item", "Наименование предмета лизинга*", True),
    ("leasing_cost", "Стоимость*", True),
    ("leasing_quantity", "Количество*", True),
    ("leasing_advance", "Аванс", False),
    ("leasing_currency", "Валюта договора*", True),
    ("leasing_duration", "Срок договора*", True),
    ("place_of_birth", "Место рождения", False),
    ("gender", "Пол*", True),
    ("criminal_record", "Судимость*", True),
    ("document", "Документ", False),
    ("citizenship", "Гражданство", False),
    ("series", "Серия*", True),
    ("number", "Номер*", True),
    ("issue_date", "Дата Выдачи*", True),
    ("expiration_date", "Срок действия*", True),
    ("issued_by", "Кем выдан*", True),
    ("registration_index", "Индекс", False),
    ("registration_country", "Страна*", True),
    ("registration_region", "Область", False),
    ("registration_district", "Район", False),
    ("registration_locality", "Населенный пункт*", True),
    ("registration_street", "Улица*", True),
    ("registration_house", "Дом*", True),
    ("registration_building", "Строение, корпус", False),
    ("registration_apartment", "Квартира", False),
    ("residence_index", "Индекс", False),
    ("residence_country", "Страна*", True),
    ("residence_region", "Область", False),
    ("residence_district", "Район", False),
    ("residence_locality", "Населенный пункт*", True),
    ("residence_street", "Улица*", True),
    ("residence_house", "Дом*", True),
    ("residence_building", "Строение, корпус", False),
    ("residence_apartment", "Квартира", False),
    ("workplace_name", "Наименование организации*", True),
    ("position", "Должность*", True),
    ("work_experience", "Стаж*", True),
    ("income", "Доход*", True),
    ("hr_phone", "Телефон отдела кадров или бухгалтерии*", True),
    ("marital_status", "Семейное положение*", True),
    ("dependents_count", "Количество иждивенцев", False),
    ("education", "Образование*", True),
    ("military_duty", "Воинская обязанность*", True),
    ("relative_surname", "Фамилия*", True),
    ("relative_first_name", "Имя*", True),
    ("relative_patronymic", "Отчество*", True),
    ("relative_phone", "Телефон*", True),
    ("passport_main_page", "Главный разворот*", True),
    ("passport_30_31_page", "Разворот 30-31*", True),
    ("passport_registration_page", "Разворот с регистрацией*", True),
]

# Обработчики состояний для сохранения данных в базе
async def save_data(state: FSMContext):
    data = await state.get_data()
    # Remove temporary state data
    data.pop('current_field', None)
    data.pop('current_index', None)

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

# Функция отправки данных в Bitrix24
async def send_data_to_bitrix(data):
    bitrix_webhook_url = 'https://yourdomain.bitrix24.com/rest/1/webhook/'
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
                f"Паспортные данные: {data.get('passport_data')}\n"
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

    async with aiohttp.ClientSession() as session:
        async with session.post(bitrix_webhook_url, json=lead_data) as response:
            if response.status == 200:
                return await response.json()
            else:
                logger.error(f"Error sending data to Bitrix24: {response.status}")
                return None

# Общий обработчик для всех состояний
@router.message(Command("lead"))
async def start_lead(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать! Начнем сбор вашей информации.")
    await process_next_field(message, state, 0)

async def process_next_field(message: Message, state: FSMContext, index: int):
    if index < len(fields):
        field, label, mandatory = fields[index]
        await state.update_data(current_field=field, current_index=index)
        await message.answer(f"Пожалуйста, предоставьте {label}")
    else:
        success = await save_data(state)
        if success:
            await message.answer("Спасибо, что предоставили всю информацию! Данные успешно отправлены в Bitrix24.")
        else:
            await message.answer("Произошла ошибка при сохранении данных. Пожалуйста, попробуйте снова.")


@router.message()
async def process_field(message: Message, state: FSMContext):
    data = await state.get_data()
    current_field = data.get('current_field')
    current_index = data.get('current_index')

    if current_field:
        await state.update_data({current_field: message.text})
        await process_next_field(message, state, current_index + 1)
    else:
        await message.answer("Привет! Я бот-менеджер. Чем могу помочь?")


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
