from app.dao.base import BaseService
from app.users.models import Users


class UsersService(BaseService):
    model = Users
