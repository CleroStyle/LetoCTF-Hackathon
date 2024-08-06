from dataclasses import dataclass


class Message:
    message_id: int
    image: str = None  # path
    text: str
    is_successful: bool
