from dataclasses import dataclass


@dataclass
class Message:
    message_id: int = None
    text: str = None
    is_successful: bool = False
    image: str = None  # path

    # for tg
    tg_id: str = None
    username: str = None
    reply_text: str = None
    file_path: str = None
