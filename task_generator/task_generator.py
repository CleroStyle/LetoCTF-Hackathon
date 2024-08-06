"""
Task Generator - модуль для генерации тасков
"""
import random

from common.message import Message
from common.round import Round
from common.task_type import TaskType


class TaskGenerator:
    def get_round(self) -> Round:
        return Round(
            round_id=random.randint(1, 1000),
            text_for_instructor="Выбери правильный ответ",
            task_type=TaskType.color,
            right_answer="красный",
            choices=["красный", "желтый", "фиолетовый"]
        )

    def get_successful_message(self, round_id: int) -> Message:
        return Message(
            message_id=random.randint(1, 10000),
            text="Base text",
            is_successful=True
        )

    def get_fail_message(self, round_id: int) -> Message:
        return Message(
            message_id=random.randint(1, 10000),
            text="Base text",
            is_successful=True
        )
