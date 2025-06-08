from dataclasses import dataclass
from application.models import User, Account


@dataclass
class UserInfo:
    user: User
    account_list: list[Account]
