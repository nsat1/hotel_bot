from db.base_repository import BaseRepository
from models import User


class UserRepository(BaseRepository[User]):
    pass


users = UserRepository(User)
