
from Cinemascope.utils.data_generator import Datagenerator
from Cinemascope.resources.user_roles import Roles
from typing import List
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from venv import logger


class RegistrationUserData(BaseModel):
    email: str = Field(..., min_length=8)
    fullName: str
    password: str
    passwordRepeat: str
    roles: List[Roles]
    banned: Optional[bool] = None
    verified: Optional[bool] = None

    @field_validator("email")
    def check_symbols(cls, email: str):
        if "@" not in email:
            raise ValueError("должен содержать @")
        return email
def get_registration_user_data():
    random_password = Datagenerator.generate_random_password()
    return {
    "email": Datagenerator.generate_random_email(),
    "fullName": Datagenerator.generate_random_name(),
    "password": random_password,
    "passwordRepeat": random_password,
    "roles": [Roles.USER.value]
    }


def test_registration_user_data(registration_user_data):
    user = RegistrationUserData(**registration_user_data)
    assert user.email is not None
    assert user.fullName is not None
    assert user.password == user.passwordRepeat
    assert Roles.USER in user.roles
    json_data = user.model_dump_json(exclude_unset=True)
    logger.info(f"{user.email=}\n{user.fullName=}\n{user.password=}\n{Roles.USER.value=}\n{json_data=}")

def test_both_fixtures(test_user, creation_user_data, registration_user_data):
    RegistrationUserData(**registration_user_data)
    RegistrationUserData(**test_user)
    RegistrationUserData(**creation_user_data)




