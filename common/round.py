from dataclasses import dataclass
from datetime import datetime

import enum

from common.type_round import TypeRound

# from common.task_type import TaskType < dialog


class RoundStatus(enum.Enum):
    not_sending = 0
    started = 1
    finished = 2
    failed = 3


@dataclass
class Round:
    round_id: int
    task_type: TypeRound
    text_for_instructor: str
    right_answer: str
    choices: list[str]
    status: RoundStatus = RoundStatus.not_sending
    time: datetime = None
    image: str = None     # path
