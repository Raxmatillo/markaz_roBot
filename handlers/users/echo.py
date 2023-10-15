import datetime
from aiogram import types
from data.config import ADMINS

from loader import dp, db


# Echo bot
@dp.message_handler(state='*')
async def bot_echo(message: types.Message):
    
    message_ = await message.forward(ADMINS[0])
    prev = datetime.datetime.today()
    prev_date = prev.strftime("%Y-%m-%d")
    db.add_message(message.chat.id, message_.message_id, push_date=prev_date)