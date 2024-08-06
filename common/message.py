from dataclasses import dataclass


@dataclass
class Message:
    message_id: int
    text: str
    is_successful: bool
    image: str = None  # path
