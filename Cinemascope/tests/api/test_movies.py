# Cinemascope/test_movies.py
import math
import pytest
import allure
from Cinemascope.models.base_models import MovieResponse, MoviesListResponse



class TestCinemaScope:
    @pytest.mark.smoke
    @allure.title("Проверка cоздания фильма")
    @allure.description("Тест проверяет создание фильма")
    def test_create_movie(self, super_admin, movies_data):
        response = super_admin.api.movies_api.create_movie(movies_data, 201)
        assert response.status_code == 201


    @pytest.mark.smoke
    @allure.title("Проверка корректности cоздания фильма")
    @allure.description("Тест проверяет, создание фильма выполнено корректно")
    def test_get_movie(self, super_admin, created_movie, movies_data):
        response = super_admin.api.movies_api.get_movie(created_movie, 200)
        movie = MovieResponse(**response.json())
        assert movie.id is not None
        assert movie.name == movies_data['name']
        assert movie.price == movies_data['price']
        assert movie.description == movies_data['description']

    @pytest.mark.smoke
    @allure.title("Проверка обновления фильма")
    @allure.description("Тест проверяет обновление фильма")
    def test_update_movie(self, super_admin, created_movie, movies_data, update_payload):
        super_admin.api.movies_api.update_movie(created_movie, update_payload, 200)
        get_response = super_admin.api.movies_api.get_movie(created_movie, 200)
        updated_movie = MovieResponse(**get_response.json())
        assert updated_movie.id == created_movie
        assert updated_movie.name == movies_data["name"]
        assert updated_movie.location == update_payload['location']
        assert updated_movie.published == update_payload['published']
        assert updated_movie.price == update_payload['price']
        assert updated_movie.description == update_payload['description']

    @pytest.mark.smoke
    @allure.title("Проверка удаления фильма")
    @allure.description("Тест проверяет удаление фильма")
    def test_delete_movie(self, super_admin, created_movie, movies_data):
        super_admin.api.movies_api.delete_movie(created_movie, 200)
        super_admin.api.movies_api.get_movie(created_movie, 404)


    @pytest.mark.roles
    @allure.title("Проверка удаления фильма пользоветелями")
    @allure.description("Тест проверяет удаление фильма пользователями: super_admin, admin, common_user")
    @pytest.mark.parametrize("user_role,expected_status", [("super_admin", 200), ("admin", 403), ("common_user", 403)])
    def test_delete_movie_roles(self, user_role, expected_status, super_admin, admin, common_user, movies_data):
        with allure.step("Создание тестового фильма"):
            response = super_admin.api.movies_api.create_movie(movies_data)
            assert response.status_code == 201
            movie_id = response.json()["id"]

        with allure.step(f"Выбор пользователя: {user_role}"):
            if user_role == "super_admin":
                user = super_admin
            elif user_role == "admin":
                user = admin
            else:
                user = common_user

        with allure.step(f"Попытка удаления фильма пользователем {user_role}"):
            user.api.movies_api.delete_movie(movie_id, expected_status)

        with allure.step(f"Проверка результата (ожидаемый статус: {expected_status})"):
            if expected_status == 200:
                with allure.step("Проверка что фильм удален"):
                    super_admin.api.movies_api.get_movie(movie_id, 404)
            else:
                with allure.step("Проверка что фильм остался в базе"):
                    get_response = super_admin.api.movies_api.get_movie(movie_id, 200)
                    movie = MovieResponse(**get_response.json())
                    assert movie.id == movie_id

    @allure.title("Проверка фильтрации")
    @allure.description("Тест проверяет фильтрацию фильма по параметрам")
    @pytest.mark.parametrize("minPrice,maxPrice,locations,genreId", [(1, 1000, "MSK", 1), (100, 500, "SPB", 2)])
    def test_get_movies_list(self, super_admin, minPrice, maxPrice, locations, genreId):
        with allure.step(f"Формирование параметров фильтрации: цена {minPrice}-{maxPrice}, локация {locations}, жанр {genreId}"):
            params = {
                "pageSize": 10,
                "page": 1,
                "minPrice": minPrice,
                "maxPrice": maxPrice,
                "locations": locations,
                "published": True,
                "genreId": genreId,
                "createdAt": "asc"
            }

        with allure.step("Выполнение запроса на получение списка фильмов"):
            list_response = super_admin.api.movies_api.get_movies_list(params)
            response_data = MoviesListResponse(**list_response.json())
        with allure.step("Проверка наличия обязательных полей в ответе"):
            assert response_data.movies is not None
            assert response_data.page == params['page']
            assert response_data.pageSize == params['pageSize']

        with allure.step("Проверка параметров пагинации"):
            assert response_data.page == params['page']
            assert response_data.pageSize == params['pageSize']

        with allure.step("Расчет и проверка количества страниц"):
            count = response_data.count
            movies = response_data.movies
            page_count = response_data.pageCount

            expected_page_count = math.ceil(count / params["pageSize"])
            assert page_count == expected_page_count, "Неверный 'pageCount'"

        assert len(movies) <= params["pageSize"], "Слишком много фильмов на странице"

        for movie in response_data.movies:
            assert movie.price is not None
            assert movie.published is True
            assert movie.genreId == genreId
            assert movie.location == locations

    @pytest.mark.negative
    @allure.title("Негативный тест на создание фильма")
    @allure.description("Тест проверяет создание фильма с пустым телом запроса")
    def test_create_movie_negative(self, super_admin, movies_data):
        super_admin.api.movies_api.create_movie({}, 400)

    @pytest.mark.negative
    @allure.title("Негативный тест на обновление фильма")
    @allure.description("Тест проверяет обновление несуществующего фильма")
    def test_update_movie_negative(self, super_admin, created_movie, movies_data, update_payload):
        non_existent_id = created_movie + 1000
        super_admin.api.movies_api.update_movie(non_existent_id, update_payload, 404)

    @pytest.mark.negative
    @allure.title("Негативный тест на удаление фильма")
    @allure.description("Тест проверяет удаление несуществующего фильма")
    def test_delete_movie_negative(self, super_admin, created_movie, movies_data):
        super_admin.api.movies_api.delete_movie({}, 404)

    @pytest.mark.negative
    @allure.title("Негативный тест на фильтрацию")
    @allure.description("Тест проверяет фильтрацию с некорректными параметрами")
    def test_get_movies_list_negative(self, super_admin):
        bad_params = {
            "pageSize": 0,
            "page": 0,
            "minPrice": -10000,

        }

        super_admin.api.movies_api.get_movies_list(bad_params, expected_status=400)

    @pytest.mark.negative
    @allure.title("Негативный тест на создание фильма")
    @allure.description("Тест проверяет создание фильма пользователем, у которого нет прав на создание")
    def test_create_movie_common_user(self, common_user, movies_data):
        response = common_user.api.movies_api.create_movie(movies_data, 403)
        assert response.json()["message"] == "Forbidden resource"


    @allure.title("Проверка создания фильма с проверкой в БД")
    @allure.description("Создает фильм через API и проверяет, что данные сохранились в БД")
    @pytest.mark.smoke
    @pytest.mark.db
    def test_create_movie_db_check(self, super_admin, movies_data, db_helper):

        with allure.step("Создание фильма через API"):
            response = super_admin.api.movies_api.create_movie(movies_data)
            assert response.status_code == 201
            movie_id = response.json()["id"]
            allure.attach(str(movie_id), "ID фильма", allure.attachment_type.TEXT)

        with allure.step("Проверка наличия фильма в БД"):
            movie_in_db = db_helper.get_movie_by_id(movie_id)
            assert movie_in_db is not None, "Фильм не найден в БД!"
            allure.attach(str(movie_in_db), "Данные из БД", allure.attachment_type.TEXT)

        with allure.step("Проверка соответствия данных"):
            assert movie_in_db.name == movies_data["name"], "Название не совпадает"
            assert movie_in_db.price == movies_data["price"], "Цена не совпадает"
            assert movie_in_db.location == movies_data["location"], "Локация не совпадает"
            assert movie_in_db.published == movies_data["published"], "Статус публикации не совпадает"
            assert movie_in_db.genre_id == movies_data["genreId"], "ID жанра не совпадает"
            assert movie_in_db.rating == movies_data["rating"], "Рейтинг не совпадает"
            assert movie_in_db.genre_id == movies_data["genreId"]
            assert movie_in_db.rating == movies_data["rating"]

        with allure.step("Очистка — удаление фильма из БД"):
            db_helper.delete_movie_by_id(movie_id)
            allure.attach("Фильм удален из БД", "Очистка", allure.attachment_type.TEXT)

