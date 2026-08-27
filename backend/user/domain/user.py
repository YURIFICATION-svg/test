from dataclasses import dataclass #__init__()을 생략 가능

@dataclass
class User:
    id: str
    name: str
    password: str