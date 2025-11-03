"""
File B — Person manager with JSON import/export
"""

import json
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Person:
    name: str
    age: int
    city: str
    skills: List[str]

    def birthday(self):
        self.age += 1

    def add_skill(self, skill: str):
        self.skills.append(skill)


class PersonManager:
    def __init__(self):
        self.people: List[Person] = []

    def add_person(self, person: Person):
        self.people.append(person)

    def get_by_city(self, city: str):
        return [p for p in self.people if p.city.lower() == city.lower()]

    def save_to_file(self, filename="people.json"):
        with open(filename, "w", encoding="utf-8") as f:
            data = [asdict(p) for p in self.people]
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_from_file(self, filename="people.json"):
        with open(filename, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        self.people = [Person(**p) for p in raw_data]

    def summary(self):
        return {
            "total_people": len(self.people),
            "cities": list({p.city for p in self.people}),
            "all_skills": sorted({skill for p in self.people for skill in p.skills})
        }


def demo():
    manager = PersonManager()
    p1 = Person("Alice", 30, "London", ["C++"])
    p2 = Person("Bob", 25, "Berlin", ["docker", "git"])
    p3 = Person("Charlie", 40, "London", ["SQL"])

    manager.add_person(p1)
    manager.add_person(p2)
    manager.add_person(p3)

    manager.save_to_file("people.json")
    print("Saved to file.")

    manager.load_from_file("people.json")
    print("Loaded:", manager.summary())


if __name__ == "__main__":
    demo()
