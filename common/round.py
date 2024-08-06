from dataclasses import dataclass

from task_type import TaskType


@dataclass
class Round:
    round_id: int
    image: str  # path
    task_type: TaskType
    text_for_instructor: str
    right_answer: str
    choices: list[str]
