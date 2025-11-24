from apps.core.base_crud import BaseCRUDManager
from apps.users.models import User


class UserCRUDManager(BaseCRUDManager):
    def __init__(self):
        self.model = User


user_manager = UserCRUDManager()