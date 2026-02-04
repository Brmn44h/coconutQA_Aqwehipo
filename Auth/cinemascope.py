# Auth/cinemascope.py
import pytest


class TestCinemaScope:



	def test_full_movie_lifecycle(self, api_manager, movies_data):



		print("1. Создаём фильм")
		create_response = api_manager.create_and_validate(movies_data, 201)
		movie_id = create_response.json().get('id')
		assert movie_id is not None, "Фильм создан без ID"
		print(f"   Фильм создан с ID: {movie_id}")


		print("2. Получаем созданный фильм")
		get_response = api_manager.get_and_validate(movie_id, 200)
		assert get_response.json()['id'] == movie_id, "ID не совпадают"
		print(f"   Фильм получен: {get_response.json()['name']}")



		print("3. Обновляем фильм")
		update_payload = {
			"description": "Обновлённое описание",
			"price": 200,
			"location": "SPB",
			"published": False
		}
		update_response = api_manager.update_movie(movie_id, update_payload)
		assert update_response.status_code == 200, "Фильм не обновлён"

		# Проверяем обновление
		get_after_update = api_manager.get_and_validate(movie_id, 200)
		assert get_after_update.json()["description"] == update_payload["description"]
		print("   Фильм успешно обновлён")

		# 4. УДАЛЕНИЕ ФИЛЬМА
		print("4. Удаляем фильм")
		delete_response = api_manager.delete_movie(movie_id)
		assert delete_response.status_code == 200, "Ошибка удаления"

		# Проверяем, что фильма больше нет
		get_after_delete = api_manager.get_movie(movie_id)
		assert get_after_delete.status_code == 404, "Фильм не удалился"
		print("   Фильм успешно удалён")

		# 5. ПРОВЕРКА СПИСКА ФИЛЬМОВ С ФИЛЬТРАМИ
		print("5. Проверяем фильтрацию списка фильмов")
		params = {
			"pageSize": 10,
			"page": 1,
			"minPrice": 1,
			"maxPrice": 1000,
			"locations": ["MSK", "SPB"],
			"published": True,
			"genreId": 1,
			"createdAt": "asc"
		}

		list_response = api_manager.get_movies_list(params)
		assert list_response.status_code == 200, "Ошибка получения списка"

		movies = list_response.json().get("movies", [])
		for movie in movies:
			price = movie.get("price")
			assert price is not None, f"Фильм {movie.get('id')} без цены"
			assert 1 <= price <= 1000, f"Цена {price} вне диапазона"

		print(f"   ✓ Все {len(movies)} фильмов в правильном ценовом диапазоне")
		print("\n✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО")