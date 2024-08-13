import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import psycopg2

# Настройки бота
API_TOKEN = 'YOUR_BOT_API_TOKEN'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="student_society",
    user="student_user",
    password="your_password",
    host="localhost"
)
cursor = conn.cursor()


# Определение состояний
class Form(StatesGroup):
    full_name = State()
    phone_number = State()
    email = State()
    institute = State()
    group_name = State()
    course_number = State()
    study_program = State()
    manhole_cover = State()

# Обработчик команды /start
@dp.message(Command(commands=["start"]))
async def start(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите ваше ФИО.")
    await state.set_state(Form.full_name)

# Обработка ввода ФИО
@dp.message(Form.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Введите ваш номер телефона.")
    await state.set_state(Form.phone_number)

# Обработка ввода номера телефона
@dp.message(Form.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer("Введите ваш email.")
    await state.set_state(Form.email)

# Обработка ввода email
@dp.message(Form.email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Из какого вы института? (например, ИЭУБ, ИНГЭ, ИКСиИБ и т.д.)")
    await state.set_state(Form.institute)

# Обработка ввода института
@dp.message(Form.institute)
async def process_institute(message: types.Message, state: FSMContext):
    await state.update_data(institute=message.text)
    await message.answer("Введите полное название учебной группы.")
    await state.set_state(Form.group_name)

# Обработка ввода названия учебной группы
@dp.message(Form.group_name)
async def process_group_name(message: types.Message, state: FSMContext):
    await state.update_data(group_name=message.text)
    await message.answer("На каком вы курсе?")
    await state.set_state(Form.course_number)

# Обработка ввода номера курса
@dp.message(Form.course_number)
async def process_course_number(message: types.Message, state: FSMContext):
    await state.update_data(course_number=message.text)
    await message.answer("Введите ваше направление обучения.")
    await state.set_state(Form.study_program)

# Обработка ввода направления обучения
@dp.message(Form.study_program)
async def process_study_program(message: types.Message, state: FSMContext):
    await state.update_data(study_program=message.text)
    await message.answer("Почему канализационные люки круглые?")
    await state.set_state(Form.manhole_cover)

# Обработка ответа на вопрос про люки
@dp.message(Form.manhole_cover)
async def process_manhole_cover(message: types.Message, state: FSMContext):
    await state.update_data(manhole_cover=message.text)

    # Сохранение данных в базу данных
    user_data = await state.get_data()
    cursor.execute("""
        INSERT INTO students (full_name, phone_number, email, institute, group_name, course_number, study_program, manhole_cover)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (user_data["full_name"], user_data["phone_number"], user_data["email"], user_data["institute"], user_data["group_name"], user_data["course_number"], user_data["study_program"], user_data["manhole_cover"]))
    conn.commit()

    # Отправка ссылки на группы СНО
    sno_links = {
        "ИЭУБ": "https://t.me/link_to_IEUB_group",
        "ИНГЭ": "https://t.me/link_to_INGE_group",
        "ИКСиИБ": "https://t.me/link_to_IKSiIB_group",   #  на будущее ))
        "ИПиПП": "https://t.me/link_to_IPiPP_group",
        "ИСТИ": "https://t.me/link_to_ISTI_group",
        "ИМРИТТС": "https://t.me/link_to_IMRITTS_group",
        "ИФН": "https://t.me/link_to_IFN_group"
    }

    institute = user_data["institute"]
    await message.answer(f"Спасибо! Ваши данные сохранены.\nСсылка на группу вашего института: {sno_links.get(institute, 'https://vk.com/sno_kubstu?ysclid=lzsylxerbe615975611')}")

    await state.clear()

# Главная функция для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())