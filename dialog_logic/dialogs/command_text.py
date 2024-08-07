from dataclasses import dataclass


@dataclass
class CommandText:
    start = "/start"
    match = "🔆 MATCH 🔆"
    not_play = "😢 Не хочу играть 😢"

    start_play = "💥 Начать игру! 💥"
    rating = "🏆 Узнать рейтинг! 🏆"
