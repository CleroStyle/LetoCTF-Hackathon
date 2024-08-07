import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from secret_env import BOT_TOKEN
from behavior import Behavior

TOKEN = BOT_TOKEN


class TGBot:

    def __init__(self, token: str):
        self._bot = Bot(token)
        self._dp = Dispatcher()

        self._behavior = Behavior(self._dp, self._bot)
        self._behavior.configure()

    async def start(self):
        await self._dp.start_polling(self._bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    tg_bot = TGBot(TOKEN)
    asyncio.run(tg_bot.start())
