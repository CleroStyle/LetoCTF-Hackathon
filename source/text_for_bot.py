from dataclasses import dataclass


@dataclass
class TextForBot:
    hello = "Здравствуй, игрок!"
    rule = "Правила игры: бла бла"

    are_you_ready = "Готов ли ты к новому вызову?"
    do_yo_wanna = "Хочешь сыграть?"
