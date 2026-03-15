import pytest
from Cinemascope.utils.data_generator import Datagenerator


class TestMovieLifecycle:
    """
    Тест жизненного цикла фильма с отдельными функциями для каждого шага
    """

    # ===== ШАГ 1: Проверка отсутствия =====
    def verify_movie_absent(self, db_helper, movie_name):
        """Проверяет что фильма нет в БД"""
        movie = db_helper.get_movie_by_name(movie_name)
        assert movie is None, f"❌ Фильм '{movie_name}' уже существует!"
        print("✅ [1/5] Фильм отсутствует в БД")
        return True

    # ===== ШАГ 2: Создание фильма =====
    def create_movie(self, super_admin, movie_data):
        """Создает фильм через API и возвращает его ID"""
        response = super_admin.api.movies_api.create_movie(movie_data)
        assert response.status_code == 201
        movie_id = response.json().get('id')
        print(f"✅ [2/5] Фильм создан, ID: {movie_id}")
        return movie_id

    # ===== ШАГ 3: Проверка наличия =====
    def verify_movie_present(self, db_helper, movie_id, expected_data):
        """Проверяет что фильм появился в БД с правильными данными"""
        movie = db_helper.get_movie_by_id(movie_id)
        assert movie is not None, "❌ Фильм не найден в БД!"
        assert movie.name == expected_data['name']
        assert movie.price == expected_data['price']
        print("✅ [3/5] Фильм найден в БД, данные совпадают")
        return movie

    # ===== ШАГ 4: Удаление фильма =====
    def delete_movie(self, super_admin, movie_id):
        """Удаляет фильм через API"""
        response = super_admin.api.movies_api.delete_movie(movie_id)
        assert response.status_code == 200
        print("✅ [4/5] Фильм удален через API")
        return response

    # ===== ШАГ 5: Проверка отсутствия после удаления =====
    def verify_movie_absent_after_deletion(self, db_helper, movie_id):
        """Проверяет что фильм исчез из БД после удаления"""
        movie = db_helper.get_movie_by_id(movie_id)
        assert movie is None, "❌ Фильм все еще существует в БД!"
        print("✅ [5/5] Фильм отсутствует в БД после удаления")
        return True

    def test_movie_lifecycle(self, super_admin, db_helper):
        """
        Только ЭТОТ метод - тест. Он вызывает все шаги по порядку.
        """
        # Подготовка данных
        movie_data = Datagenerator.generate_movie_data()
        movie_name = movie_data["name"]

        print("\n🎬 ТЕСТ ЖИЗНЕННОГО ЦИКЛА ФИЛЬМА")
        print("=" * 50)

        # ШАГ 1: Проверяем что фильма нет
        self.verify_movie_absent(db_helper, movie_name)

        # ШАГ 2: Создаем фильм
        movie_id = self.create_movie(super_admin, movie_data)

        # ШАГ 3: Проверяем что фильм появился
        self.verify_movie_present(db_helper, movie_id, movie_data)

        # ШАГ 4: Удаляем фильм
        self.delete_movie(super_admin, movie_id)

        # ШАГ 5: Проверяем что фильм исчез
        self.verify_movie_absent_after_deletion(db_helper, movie_id)

        print("\n" + "=" * 50)
        print("✅ ВСЕ ШАГИ ЖИЗНЕННОГО ЦИКЛА УСПЕШНО ПРОЙДЕНЫ!")
        print("=" * 50)