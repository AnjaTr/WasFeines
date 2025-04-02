from dataclasses import dataclass

@dataclass
class User:
    sub: str
    name: str
    email: str
    picture: str
    given_name: str
    family_name: str

