from Person import Person

class Reader:
    def __init__(self,
                 reader_number: str,
                 location_blueprint: str = None,
                 location_hospital: str = None, 
                 location_name: str = None,
                 ) -> None:
        
        self.reader_number = reader_number
        self.location_blueprint = location_blueprint
        self.location_hospital = location_hospital
        self.location_name = location_name
        self.authorized_personel = []
    
    def __str__(self):
        return f'{self.reader_number} - {self.location_name}'
    
    def __repr__(self):
        return f'Reader:{self.reader_number}'

    def __eq__(self, other):
        return int(self.reader_number) == int(other.reader_number)

    def add_person(self, person: Person) -> None:
        if person not in self.authorized_personel:
            self.authorized_personel.append(person)
    
    def remove_person(self, person: Person) -> None:
        self.authorized_personel.remove(person)