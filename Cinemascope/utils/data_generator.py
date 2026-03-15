import random
import string
import time
from faker import Faker
import datetime

faker = Faker()


class Datagenerator:
    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """

        letters = random.choice(string.ascii_letters)
        digits = random.choice(string.digits)

        special_chars = "?#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(8, 16)
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_unique_movie_name():
        timestamp = int(time.time())
        adjectives = ["Великий", "Страшный", "Смешной", "Загадочный", "Эпичный"]
        titles = ["Фильм", "Кино", "История", "Приключение", "Сюжет"]
        random_word = random.choice(adjectives) + " " + random.choice(titles)
        return f"{random_word} {timestamp}"

    @staticmethod
    def generate_movie_data():
        """Генерирует полные данные для фильма"""
        return {
            "name": Datagenerator.generate_unique_movie_name(),
            "imageUrl": f"https://picsum.photos/seed/{int(time.time())}/600/400",
            "price": random.randint(100, 1000),
            "description": "Тестовое описание фильма для автоматизированного тестирования",
            "location": random.choice(["MSK", "SPB"]),
            "published": random.choice([True, False]),
            "genreId": random.randint(1, 5)
        }

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': Datagenerator.generate_random_email(),
            'full_name': Datagenerator.generate_random_name(),
            'password': Datagenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }

    @staticmethod
    def generate_random_int(min_value: int = 1, max_value: int = 100) -> int:
        return random.randint(min_value, max_value)
