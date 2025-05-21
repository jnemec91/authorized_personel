"""
Person.py
This module defines the Person class, which represents a person in a system.
It includes all the necessary attributes that a person might have.
"""
class Person:
    """
    Person class
    """
    def __init__(self,
                 person_number: str,
                 first_name: str = None,
                 last_name: str = None,
                 card_number: str = None,
                 email: str = None,
                 ) -> None:

        self.person_number = person_number
        self.first_name = first_name
        self.last_name = last_name
        self.card_number = card_number
        self.email = email

    def __str__(self) -> str:
        return f'{self.person_number} - {self.first_name} {self.last_name}'

    def __repr__(self) -> str:
        return f'Person:{self.person_number}'
