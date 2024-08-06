from generator import generator
from common.type_round import type_round

obj = generator.generate_round(type_round.code, 10, 3)
print(obj.type)
print(obj.instructor_text)
print(obj.answer)
print(obj.version_answer)


