"""
reader.py
This module defines the Reader class, which represents a reader in a system.
It includes all the necessary attributes that a reader might have and all methods to manage it.
"""
from person import Person

class Reader:
    """
    Reader class
    This class represents a reader in a system.
    """
    def __init__(self,
                 reader_number: str,
                 location_blueprint: str = None,
                 location_hospital: str = None, 
                 location_name: str = None,
                 abi_location: str = None,
                 ) -> None:

        self.reader_number = reader_number
        self.location_blueprint = location_blueprint
        self.location_hospital = location_hospital
        self.location_name = location_name
        self.abi_location = abi_location
        self.authorized_personel = []

    def format_number(self):
        while len(self.reader_number) < 5:
            self.reader_number = '0' + self.reader_number

        return self.reader_number

    def __str__(self):
        return f'{self.reader_number} - {self.location_name}'

    def __repr__(self):
        return f'Reader:{self.reader_number}'

    def __eq__(self, other):
        return self.reader_number == other.reader_number

    def add_person(self, person: Person) -> None:
        if person not in self.authorized_personel:
            self.authorized_personel.append(person)

    def remove_person(self, person: Person) -> None:
        self.authorized_personel.remove(person)
