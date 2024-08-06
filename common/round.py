from dataclasses import dataclass
from datetime import datetime

import enum

from common.for_rounds.round_type import RoundType


class RoundStatus(enum.Enum):
    not_sending = 0
    started = 1
    finished = 2
    failed = 3


@dataclass
class Round:
    round_id: int
    task_type: RoundType
    text_for_instructor: str
    right_answer: str
    choices: list[str]
    status: RoundStatus = RoundStatus.not_sending
    time: datetime = None
    image: str = None     # path
