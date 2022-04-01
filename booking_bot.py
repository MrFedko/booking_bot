import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from info import file_id

token = file_id.token
bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
class Form(StatesGroup):
    date = State() 
    time = State() 
    size = State()
    name = State()
    telephone = State()

@dp.message_handler(commands="start")
async def start_message(message: types.Message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1=types.KeyboardButton('👉🏻 ПЕРЕЙТИ К БРОНИРОВАНИЮ 👈🏻')
    markup.add(item1)
    await message.answer("""Я помогу Вам забронировать стол🤗
Пару уточнений и все будет готово👌🏻

Нажмите на кнопку 
«Перейти к бронированию», и мы начнём.
Она спряталась внизу 🙈""",reply_markup=markup)
    
@dp.message_handler(lambda message: message.text == 'chat_id')
async def message_date(message: types.Message):
    await message.answer(message.chat.id)

@dp.message_handler(lambda message: message.text == '👉🏻 ПЕРЕЙТИ К БРОНИРОВАНИЮ 👈🏻')
async def message_date(message: types.Message):
    await Form.date.set()
    await message.answer("Здесь нам нужна точная дата Вашего визита 🧐")

@dp.message_handler(state=Form.date)
async def get_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await Form.next()
    await message.answer("""В котором часу? 
Напоминаю, что мы работаем с 12:00 до 23:00""")
    
@dp.message_handler(state=Form.time)
async def get_time(message: types.Message, state: FSMContext):
    await Form.next()
    async with state.proxy() as data:
        data['time'] = message.text
    await message.answer('На какое количество гостей?')
    
@dp.message_handler(state=Form.size)
async def get_size(message: types.Message, state: FSMContext):
    await Form.next()
    async with state.proxy() as data:
        data['size'] = message.text
    await message.answer('Подскажите Ваше имя и фамилию, пожалуйста🥰')
    
@dp.message_handler(state=Form.name)
async def get_name(message: types.Message, state: FSMContext):
    await Form.next()
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Нам нужен Ваш номер телефона, обязательно точный, чтобы мы могли Вам перезвонить - и всё готово ☎️ ')
    
@dp.message_handler(state=Form.telephone)
async def get_telephone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['telephone'] = message.text
    await message.answer("""Я передал информацию нашим хостес 🤌🏻
Они скоро с Вами свяжутся и подтвердят резерв 🤗""")
    new_message = ''
    async with state.proxy() as data:
        date, time, size, name, telephone = data['date'], data['time'], data['size'], data['name'], data['telephone']
        new_message += f'{message.from_user.username}\n\nДата: {date}\nВремя: {time}\nКоличество гостей: {size}\nИмя гостя: {name}\nНомер телефона: {telephone}'
    await bot.send_message(file_id.chat_id, new_message) 
    await message.answer_photo('AgACAgIAAxkBAAICmGIQTamNcbDVa5dLQRTMUtfmmsUhAAKNujEbuYSBSEkanxXtHmtkAQADAgADeAADIwQ')
        
@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
    return True

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)