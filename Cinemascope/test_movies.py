# Cinemascope/test_movies.py
import pytest
import math


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
		assert movie['name'] == movies_data['name'], "Название фильма не совпадает"
		assert movie['price'] == movies_data['price'], "Цена фильма не совпадает"
		assert movie['description'] == movies_data['description'], "Описание фильма не совпадает"

	def test_update_movie(self, api_manager, created_movie, movies_data, update_payload):
		print("3. Проверка обновления фильма")
		response = api_manager.movies_api.update_movie(created_movie, update_payload, 200)
		get_response = api_manager.movies_api.get_movie(created_movie, 200)
		updated_movie = get_response.json()
		assert updated_movie["id"] == created_movie
		assert updated_movie["name"] == movies_data["name"], "Имя фильма изменилось (не должно было!)"
		assert updated_movie['location'] == update_payload['location'], "Cтрана фильма не совпадает"
		assert updated_movie['published'] == update_payload['published'], "Опубликовано"
		assert updated_movie['price'] == update_payload['price'], "Цена фильма не совпадает"
		assert updated_movie['description'] == update_payload['description'], "Описание фильма не совпадает"

	def test_delete_movie(self, api_manager, created_movie, movies_data):
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
		response_data = list_response.json()
		assert "movies" in response_data, "Нет поля 'movies' в ответе"
		assert "count" in response_data, "Нет поля 'count' в ответе"
		assert "page" in response_data, "Нет поля 'page' в ответе"
		assert "pageSize" in response_data, "Нет поля 'pageSize' в ответе"
		assert "pageCount" in response_data, "Нет поля 'pageCount' в ответе"

		assert response_data['page'] == params['page'], "Неверный Page"
		assert response_data['pageSize'] == params['pageSize']

		count = response_data['count']
		movies = response_data['movies']
		page_count = response_data['pageCount']

		expected_page_count = math.ceil(count / params["pageSize"])
		assert page_count == expected_page_count, "Неверный 'pageCount'"

		assert len(movies) <= params["pageSize"], "Слишком много фильмов на странице"


		for movie in movies:
			movie_id = movie.get("id", "без ID")

			price = movie.get("price")
			assert price is not None, f"Фильм {movie.get('id')} без цены"
			assert 1 <= price <= 1000, f"Цена {price} вне диапазона"

			published = movie.get("published")
			assert published is not None, f"Фильм {movie_id} без поля published"
			assert published == params[
				"published"], f"Фильм {movie_id} имеет published={published}, ожидалось {params['published']}"

			genre_id = movie.get("genreId")
			assert genre_id is not None, f"Фильм {movie_id} без genreId"
			assert genre_id == params[
				"genreId"], f"Фильм {movie_id} имеет genreId={genre_id}, ожидалось {params['genreId']}"

			movie_location = movie.get("location")
			assert movie_location is not None
			assert movie_location in params["locations"]



	print("\n✅ ВСЕ ПОЗИТИВНЫЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО")
	def test_create_movie_negative(self, api_manager, movies_data):
		print("6. Создание фильма без тела запроса")
		response = api_manager.movies_api.create_movie({}, 400)


	def test_update_movie_negative(self, api_manager, created_movie, movies_data, update_payload):
		print("7. Проверка обновления несуществующего фильма")
		non_existent_id = created_movie + 1000
		response = api_manager.movies_api.update_movie(non_existent_id, update_payload, 404)

	def test_delete_movie_negative(self, api_manager, created_movie, movies_data):
		print("8. Проверка удаления несуществующего фильма")
		response = api_manager.movies_api.delete_movie({}, 404)

	def test_get_movies_list_negative(self, api_manager):
		print("9. Проверяем фильтрацию списка фильмов с некорректными Params")
		bad_params = {
			"pageSize": 0,
			"page": 0,
			"minPrice": -10000,

		}

		list_response = api_manager.movies_api.get_movies_list(bad_params, expected_status=400)

	print("\n✅ ВСЕ НЕГАТИВНЫЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО")





