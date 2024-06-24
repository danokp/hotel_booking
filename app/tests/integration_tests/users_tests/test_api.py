import pytest
from fastapi import status


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("harry@potter.com", "harry_potter", status.HTTP_200_OK),
        ("test@test.com", "test", status.HTTP_409_CONFLICT),
        ("germiona@grenjer.com", "grenjer123", status.HTTP_200_OK),
        ("abcde", "harry_potter", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_register_user(
    email: str, password: str, status_code: int, async_client, mocker
):
    mocker.patch("app.users.dao.UsersService.add")
    response = await async_client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("test@test.com", "test", status.HTTP_200_OK),
        ("daniil@example.com", "daniil", status.HTTP_200_OK),
        ("not_registed@user.com", "not_registed_user", status.HTTP_401_UNAUTHORIZED),
    ],
)
async def test_login_user(email: str, password: str, status_code: int, async_client):
    response = await async_client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code


async def test_logout_user(async_client):
    response = await async_client.post("/auth/logout")
    assert response.status_code == status.HTTP_200_OK
