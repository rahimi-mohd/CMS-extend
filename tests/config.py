from dataclasses import dataclass

"""Some config data for the test"""


@dataclass
class User:
    username: str
    password: str
    user_type: str


@dataclass
class Patient:
    # TODO: add details later for patient details page test
    first_name: str
    last_name: str
    ic_number: str
    tel_number: str
