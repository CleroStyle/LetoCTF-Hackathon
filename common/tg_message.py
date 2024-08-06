from dataclasses import dataclass


class TgMessage:
    text: str = None
    image: str = None   # path
    choices: list[str] = None
