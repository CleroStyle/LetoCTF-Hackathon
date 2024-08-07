"""
    Модуль для генерации диалогов.
"""
import asyncio
import logging

from common.message import Message
from .dialogs import *
from task_generator import Generator
from common import User


class DialogLogic:

    def __init__(self, send_message=None, send_image=None, send_keyboards=None):

        self._send_message = send_message
        self._send_image = send_image
        self._send_keyboards = send_keyboards

        self.storage: dict = dict()         # dict = {tg_id: user}
        self.match_making: MatchMaking = MatchMaking()
        self.task_generator: Generator = Generator()

    async def handle_message(self, message: Message):
        user = self.storage.get(message.tg_id)
        if user is None:
            user = User(
                tg_id=message.tg_id,
                tg_username=message.username
            )
            self.storage.update({message.tg_id: user})
            user.current_dialog = Dialog(user, self.send_message, self.send_keyboard, self.send_image,
                                         self.match_making, self.task_generator.get_round)
            await user.current_dialog.temp(message.text)
        else:
            await self.process_new_message(user, message.text)

    async def process_new_message(self, user: User, text: str):
        if text == CommandText.not_play:
            if user.teammate is not None:
                user.teammate.current_dialog.temp = user.teammate.current_dialog.match
                await self.send_message(user.teammate.tg_id, f"Твой тиммейт не хочет играть!")
                await self.send_keyboard(user.teammate.tg_id,
                                [CommandText.match, CommandText.rating, CommandText.not_play])

            self.match_making.delete_match(user)
            user.current_dialog.temp = user.current_dialog.start
        elif text == CommandText.rating:
            await self.send_message(user.tg_id, f"Ваш рейтинг {user.rating}")
        else:
            await user.current_dialog.temp(text)

    async def send_message(self, tg_id: str, text: str):
        if self._send_message:
            await self._send_message(tg_id, text)
        else:
            logging.warning(f"Domain: Функция отправки сообщения не преопределена")
        logging.info(f"Domain: Отправлено сообщение {text} пользователю {tg_id}")

    async def send_keyboard(self, tg_id: str, choices: list[str]):
        if self._send_keyboards:
            await self._send_keyboards(tg_id, choices)
        else:
            logging.warning(f"Domain: Функция отправки клавиатуры не преопределена")
        logging.info(f"Domain: Отправлена клавиатура пользователю {tg_id}: {' '.join(choices)}")

    async def send_image(self, tg_id: str, image: str):
        if self._send_image:
            await self._send_image(tg_id, image)
        else:
            logging.warning(f"Domain: Функция отправки картинки не преопределена")
        logging.info(f"Domain: Отправлена картинка по пути {image} пользователю {tg_id}")


if __name__ == '__main__':

    async def main():
        dialog_logic = DialogLogic()
        while True:
            tg, *s = input().split()
            t = ' '.join(s)
            print(t)
            await dialog_logic.process_new_message(tg, t)

    asyncio.run(main())
