

### БОМБА проект

### Распределение задачи
БОТ:
    - task_generator - делает Денис
    - бизнес логику - Полина
    - sql_module - Месо
    - tg_module - Месо

Resources:
    - презентация - Паша
    - доситжения, рейтинг, статусы - Костя

#### Генератор тасков
Типы даннных:
**Message**:
- id: int (random)
- image: str (path)
- text: str
- is_succesfull: bool

**TaskType**: Enum
- color
- code
- directions

**ROUND**:
- id: int
- картинка: str (path)
- тип: str (ENUM)
- текст для инструктора
- правильный ответ
- варианты ответа: list[str]

Интерфейс модуля:
**API TASK module**
- get_round()
- get_succesfull_message(id: int) - return Message
- get_fail_message(id: int) - return Message

#### Модуль для работы с бд
API:
- add_new_user(tg_id: str) - создает нового пользователя с рейтингом ноль
 - get_rating_by_tg_id(tg_id: str) -> int
- update_rating(tg_id: int, value: int) - изменяет значение рейтинга на значение  value

#### Модуль для работы с тг 
_Главный модуль, запуск исходит из него_

API:
- send_message(text: str): отправляет текст
- send_image(path: str): отправляет картинку (берет её по пути)
- send_keyboard(keyboards: list[str]) (отправляет клавиатуру, кнопки в списке)

#### Модуль диалогов
_Генерация диалогов, использует генераторов тасков_

Типы данных:
**TgMessage**:
    text: str = None
    image: str = None   # path
    choices: list[str] = None
    

API:
- get_new_message

