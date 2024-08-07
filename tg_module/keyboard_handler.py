from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class KeyboardHandler:

    def create_kb(self, choices: list[str]):
        kb_list = []
        for choice in choices:
            kb_list.append([KeyboardButton(text=str(choice))])

        keyboard = ReplyKeyboardMarkup(
            keyboard=kb_list,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Воспользуйтесь меню:"
        )
        return keyboard

    def main_kb(self, user_telegram_id: int):
        kb_list = [
            [KeyboardButton(text="📖 О нас"), KeyboardButton(text="👤 Профиль")],
            [KeyboardButton(text="📝 Заполнить анкету"), KeyboardButton(text="📚 Каталог")]
        ]
        if user_telegram_id:
            kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
        keyboard = ReplyKeyboardMarkup(
            keyboard=kb_list,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Воспользуйтесь меню:"
        )
        return keyboard
