"""
data_readers.py
This module defines the DataReader class and its subclasses, which are responsible for reading data
from Excel files. And mapping the data to the appropriate classes.
"""
from typing import Iterator
import openpyxl as opx
from reader import Reader
from person import Person
from formater import change_string_format

class DataReader:
    """
    This class is responsible for reading data from an Excel file.
    It uses the openpyxl library to read the data and map it to the appropriate classes.
    It is a base class for the ReaderMapper, PersonMapper, AuthorizationMapper,
    and ABILocationMapper classes.
    """
    def __init__(self, file_path: str, columns: list[int] | None) -> None:
        self.file_path = file_path
        self.data = []
        self.columns = columns

    def read_data(self) -> list:
        """
        This method reads data from the Excel file and stores it in the data attribute.
        """
        self.data = []
        data = opx.load_workbook(self.file_path)
        sheet = data.active

        print(f'Reading data from {self.file_path}...')
        progress = 0
        complete = sheet.max_row
        for row in sheet.rows:
            progress += 1
            print(
                f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r") # pylint: disable=C0301
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
    """
    This class is responsible for mapping data from the Excel file to the Reader class.
    It inherits from the DataReader class and uses the map_data method to map the data.
    """
    def __init__(self, file_path:str, columns=None) -> None:
        if columns is None:
            columns = [2, 3, 4]
        super().__init__(file_path, columns)
        self.read_data()


    def map_data(self) -> list:
        """
        This method maps the data to the Reader class.
        It creates a list of reader objects and assigns the appropriate values to each object.
        """
        readers = []

        print('Mapping data...')

        progress = 0
        complete = len(self.data)
        for row in self.data:
            progress += 1
            print(
                f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r") # pylint: disable=C0301
            reader = Reader(reader_number=str(row[0]),
                            location_blueprint=change_string_format(row[1]),
                            location_name=row[2])
            reader.format_number()
            readers.append(reader)

        print('Data mapped.\n')
        return readers

    def get_readers(self) -> list:
        """
        This method returns the mapped data.
        """
        return self.map_data()


class PersonMapper(DataReader):
    """
    This class is responsible for mapping data from the Excel file to the Person class.
    It inherits from the DataReader class and uses the map_data method to map the data.
    """
    def __init__(self, file_path:str, columns:list[int] | None=None) -> None:
        if columns is None:
            columns = [1,2,3,4,6]
        super().__init__(file_path, columns)
        self.read_data()

    def map_data(self) -> list:
        """
        This method maps the data to the Person class.
        It creates a list of person objects and assigns the appropriate values to each object.
        """
        people = []

        print('Mapping data...')

        progress = 0
        complete = len(self.data)
        for row in self.data:
            progress += 1
            print(
                f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r") # pylint: disable=C0301
            person = Person(person_number=row[0],
                            first_name=row[3],
                            last_name=row[2],
                            card_number=row[4],
                            email=row[1])
            people.append(person)

        print('Data mapped.\n')
        return people

    def get_people(self) -> list:
        """
        This method returns the mapped data.
        """
        return self.map_data()



class AuthorizationMapper(DataReader):
    """
    This class is responsible for mapping data from the Excel file to the Reader and Person classes.
    It inherits from the DataReader class and uses the map_data method to map the data.
    It requires a list of readers and personel objects to initialize.
    """
    def __init__(self,
                 file_path:str,
                 readers:list[Reader],
                 personel:list[Person],
                 columns:list[int] | None=None) -> None:

        if columns is None:
            columns = [1,2,3,4,5,6]
        super().__init__(file_path, columns)
        self.read_data()
        self.readers = readers
        self.personel = personel

    def person_gen(self) -> Iterator[Person]:
        """
        This method is a generator that yields each person in the personel list.
        """
        for person in self.personel:
            yield person

    def reader_gen(self) ->  Iterator[Reader]:
        """
        This method is a generator that yields each reader in the readers list.
        """
        for reader in self.readers:
            yield reader

    def map_data(self) -> list:
        """
        This method maps the data to the Reader and Person classes.
        It iterates through the data and assigns the appropriate values to the reader
        and person objects.
        """
        print('Mapping data...')

        progress = 0
        complete = len(self.data)
        for row in self.data:
            progress += 1
            print(
                f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r")  # pylint: disable=C0301
            for reader in self.readers:
                if str(reader.location_blueprint).strip() == str(row[3]).strip() and reader.location_blueprint is not None:  # pylint: disable=C0301
                    reader.location_hospital = str(row[0])
                    if row[2] is not None:
                        reader.location_name = f'{row[1]} ({row[2]})'
                    else:
                        reader.location_name = row[1]
                    personel = str(row[4]).casefold().split(), str(row[5]).casefold().split()

                    for person in personel:
                        if person != 'None':
                            for p in self.person_gen():
                                if set((p.first_name.casefold(), p.last_name.casefold())) == set(person): # pylint: disable=C0301
                                    reader.add_person(p)

        print('Data mapped.\n')
        return self.readers


    def get_authorizations(self) -> list:
        """
        This method returns the mapped data.
        """
        return self.map_data()


class ABILocationMapper(DataReader):
    """
    This class is responsible for mapping data from the Excel file to the Reader class.
    It inherits from the DataReader class and uses the map_data method to map the data.
    """
    def __init__(self, file_path:str, readers:list[Reader], columns:list[int] | None=None) -> None:
        if columns is None:
            columns = [2, 5]
        super().__init__(file_path, columns)
        self.read_data()
        self.readers = readers

    def map_data(self) -> list:
        """
        This method maps the data to the Reader class.
        """
        print('Mapping data...')
        progress = 0
        complete = len(self.data)
        for row in self.data:
            progress += 1
            print(
                f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r") # pylint: disable=C0301
            for reader in self.readers:
                if int(reader.reader_number) == int(row[0]):
                    reader.abi_location = row[1]

        print('Data mapped.\n')
        return self.readers

    def get_readers(self) -> list:
        """
        This method returns the mapped data.
        """
        return self.map_data()


class VelinMapper(DataReader):
    """
    This class is responsible for mapping data from the Excel file to the Reader class.
    It inherits from the DataReader class and uses the map_data method to map the data.
    """
    def __init__(self,
                 file_path: str,
                 readers: list[Reader],
                 columns: list[int] | None = None) -> None:

        if columns is None:
            columns = [2]
        super().__init__(file_path, columns)
        self.read_data()
        self.readers = readers

    def map_data(self) -> list:
        """
        This method maps the data to the Reader class.
        It creates a new reader if not found in list instance was initialized with.
        It iterates through the data and assigns the appropriate values to the readers.
        """
        print('Mapping data...')
        progress = 0
        complete = len(self.data)
        for row in self.data:
            reader_found = False
            # add readers that are not in authorizations
            progress += 1
            print(
                f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r") # pylint: disable=C0301

            if len(row[0]) < 5:
                row[0] = f'0{row[0]}'

            for reader in self.readers:
                if int(reader.reader_number) == int(row[0]):
                    reader_found = True
                    break

            if not reader_found:
                reader = Reader(reader_number=row[0])
                self.readers.append(reader)


        print('Data mapped.\n')
        return self.readers

    def get_readers(self) -> list:
        """
        This method returns the mapped data.
        """
        return self.map_data()
