from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str


class Person:
    def __init__(self, name: Name):
        self.id = uuid.uuid1()
        self.name = name

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Person):
            return False
        return self.id == __value.id

    def __hash__(self) -> int:
        return hash(self.id)


a = Person(Name("Allen", "Lai"))
b = a
b.name = Name("Sunny", "Hsu")
assert a == b
