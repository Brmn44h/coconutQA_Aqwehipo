import requests
from Auth.constants import BASE_URL, AUTH_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
import pytest
from Auth.utils.data_generator import Datagenerator
from Auth.utils.custom_requester import CustomRequester
from Auth.api.api_manager import CinemaApiManager
import time
@pytest.fixture
def movies_data():


    unique_name = f"Тестовый фильм {int(time.time())}"
    return {
        "name":  unique_name,
        "imageUrl": "https://example.com/image.jpg",
        "price": 350,
        "description": "Эпичная фантастика о путешествиях сквозь червоточины",
        "location": "MSK",
        "published": True,
        "genreId": 1

    }


ADMIN_CREDENTIALS = {
    "email": "api1@gmail.com",
    "password": "asdqwe123Q"
}


@pytest.fixture(scope="session")
def auth_session():



	session = requests.Session()
	session.headers.update(HEADERS)

	# Логинимся с админскими кредами
	response = session.post(
		f"{AUTH_URL.rstrip('/')}{LOGIN_ENDPOINT}",
		json=ADMIN_CREDENTIALS
	)

	print(f"Статус логина: {response.status_code}")

	if response.status_code != 200:
		print(f"Ошибка логина: {response.text}")
		raise Exception(f"Не удалось залогиниться как админ: {response.status_code}")

	token = response.json().get("accessToken")
	if not token:
		print("Токен не получен!")
		print(f"Полный ответ: {response.text}")
		raise Exception("Токен не получен в ответе")

	print(f"✅ Токен получен: {token[:50]}...")


	session.headers.update({"Authorization": f"Bearer {token}"})
	print(f"🔐 Заголовки сессии: {dict(session.headers)}")

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
    from Auth.api.api_manager import CinemaApiManager  # ← можно импортировать здесь
    return CinemaApiManager(auth_session, BASE_URL)
