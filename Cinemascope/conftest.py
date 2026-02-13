import requests
from Cinemascope.constants import BASE_URL
import pytest
from Cinemascope.utils.data_generator import Datagenerator

ADMIN_CREDENTIALS = {
	"email": "api1@gmail.com",
	"password": "asdqwe123Q"
}


@pytest.fixture(scope="session")
def api_manager(session):
	from Cinemascope.api.api_manager import CinemaApiManager
	manager = CinemaApiManager(session, BASE_URL)

	manager.auth_api.authenticate(
		email=ADMIN_CREDENTIALS["email"],
		password=ADMIN_CREDENTIALS["password"]
	)

	return manager


@pytest.fixture(scope="session")
def session():
	http_session = requests.Session()
	yield http_session
	http_session.close()


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
