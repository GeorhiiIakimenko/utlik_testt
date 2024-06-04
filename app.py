import logging
from telethon import TelegramClient, events
import openai
import aiohttp

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI API key
openai.api_key = 'APi key'

# Your API ID and Hash from https://my.telegram.org
api_id = 29536561
api_hash = '13ee70158dd2ba67d56e36093272fc55'
phone = '+79935654280'

# Create the client and connect
client = TelegramClient('userbot_session', api_id, api_hash)

# User states for managing data collection
user_states = {}

# Functions to get and set user state
def get_user_state(user_id):
    return user_states.get(user_id, {})

def set_user_state(user_id, state):
    user_states[user_id] = state

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

# Function to send data to Bitrix24
async def send_data_to_bitrix(data):
    bitrix_webhook_url = 'https://b24-kw5z35.bitrix24.by/rest/11/ffqo36u9m5t1zydv/crm.lead.add.json'
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
            'UF_CRM_1716463005': data.get('birth_date'),
            'UF_CRM_1716463034': data.get('issue_date'),
            'UF_CRM_1716463053': data.get('expiration_date'),
            'UF_CRM_1716463073': data.get('passport_main_page'),
            'UF_CRM_1716463102': data.get('passport_30_31_page'),
            'UF_CRM_1716463116': data.get('passport_registration_page'),
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


async def process_next_field(event, state, index):
    if index < len(fields):
        field, label, mandatory, is_image = fields[index]
        state['current_field'] = field
        state['current_index'] = index
        state['is_image'] = is_image
        await event.respond(f"Пожалуйста, предоставьте {label}")
    else:
        success = await send_data_to_bitrix(state)
        if success:
            await event.respond("Спасибо, что предоставили всю информацию! Данные успешно отправлены в Bitrix24.")
            await continue_conversation(event)
        else:
            await event.respond("Произошла ошибка при отправке данных. Пожалуйста, попробуйте снова.")


async def continue_conversation(event):
    initial_prompt = "Чем еще я могу вам помочь?"
    response = await fetch_gpt_response(initial_prompt)
    await event.respond(response)


async def fetch_gpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Act as a friendly manager from https://yoowills.by and respond to user queries. You can say to user write command /lead to start registration or /info for information"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Error generating GPT-4 response: {str(e)}")
        return "Извините, произошла ошибка при обработке вашего запроса."


@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    initial_prompt = "Привет! Чем я могу вам помочь? Вы можете использовать команду /lead для начала регистрации или /info для получения информации."
    await event.respond(initial_prompt)


@client.on(events.NewMessage(pattern='/lead'))
async def lead_handler(event):
    state = get_user_state(event.sender_id)
    state['current_index'] = 0
    set_user_state(event.sender_id, state)
    await process_next_field(event, state, 0)


@client.on(events.NewMessage(pattern='/message (.*)'))
async def message_handler(event):
    phone_number = event.pattern_match.group(1)
    async with client.conversation(phone_number) as conv:
        try:
            # Sending a test message
            await conv.send_message("Hello! Welcome to Yoowills! How can I assist you today? If you need information, you can type /info or if you're ready to start registering, just type /lead. I'm here to help!")
            await event.respond(f"Сообщение отправлено пользователю с номером {phone_number}.")
        except Exception as e:
            await event.respond(f"Не удалось отправить сообщение пользователю с номером {phone_number}. Ошибка: {str(e)}")


@client.on(events.NewMessage)
async def generic_handler(event):
    if event.message.message.startswith('/'):
        return  # Ignore other commands

    state = get_user_state(event.sender_id)
    if 'current_field' in state and 'current_index' in state:
        current_field = state['current_field']
        current_index = state['current_index']
        is_image = state['is_image']

        if is_image and event.message.photo:
            photo = event.message.photo  # Get the photo
            file = await client.download_media(photo)
            state[current_field] = file
        elif not is_image:
            state[current_field] = event.message.message
        else:
            await event.respond("Пожалуйста, отправьте изображение.")

        state['current_index'] = current_index + 1
        set_user_state(event.sender_id, state)
        await process_next_field(event, state, current_index + 1)
    else:
        prompt = event.message.message
        response = await fetch_gpt_response(prompt)
        await event.respond(response)


async def main():
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        await client.sign_in(phone, input('Enter the code: '))
    logger.info("Client started")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        client.loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Client stopped")
