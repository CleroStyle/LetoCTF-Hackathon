"""
Task Generator - модуль для генерации тасков
"""

from common.message import Message
from common.round import Round


class TaskGenerator:
    def get_round(self) -> Round:
        pass

    def get_successful_message(self, round_id: int) -> Message:
        pass

    def get_fail_message(self, round_id: int) -> Message:
        pass
