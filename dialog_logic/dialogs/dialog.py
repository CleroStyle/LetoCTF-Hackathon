from datetime import datetime, timedelta

from common.round import Round, RoundStatus
from .command_text import CommandText
from .match_making import MatchMaking
from common.user import User, StatusUser


class Dialog:
    def __init__(self, user: User, send_message, send_keyboards,
                 send_image,
                 match_making: MatchMaking, get_new_round):
        """
        :param tg_id: id в тг
        :param send_message: func(tg_id: str, message: Message)
        """

        self.user = user
        self.temp = self.start

        self._send_message = send_message
        self._send_keyboards = send_keyboards
        self._send_image = send_image
        self._match_making = match_making

        self._get_new_round = get_new_round
        self._round: Round | None = None

    def start(self, message: str = None):
        if message == CommandText.not_play:
            self.user.status = StatusUser.not_playing
            self._send_message(self.user.status, self.user.message)
        elif message == CommandText.start_play or message == CommandText.match:
            self.user.status = StatusUser.finding
            self._send_keyboards(self.user.tg_id, [CommandText.match, CommandText.not_play])
            self.temp = self.match
            return
        if self.user.status == StatusUser.not_playing:
            self._send_message(self.user.tg_id, "Хочешь сыграть?")
            self._send_keyboards(self.user.tg_id, [CommandText.match, CommandText.not_play])
            return
        self._send_message(self.user.tg_id, "Здравствуй, игрок!")
        self._send_message(self.user.tg_id, "Готов ли ты к новому вызову?")
        self._send_keyboards(self.user.tg_id, [CommandText.match, CommandText.not_play])

        self.temp = self.match

    def match(self, message: str):
        if message == CommandText.match:
            self._send_message(self.user.tg_id, "Ура! Уже ищем тебе тиммейта")
            self.user.status = StatusUser.finding
            teammate = self._match_making.add_matches(self.user)
            if teammate:
                self._send_message(self.user.tg_id, f"Ура, твой тиммейт {teammate.tg_username} c id {teammate.tg_id}")
                self._send_message(teammate.tg_id, f"Ура, твой тиммейт {self.user.tg_username} c id {self.user.tg_id}")

                self.user.status = StatusUser.in_match
                teammate.status = StatusUser.in_match

                round: Round = self._get_new_round()
                self.user.current_round = round
                teammate.current_round = round

                self._send_message(self.user.tg_id, f"Сгенирировали бомбу")
                self._send_message(teammate.tg_id, f"Сгенирировали бомбу")

                self._send_message(self.user.tg_id, f"Ищите друг друга и начинаете игру!")
                self._send_message(teammate.tg_id, f"Ищите друг друга и начинаете игру!")

                self._send_keyboards(self.user.tg_id, [CommandText.start_play, CommandText.not_play])
                self._send_keyboards(teammate.tg_id, [CommandText.start_play, CommandText.not_play])

                self.temp = self.game
                teammate.current_dialog.temp = teammate.current_dialog.game
            else:
                self._send_message(self.user.tg_id, f"Ждем новых игроков!")
        elif message == CommandText.not_play:
            self._send_message(self.user.tg_id, f"Если захочешь - пиши")
            self._send_keyboards(self.user.tg_id, [CommandText.start_play])
        else:
            self._send_message(self.user.tg_id, f"Используй клавиатуру!")
            self._send_keyboards(self.user.tg_id, [CommandText.match, CommandText.not_play])

    def game(self, message: str):
        if message == CommandText.start_play:
            if self.user.teammate is None or self.user.teammate.status in (StatusUser.not_playing,
                                                                           StatusUser.not_auth):
                self.user.status = StatusUser.finding
                self.user.teammate = None
                self.user.current_round = None
                self.user.count_current_round = 0
                self._send_keyboards(self.user.tg_id, [CommandText.match, CommandText.not_play])
                self.temp = self.match
                return
            if self.user.teammate.status == StatusUser.in_match:
                self._send_message(self.user.tg_id, f"Ждем подтверждения второго игрока!")
                self.user.status = StatusUser.instructor
            elif self.user.teammate.status == StatusUser.instructor:
                self.user.status = StatusUser.sapper
                self._send_message(self.user.tg_id, f"Ура! Ты - сапер")
                self._send_message(self.user.teammate.tg_id, f"Ура! Ты - инструктор")

                user = self.user    # sapper
                teammate = self.user.teammate   # instructor

                self._send_image(user.tg_id, user.current_round.image)
                self._send_image(teammate.tg_id, user.current_round.image)
                self._send_keyboards(user.tg_id, user.current_round.choices)
                self._send_message(teammate.tg_id, user.current_round.text_for_instructor)

                user.current_round.status = RoundStatus.started
                user.current_round.time = datetime.now()
                self._send_message(user.tg_id, f"Время пошло! У вас 3 секунды!!!")
                self._send_message(teammate.tg_id, f"Время пошло! У вас 3 секунды")

                self.temp = self.wait_right_word
                teammate.current_dialog.temp = teammate.current_dialog.wait_right_word
            else:
                self._send_message(self.user.tg_id, "Какая-то ошибка обратитесь к администратору!")
        else:
            if self.user.teammate:
                if self.user.status == StatusUser.instructor:
                    self._send_message(self.user.tg_id, f"Ждем подтверждения второго игрока!")
                    self._send_message(self.user.teammate.tg_id, f"Ждем только вас!!!")
                    self._send_keyboards(self.user.teammate.tg_id, [CommandText.start_play, CommandText.not_play])
                else:
                    self._send_keyboards(self.user.tg_id, [CommandText.start_play, CommandText.not_play])

            else:
                self.user.status = StatusUser.finding
                self.temp = self.match
                self._send_keyboards(self.user.tg_id, [CommandText.match, CommandText.not_play])


    def wait_right_word(self, message: str):
        if self.user.status == StatusUser.instructor:
            self._send_message(self.user.tg_id, f"Отвечать должен второй игрок!!!")
            return

        round = self.user.current_round
        if datetime.now() - timedelta(seconds=300) >= round.time:
            self._send_message(self.user.tg_id, "О, нет... Вы не успели")
            self._send_message(self.user.teammate.tg_id, "О, нет... Вы не успели")

            round.status = RoundStatus.failed

            teammate = self.user.teammate
            self._match_making.delete_match(self.user)
            self.user.status = StatusUser.finding
            teammate.status = StatusUser.finding
            teammate.count_current_round = 0
            self.user.count_current_round = 0

            self.user.current_round = None
            teammate.current_round = None

            self.user.rating -= 50
            teammate.rating -= 50
            self.temp = self.start

        elif message == self.user.current_round.right_answer:
            self._send_message(self.user.tg_id, "Это правильный ответ!")
            self._send_message(self.user.teammate.tg_id, "Это правильный ответ!")

            if self.user.count_current_round == 3:
                self._send_message(self.user.teammate.tg_id, "Вы были отличной коммандой")
                self._send_message(self.user.tg_id, "Вы были отличной коммандой")

                self.temp = self.match
                teammate = self.user.teammate
                teammate.current_dialog.temp = teammate.current_dialog.match

                self._match_making.delete_match(self.user)
                self.user.status = StatusUser.not_playing
                teammate.status = StatusUser.not_playing
                teammate.count_current_round = 0
                self.user.count_current_round = 0

                self.user.current_round = None
                teammate.current_round = None

                self.user.rating += 150
                teammate.rating += 150

                self.temp = self.match
                teammate.current_dialog.temp = teammate.current_dialog.match

                self._send_keyboards(self.user.tg_id, [CommandText.match])
                self._send_keyboards(teammate.tg_id, [CommandText.match])

                return

            self.user.current_round = self._get_new_round()
            teammate = self.user.teammate
            teammate.current_round = self.user.current_round

            self.user.count_current_round += 1
            teammate.count_current_round += 1

            self.user.status = StatusUser.finding
            teammate.status = StatusUser.finding

            self.user.rating += 100
            teammate.rating += 100
            self.temp = self.game
            teammate.current_dialog.temp = teammate.current_dialog.game

            self.user.status = StatusUser.in_match
            teammate.status = StatusUser.in_match

            self._send_message(self.user.tg_id, "Новый раунд! Вы готовы, дети?")
            self._send_message(teammate.tg_id, "Новый раунд! Вы готовы, дети?")

            self._send_keyboards(self.user.tg_id, [CommandText.start_play, CommandText.not_play])
            self._send_keyboards(teammate.tg_id, [CommandText.start_play, CommandText.not_play])

        else:
            self._send_message(self.user.tg_id, "О, нет буум!")
            self._send_message(self.user.teammate.tg_id, "О, нет, буум!")

            round.status = RoundStatus.failed

            teammate = self.user.teammate
            self._match_making.delete_match(self.user)
            self.user.status = StatusUser.not_playing
            teammate.status = StatusUser.not_playing
            teammate.count_current_round = 0
            self.user.count_current_round = 0

            self.user.current_round = None
            teammate.current_round = None

            self.user.rating -= 50
            teammate.rating -= 50

            self.temp = self.match
            teammate.current_dialog.temp = teammate.current_dialog.match

            self._send_keyboards(self.user.tg_id, [CommandText.match])
            self._send_keyboards(teammate.tg_id, [CommandText.match])


