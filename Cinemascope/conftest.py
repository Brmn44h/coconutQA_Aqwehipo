import sys
import os


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import requests
from Cinemascope.constants import BASE_URL
import pytest
from Cinemascope.utils.data_generator import Datagenerator
from Cinemascope.models.base_models import TestUser
from Cinemascope.resources.user_creds import SuperAdminCreds
from Cinemascope.api.api_manager import CinemaApiManager
from Cinemascope.entities.user import User
from Cinemascope.resources.user_roles import Roles
import time
import random
from sqlalchemy.orm import Session
from Cinemascope.db_requester.db_helpers import DBHelper
from Cinemascope.db_requester.db_client import get_db_session
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
    response = api_manager.movies_api.create_movie(movies_data)
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
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(*super_admin.creds)
    return super_admin


@pytest.fixture
def test_user() -> TestUser:
    random_password = Datagenerator.generate_random_password()

    return TestUser(
        email=Datagenerator.generate_random_email(),
        fullName=Datagenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )
@pytest.fixture(scope="function")
def creation_user_data(test_user):
    return TestUser(
        email=test_user.email,
        fullName=test_user.fullName,
        password=test_user.password,
        passwordRepeat=test_user.passwordRepeat,
        roles=test_user.roles,
        verified=True,
        banned=False
    )
@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()
    unique_email = f"common_user_{int(time.time())}_{random.randint(1000, 9999)}@example.com"

    super_admin.api.user_api.create_user({
        "email": unique_email,
        "password": creation_user_data.password,
        "fullName": creation_user_data.fullName,
        "roles": ["USER"],
        "verified": True,
        "banned": False
    })

    common_user = User(
        unique_email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session)
    #

    common_user.api.auth_api.authenticate(*common_user.creds)
    return common_user


@pytest.fixture
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session)


    super_admin.api.user_api.create_user(creation_user_data)
    admin.api.auth_api.authenticate(*admin.creds)
    return admin
@pytest.fixture
def registration_user_data():
    random_password = Datagenerator.generate_random_password()

    return {
        "email": Datagenerator.generate_random_email(),
        "fullName": Datagenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }

@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(Datagenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)