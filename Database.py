"""
database.py
This module defines the Database class, which is responsible for managing the database connection
and performing CRUD operations on the database.
It uses SQLite as the database engine and provides methods to create tables,
insert data, retrieve data.
"""
import sqlite3
from person import Person
from reader import Reader


class Database:
    """
    This class is responsible for managing the database connection 
    and performing CRUD operations on the database.
    It uses SQLite as the database engine.
    """
    def __init__(self, db_name:str) -> None:
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self) -> None:
        """
        Create the tables in the database if they do not exist.
        """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS people
                            (person_number TEXT PRIMARY KEY,
                            first_name TEXT,
                            last_name TEXT,
                            card_number TEXT,
                            email TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS readers
                            (reader_number TEXT PRIMARY KEY,
                            location_blueprint TEXT,
                            location_hospital TEXT,
                            location_name TEXT,
                            abi_location TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS authorizations
                            (person_number TEXT,
                            reader_number TEXT,
                            FOREIGN KEY(person_number) REFERENCES people(person_number),
                            FOREIGN KEY(reader_number) REFERENCES readers(reader_number))''')

    def insert_person(self, person: Person) -> None:
        """
        Insert a person into the database.
        """
        self.cursor.execute('''INSERT INTO people
                            (person_number, first_name, last_name, card_number, email)
                            VALUES (?, ?, ?, ?, ?)''',
                            (person.person_number,
                             person.first_name,
                             person.last_name,
                             person.card_number,
                             person.email))
        self.conn.commit()

    def insert_reader(self, reader: Reader) -> None:
        """
        Insert a reader into the database.
        """
        self.cursor.execute('''INSERT INTO readers
                            (reader_number, location_blueprint, location_hospital, location_name, abi_location)
                            VALUES (?, ?, ?, ?, ?)''',
                            (reader.reader_number,
                             reader.location_blueprint,
                             reader.location_hospital,
                             reader.location_name,
                             reader.abi_location))
        self.conn.commit()

    def insert_authorization(self, person: Person, reader: Reader) -> None:
        """
        Insert an authorization into the database.
        """
        self.cursor.execute('''INSERT INTO authorizations
                            (person_number, reader_number)
                            VALUES (?, ?)''',
                            (person.person_number,
                             reader.reader_number))
        self.conn.commit()

    def get_people(self) -> list:
        """
        Get all people from the database.
        """
        self.cursor.execute('''SELECT * FROM people''')
        people = self.cursor.fetchall()
        return people

    def get_readers(self) -> list:
        """
        Get all readers from the database.
        """
        self.cursor.execute('''SELECT * FROM readers''')
        readers = self.cursor.fetchall()
        return readers

    def get_authorizations(self) -> list:
        """
        Get all authorizations from the database.
        """
        self.cursor.execute('''SELECT * FROM authorizations''')
        authorizations = self.cursor.fetchall()
        return authorizations
    
    def select_person(self, person_number: str) -> tuple:
        """
        Select a person from the database.
        """
        self.cursor.execute('''SELECT * FROM people WHERE person_number = ?''', (person_number,))
        person = self.cursor.fetchone()
        return person

    def select_reader(self, reader_number: str) -> tuple:
        """
        Select a reader from the database.
        """
        self.cursor.execute('''SELECT * FROM readers WHERE reader_number = ?''', (reader_number,))
        reader = self.cursor.fetchone()
        return reader

    def close(self) -> None:
        """
        Close the database connection.
        """
        self.conn.close()
