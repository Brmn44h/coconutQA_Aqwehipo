import requests
from Cinemascope.constants import BASE_URL
import pytest
from Cinemascope.utils.data_generator import Datagenerator
from Cinemascope.resources.user_creds import SuperAdminCreds
from Cinemascope.api.api_manager import CinemaApiManager
from Cinemascope.entities.user import User
ADMIN_CREDENTIALS = {
    "email": "api1@gmail.com",
    "password": "asdqwe123Q"
}


@pytest.fixture(scope="session")
def api_manager(session):
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


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = CinemaApiManager(session, BASE_URL)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        "[SUPER_ADMIN]",
        new_session)

    super_admin.api.auth_api.authenticate(*super_admin.creds)
    return super_admin

@pytest.fixture
def test_user():
    import time
    unique_email = f"testuser_{int(time.time())}@example.com"
    return {
        "email": unique_email,
        "password": "password123",
        "roles": ["USER"],
        "fullName": "Test User"
    }

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data