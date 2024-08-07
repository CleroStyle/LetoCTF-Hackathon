from dataclasses import dataclass

from common.type_round import type_round


@dataclass
class Round:
    path_image: str
    type: type_round
    instructor_text: str
    version_answer: list
    answer: str
