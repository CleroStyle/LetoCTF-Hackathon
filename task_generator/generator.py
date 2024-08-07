from common.round import Round
from common.message import Message
from common.for_rounds.round_type import RoundType
from common.for_rounds.colors import Colors
from common.for_rounds.directions import Directions
import random


class Generator:
    """
    generate_round(self, type: type_round, count: int)
    type - тип вопроса (код, цвет, направление)
    count - кол-во вариантов в ответе
    count_version - кол-во вариантов ответа у сапёра
    """

    def get_round(self):
        random_round_type = random.choices((RoundType.code, RoundType.color, RoundType.direction))
        return self.generate_round(random_round_type[0], count=random.randint(1, 3),
                                   count_version=random.randint(3, 6))

    def generate_round(self, round_type: RoundType, count: int = 3, count_version: int = 4):
        answer = self.generate_answer(round_type=round_type, count=count)
        generate_round = Round(
            round_id=random.randint(1, 10000),
            task_type=round_type,
            right_answer=answer,
            text_for_instructor=self.generate_instructor_text(round_type, answer),
            choices=self.generate_version_answer(round_type, count_version, count, answer),
            image=self.get_image(round_type)
        )
        return generate_round

    @staticmethod
    def get_successful_message():
        msg = Message(
            message_id=random.randint(1, 10000),
            text="Бомба успешно обезврежена!",
            is_successful=True
        )
        return msg

    @staticmethod
    def get_fail_message():
        msg = Message(
            message_id=random.randint(1, 10000),
            text="Вы не успели, бомба была взорвана!",
            is_successful=False
        )
        return msg

    def generate_version_answer(self, round_type: RoundType, count_version: int, count: int, answer: str) -> list[str]:
        version = []
        for i in range(count_version):
            version.append(self.generate_answer(round_type, count))
        version.append(answer)
        random.shuffle(version)
        return version

    @staticmethod
    def get_image(round_type: RoundType):
        text = ""
        if round_type == RoundType.color:
            text = "source\\bomb_colors.png"
        elif round_type == RoundType.code:
            text = "source\\bomb_numbers.png"
        elif round_type == RoundType.direction:
            text = "source\\bomb_directions.png"
        return text

    def generate_answer(self, round_type: RoundType, count: int):
        if round_type == RoundType.color:
            text = self.generate_answer_for_colors(count)
        elif round_type == RoundType.code:
            text = self.generate_answer_for_codes(count)
        elif round_type == RoundType.direction:
            text = self.generate_answer_for_directions(count)
        return text
    
    def generate_instructor_text(self, type: RoundType, generate_str: str):
        text = ""
        if type == RoundType.color:
            text = self.generate_text_for_color(generate_str)
        elif type == RoundType.code:
            text = self.generate_text_for_code(generate_str)
        elif type == RoundType.direction:
            text = self.generate_text_for_message(generate_str)
        return text

    @staticmethod
    def generate_text_for_color(generate_str: str):
        returned_str = f"Саперу нужно перерезать: <b>{generate_str}</b> провода"
        return returned_str

    @staticmethod
    def generate_text_for_code(generate_str: str):
        returned_str = f"Саперу необходимо ввести следующую комбинацию: <b>{generate_str}</b>"
        return returned_str
    

    @staticmethod
    def generate_text_for_message(generate_str: str):
        returned_str = f"Вам необходимо указать правильные направления сапёру: <b>{generate_str}</b>"
        return returned_str

    @staticmethod
    def generate_answer_for_codes(count: int):
        returned_str = ""
        for i in range(count):
            returned_str += str(random.randint(0, 9))
        return returned_str

    @staticmethod
    def generate_answer_for_directions(count: int):
        list_str = []
        directions_list = [str(direction.value) for direction in Directions]
        for i in range(count):
            list_str.append(str(directions_list[random.randint(0, len(directions_list) - 1)]))
        return ', '.join(list_str)

    @staticmethod
    def generate_answer_for_colors(count: int):
        list_str = []
        colors_list = [str(color.value) for color in Colors]
        for i in range(count):
            list_str.append(str(colors_list[random.randint(0, len(colors_list) - 1)]))
        return ', '.join(list_str)


if __name__ == '__main__':
    generator = Generator()

    while True:
        s = input()
        match s:
            case "gen":
                round = generator.get_round()
                print(round)
