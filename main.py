from DataReaders import ReaderMapper, PersonMapper, AuthorizationMapper
from Database import Database
from Person import Person
from Reader import Reader
from ExportData import ExportData
from sqlite3 import IntegrityError


if __name__ == '__main__':
    reader_mapper = ReaderMapper('source_documents/export_readers.xlsx')
    readers = reader_mapper.get_readers()

    person_mapper = PersonMapper('source_documents/export_employees.xlsx')
    personel = person_mapper.get_people()

    authorization_mapper = AuthorizationMapper('source_documents/export_efas.xlsx', readers=readers, personel=personel)
    authorized_readers = authorization_mapper.get_authorizations()
        
    print(f'Found {len(authorized_readers)} readers...')

    db = Database('test.db')

    print('Building database...')
    progress = 0
    complete = len(readers)
    for reader in readers:
        progress += 1
        print(f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r")

        try:
            db.insert_reader(reader)
        except IntegrityError:
            # print(f'Reader already exists in database. {reader}')
            pass
        
        for person in reader.authorized_personel:
            try:
                db.insert_person(person)
            except IntegrityError:
                # print(f'Person already exists in database. {person}')
                pass

            db.insert_authorization(person, reader)
    
    print('Database built.\n')

    export = ExportData(db)
    export.export_authorizations()
    