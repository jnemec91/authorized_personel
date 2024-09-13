import openpyxl as opx
from Reader import Reader
from Person import Person
from Formater import change_string_format

class DataReader:
    def __init__(self, file_path, columns):
        self.file_path = file_path
        self.data = []
        self.columns = columns

    def read_data(self) -> list:
        self.data = []
        data = opx.load_workbook(self.file_path)
        sheet = data.active

        print(f'Reading data from {self.file_path}...')
        progress = 0
        complete = sheet.max_row
        for row in sheet.rows:
            progress += 1
            print(f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r")
            data_row = []
            for cell in row:
                if cell.column in self.columns:
                    if isinstance(cell.value, str):
                        data_row.append(cell.value.strip())
                    else:
                        data_row.append(cell.value)

            self.data.append(data_row)
        
        print('Data read complete.\n')
        return self.data
    

class ReaderMapper(DataReader):
    def __init__(self, file_path, columns=[2, 3, 4]) -> None:
        super().__init__(file_path, columns)
        self.read_data()


    def map_data(self) -> list:
        readers = []

        print('Mapping data...')

        progress = 0
        complete = len(self.data)
        for row in self.data:
            progress += 1
            print(f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r")            
            reader = Reader(reader_number=row[0],
                            location_blueprint=change_string_format(row[1]),
                            location_name=row[2])
            readers.append(reader)

        print('Data mapped.\n')
        return readers

    def get_readers(self):
        return self.map_data()


class PersonMapper(DataReader):
    def __init__(self, file_path, columns=[1,2,3,4,6]) -> None:
        super().__init__(file_path, columns)
        self.read_data()

    def map_data(self) -> list:
        people = []

        print('Mapping data...')

        progress = 0
        complete = len(self.data)
        for row in self.data:
            progress += 1
            print(f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r")
            person = Person(person_number=row[0],
                            first_name=row[3],
                            last_name=row[2],
                            card_number=row[4],
                            email=row[1])
            people.append(person)

        print('Data mapped.\n')
        return people

    def get_people(self):
        return self.map_data()



class AuthorizationMapper(DataReader):
    def __init__(self, file_path, readers, personel, columns=[1,2,3,4,5,6]) -> None:
        super().__init__(file_path, columns)
        self.read_data()
        self.readers = readers
        self.personel = personel
    
    def person_gen(self):
        for person in self.personel:
            yield person
        
    def reader_gen(self):
        for reader in self.readers:
            yield reader

    def map_data(self) -> list:
        authorizations = []
        print('Mapping data...')

        progress = 0
        complete = len(self.data)
        for row in self.data:
            progress += 1
            print(f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r")
            for reader in self.readers:
                if reader.location_blueprint == row[3] and reader.location_blueprint is not None:
                    reader.location_hospital = row[0]
                    if row[2] is not None:
                        reader.location_name = f'{row[1]} ({row[2]})'
                    else:
                        reader.location_name = row[1]
                        
                    personel = str(row[4]).casefold().split(), str(row[5]).casefold().split()

                    for person in personel:
                        if person != 'None':
                            for p in self.person_gen():
                                # print(set((p.first_name.casefold(), p.last_name.casefold())), set(person))
                                if set((p.first_name.casefold(), p.last_name.casefold())) == set(person):
                                    reader.add_person(p)

        print('Data mapped.\n')
        return self.readers

    
    def get_authorizations(self):
        return self.map_data()

