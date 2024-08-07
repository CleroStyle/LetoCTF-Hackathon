import logging
import pathlib

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.types import InputFile

from common.message import Message
from sql_module.storage import Storage
from dialog_logic import DialogLogic
from keyboard_handler import KeyboardHandler


class Behavior:

    def __init__(self, dp: Dispatcher, bot: Bot):
        self._dp = dp
        self._bot = bot

        self._dialog: DialogLogic = DialogLogic(
            send_message=self.send_message,
            send_keyboards=self.send_keyboard,
            send_image=self.send_photo
        )

    def configure(self):
        logging.info(f"bot: Configure behavior")
        router_test = Router(name="test")

        router_test.message.register(self.message_handler)

        router_test.callback_query.register(self.callback_query_handler)

        self._dp.include_router(router_test)

    async def callback_query_handler(self, callback_query: types.CallbackQuery):
        logging.info(f"bot: Received callback_query from id={callback_query.message.chat.id} data={callback_query.data}")

        await self._dialog.handle_message(Message(
            tg_id=str(callback_query.message.chat.id),
            text=callback_query.data,
            username=callback_query.message.chat.username,
        ))

    async def message_handler(self, message: types.Message) -> None:
        logging.info(f"bot: Received message from user id={message.chat.id} with text={message.text}")

        await self._dialog.handle_message(Message(
            tg_id=str(message.chat.id),
            text=message.text,
            username=message.chat.username,
        ))

    async def send_message(self,
                           chat_id: str,
                           text: str,
                           markup=None):
        await self._bot.send_message(chat_id, text, reply_markup=markup,
                                     parse_mode=ParseMode.HTML)

    async def send_keyboard(self,
                            chat_id: str,
                            choices: list[str] = None,
                            text: str = "Напоминаю, что ты играешь в <b>супер</b> крутую игру - <b> БОМБА 💣</b>"):
        keyboard = KeyboardHandler().create_kb(choices)
        await self._bot.send_message(chat_id, text, reply_markup=keyboard,
                                     parse_mode=ParseMode.HTML)

    async def send_photo(self, chat_id: str, path: str):
        logging.info(f"bot: Sending image by {path} to chat_id={chat_id}")
        path = pathlib.Path("..\\" + path)
        photo=types.FSInputFile(path.absolute())
        await self._bot.send_photo(
            chat_id=chat_id,
            photo=photo
        )
