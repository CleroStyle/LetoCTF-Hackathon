from common.round import Round
from common.message import Message
from common.type_round import type_round
from common.colors import colors
from common.directions import directions
import random


class generator(object):

    '''
    generate_round(self, type: type_round, count: int)
    type - тип вопроса (код, цвет, направление)
    count - кол-во вариантов в ответе
    count_version - кол-во вариантов ответа у сапёра
    '''
    @classmethod
    def generate_round(self, type: type_round, count: int, count_version: int):
        answer = self.generate_answer(self, type=type, count=count)
        generate_round = Round()
        generate_round.type = type
        generate_round.answer = answer
        generate_round.path_image = self.get_image(type)
        generate_round.instructor_text = self.generate_instructor_text(self, type, answer)
        generate_round.version_answer = self.generate_version_answer(self, type, count_version, count, answer)
        return generate_round
    

    @classmethod
    def get_succesfull_message(self):
        mes = Message()
        mes.text = "Бомба успешно обезврежена!"
        mes.is_successful = True
        return mes
    

    @classmethod
    def get_fail_message(self):
        mes = Message()
        mes.text = "Вы не успели, бомба была взорвана!"
        mes.is_successful = False
        return mes

    
    def generate_version_answer(self, type: type_round, count_version: int, count: int, answer: str):
        version = []
        for i in range(count_version - 1):
            version.append(self.generate_answer(self, type, count))
        version.append(answer)
        random.shuffle(version)
        return version


    def get_image(self, type: type_round):
        text = ""
        if type == type_round.color:
            text = "source\\bomb_colors.png"
        elif type == type_round.code:
            text = "source\\bomb_numbers.png"
        else:
            text = "source\\bomb_diractions.png"
        return text


    def generate_answer(self, type: type_round, count: int):
        text = ""
        if type == type_round.color:
            text = self.generate_answer_for_colors(self, count)
        elif type == type_round.code:
            text = self.generate_answer_for_codes(self, count)
        else:
            text = self.generate_answer_for_directions(self, count)
        return text
    
    def generate_instructor_text(self, type: type_round, generate_str: str):
        text = ""
        if type == type_round.color:
            text = self.generate_text_for_color(generate_str)
        elif type == type_round.code:
            text = self.generate_text_for_code(generate_str)
        else:
            text = self.generate_text_for_message(generate_str)
        return text
    

    def generate_text_for_color(generate_str: str):
        returned_str = "Саперу нужно перерезать: " + generate_str + " провода"
        return returned_str
    

    def generate_text_for_code(generate_str: str):
        returned_str = "Саперу необходимо ввести следующую комбинацию: " + generate_str
        return returned_str
    

    def generate_text_for_message(generate_str: str):
        returned_str = "Вам необходимо указать правильные направления сапёру: " + generate_str
        return returned_str


    def generate_answer_for_codes(self, count: int):
        returned_str = ""
        for i in range(count):
            returned_str += str(random.randint(0, 9))
        return returned_str
        

    def generate_answer_for_directions(self, count: int):
        list_str = []
        directions_list = [str(direction.value) for direction in directions]
        for i in range(count):
            list_str.append(str(directions_list[random.randint(0, len(directions_list) - 1)]))
        return ', '.join(list_str)


    def generate_answer_for_colors(self, count: int):
        list_str = []
        colors_list = [str(color.value) for color in colors]
        for i in range(count):
            list_str.append(str(colors_list[random.randint(0, len(colors_list) - 1)]))
        return ', '.join(list_str)

    
        