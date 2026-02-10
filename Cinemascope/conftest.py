import requests
from Cinemascope.constants import BASE_URL, AUTH_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from Cinemascope.api.auth_api import AuthAPI
import pytest
import time
from Cinemascope.utils.data_generator import Datagenerator
ADMIN_CREDENTIALS = {
	"email": "api1@gmail.com",
	"password": "asdqwe123Q"
}


@pytest.fixture(scope="session")
def auth_session():
	session = requests.Session()
	session.headers.update(HEADERS)

	# Создаем AuthAPI клиент
	auth_api = AuthAPI(session)

	try:
		token = auth_api.authenticate(
			email=ADMIN_CREDENTIALS["email"],
			password=ADMIN_CREDENTIALS["password"]
		)

		print(f"Успешная аутентификация")
	except Exception as e:
		# Если что-то пошло не так, authenticate уже выбросил исключение
		print(f"Ошибка аутентификации: {e}")
		raise

	return session


@pytest.fixture(scope="session")
def session():
	"""
	Фикстура для создания HTTP-сессии.
	"""
	http_session = requests.Session()
	yield http_session
	http_session.close()


@pytest.fixture(scope="session")
def api_manager(auth_session):
	"""
	Фикстура для создания экземпляра CinemaApiManager.
	Используем auth_session (с токеном), а не обычную session.
	"""
	from Cinemascope.api.api_manager import CinemaApiManager  # ← можно импортировать здесь
	return CinemaApiManager(auth_session, BASE_URL)


@pytest.fixture
def movies_data():
	return Datagenerator.generate_movie_data()

@pytest.fixture
def created_movie(api_manager, movies_data):
	response = api_manager.movies_api.create_movie(movies_data, 201)
	return response.json()["id"]

@pytest.fixture
def update_payload():
	update_data = {
			"description": "Обновлённое описание",
			"price": 200,
			"location": "SPB",
			"published": False
		}
	return update_data

