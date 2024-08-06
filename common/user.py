from dataclasses import dataclass
import enum

from common.round import Round


class StatusUser(enum.IntEnum):
    not_auth = 0        # не авторизован
    not_playing = 1     # не хочет играть
    finding = 2         # в поиске пары
    in_match = 3        # нашел пару, не играет
    instructor = 4      # в игре, инструктор
    sapper = 5           # в игре, сапер


@dataclass
class User:
    tg_id: str
    tg_username: str = None
    rating: int = 0

    status: StatusUser = StatusUser.not_auth

    current_round: Round = None
    current_dialog = None

    teammate = None

    count_current_round: int = 0




