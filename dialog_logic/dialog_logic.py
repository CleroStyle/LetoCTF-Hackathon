"""
    Модуль для генерации диалогов.
"""
from dialogs import *
from task_generator.task_generator import TaskGenerator
from common import User


class DialogLogic:
    storage: dict = dict()         # dict = {tg_id: user}
    match_making: MatchMaking = MatchMaking()
    task_generator: TaskGenerator = TaskGenerator()

    def process_new_message(self, tg_id: str, text: str):
        user = self.storage.get(tg_id)
        if user is None:
            user = User(tg_id)
            self.storage[tg_id] = user
            user.current_dialog = Dialog(user, self.send_message, self.send_keyboard, self.send_image,
                                         self.match_making, self.task_generator.get_round)
            user.current_dialog.temp(text)

        else:
            if text == CommandText.not_play:
                if user.teammate is not None:
                    user.teammate.current_dialog.temp = user.teammate.current_dialog.match
                    self.send_message(user.teammate.tg_id, f"Твой тиммейт не хочет играть!")
                    self.send_keyboard(user.teammate.tg_id,
                                       [CommandText.match, CommandText.rating, CommandText.not_play])

                self.match_making.delete_match(user)
                user.current_dialog.temp = user.current_dialog.start
            elif text == CommandText.rating:
                self.send_message(user.tg_id, f"Ваш рейтинг {user.rating}")
            else:
                user.current_dialog.temp(text)


    @staticmethod
    def send_message(tg_id: str, text: str):
        print(f"Отправлено сообщение {text} пользователю {tg_id}")

    @staticmethod
    def send_keyboard(tg_id: str, choices: list[str]):
        print(f"Отправлена клавиатура пользователю {tg_id}: {' '.join(choices)}")

    @staticmethod
    def send_image(tg_id: str, image: str):
        print(f"Отправлена картинка по пути {image} пользователю {tg_id}")


if __name__ == '__main__':
    dialog_logic = DialogLogic()
    while True:
        tg, *s = input().split()
        t = ' '.join(s)
        print(t)
        dialog_logic.process_new_message(tg, t)
