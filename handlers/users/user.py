from aiogram import types

from loader import dp, db
from data.config import ADMINS


from filters import AdminFilter



@dp.message_handler(AdminFilter(), content_types = types.ContentTypes.ANY)
async def admin_reply(message: types.Message):
    if isinstance(message.reply_to_message, types.Message):
        reply_m = message.reply_to_message
        if reply_m.forward_from and reply_m.forward_from.id:
            await message.copy_to(reply_m.forward_from.id, reply_markup=message.reply_markup)
        else:
            message_id_ = reply_m.message_id
            chat_id = db.get_message_chat_id(message_id_)
            await message.copy_to(chat_id, reply_markup=message.reply_markup)
    else:
        pass