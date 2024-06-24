import pytest

from app.users.dao import UsersService


@pytest.mark.parametrize(
    "user_id,email,is_present",
    [
        (1, "test@test.com", True),
        (2, "daniil@example.com", True),
        (3, "", False),
    ],
)
async def test_users_find_by_id(user_id: int, email: str, is_present: bool):
    user = await UsersService.find_by_id(user_id)
    if is_present:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
