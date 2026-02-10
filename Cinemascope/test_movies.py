# Cinemascope/cinemascope.py
import pytest


class TestCinemaScope:
	def test_create_movie(self, api_manager, movies_data):
		print("1. Создание фильма")
		response = api_manager.movies_api.create_movie(movies_data, 201)
		created_movie = response.json()
		movie_id = created_movie.get('id')
		assert "id" in created_movie, "Фильм не создан"
		assert created_movie['name'] == movies_data['name'], "Название фильма не совпадает"
		assert created_movie['price'] == movies_data['price'], "Цена фильма не совпадает"
		assert created_movie['description'] == movies_data['description'], "Описание фильма не совпадает"


	def test_get_movie(self, api_manager, created_movie, movies_data):
		print("2. Проверка создания фильма")
		response = api_manager.movies_api.get_movie(created_movie, 200)
		movie = response.json()
		assert "id" in movie, "Фильм не создан"
		assert  movie['name'] == movies_data['name'], "Название фильма не совпадает"
		assert movie['price'] == movies_data['price'], "Цена фильма не совпадает"
		assert  movie['description'] == movies_data['description'], "Описание фильма не совпадает"

	def test_update_movie(self, api_manager, created_movie, movies_data, update_payload):
		print("3. Проверка обновления фильма")
		response = api_manager.movies_api.update_movie(created_movie, update_payload, 200)
		get_response = api_manager.movies_api.get_movie(created_movie, 200)
		updated_movie = get_response.json()
		assert updated_movie["id"] == created_movie
		assert updated_movie["name"] == movies_data["name"], "Имя фильма изменилось (не должно было!)"
		assert  updated_movie['location'] == update_payload['location'], "Cтрана фильма не совпадает"
		assert updated_movie['published'] == update_payload['published'], "Опубликовано"
		assert updated_movie['price'] == update_payload['price'], "Цена фильма не совпадает"
		assert  updated_movie['description'] == update_payload['description'], "Описание фильма не совпадает"

	def test_delete_movie(self,api_manager, created_movie, movies_data):
		print("4. Проверка удаления фильма")
		response = api_manager.movies_api.delete_movie(created_movie, 200)
		get_response = api_manager.movies_api.get_movie(created_movie, 404)


	def test_get_movies_list(self, api_manager):

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

		list_response = api_manager.movies_api.get_movies_list(params)
		movies = list_response.json().get("movies", [])
		for movie in movies:
			price = movie.get("price")
			assert price is not None, f"Фильм {movie.get('id')} без цены"
			assert 1 <= price <= 1000, f"Цена {price} вне диапазона"

		print(f"   ✓ Все {len(movies)} фильмов в правильном ценовом диапазоне")
		print("\n✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО")
