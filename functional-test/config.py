from dataclasses import dataclass

"""Some config data for the test"""


@dataclass
class User:
    username: str
    password: str
    user_type: str
