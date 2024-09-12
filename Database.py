# create database sqlite3

import sqlite3
from Person import Person
from Reader import Reader


class Database:
    def __init__(self, db_name) -> None:
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS people
                            (person_number INTEGER PRIMARY KEY,
                            first_name TEXT,
                            last_name TEXT,
                            card_number TEXT,
                            email TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS readers
                            (reader_number INTEGER PRIMARY KEY,
                            location_blueprint TEXT,
                            location_hospital TEXT,
                            location_name TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS authorizations
                            (person_number INTEGER,
                            reader_number INTEGER,
                            FOREIGN KEY(person_number) REFERENCES people(person_number),
                            FOREIGN KEY(reader_number) REFERENCES readers(reader_number))''')

    def insert_person(self, person: Person):
        self.cursor.execute('''INSERT INTO people
                            (person_number, first_name, last_name, card_number, email)
                            VALUES (?, ?, ?, ?, ?)''',
                            (person.person_number, person.first_name, person.last_name, person.card_number, person.email))
        self.conn.commit()

    def insert_reader(self, reader: Reader):
        self.cursor.execute('''INSERT INTO readers
                            (reader_number, location_blueprint, location_hospital, location_name)
                            VALUES (?, ?, ?, ?)''',
                            (reader.reader_number, reader.location_blueprint, reader.location_hospital, reader.location_name))
        self.conn.commit()

    def insert_authorization(self, person: Person, reader: Reader):
        self.cursor.execute('''INSERT INTO authorizations
                            (person_number, reader_number)
                            VALUES (?, ?)''',
                            (person.person_number, reader.reader_number))
        self.conn.commit()

    def get_people(self):
        self.cursor.execute('''SELECT * FROM people''')
        people = self.cursor.fetchall()
        return people

    def get_readers(self):
        self.cursor.execute('''SELECT * FROM readers''')
        readers = self.cursor.fetchall()
        return readers

    def get_authorizations(self):
        self.cursor.execute('''SELECT * FROM authorizations''')
        authorizations = self.cursor.fetchall()
        return authorizations

    def close(self):
        self.conn.close()
