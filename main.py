from DataReaders import ReaderMapper, PersonMapper, AuthorizationMapper, ABILocationMapper, VelinMapper
from Database import Database
from ExportData import ExportData
from sqlite3 import IntegrityError


if __name__ == '__main__':
    reader_mapper = ReaderMapper('source_documents/export_readers.xlsx')
    readers = reader_mapper.get_readers()

    abi_location_mapper = ABILocationMapper('source_documents/export_readers_app.xlsx', readers=readers)
    readers = abi_location_mapper.get_readers()

    velin_reader_mapper = VelinMapper('source_documents/export_readers_app.xlsx', readers=readers)
    readers = velin_reader_mapper.get_readers()

    person_mapper = PersonMapper('source_documents/export_employees.xlsx')
    personel = person_mapper.get_people()

    authorization_mapper = AuthorizationMapper('source_documents/export_efas.xlsx', readers=readers, personel=personel)
    authorized_readers = authorization_mapper.get_authorizations()

        
    print(f'Found {len(authorized_readers)} readers...')

    db = Database('database.db')

    print('Building database...')
    progress = 0
    complete = len(readers)
    for reader in readers:
        progress += 1
        print(f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r")

        try:
            db.insert_reader(reader)
        except IntegrityError:
            #TODO: Add routine to update reader information
            # print(f'Reader already exists in database. {reader}')
            pass
        
        for person in reader.authorized_personel:
            try:
                db.insert_person(person)
            except IntegrityError:
                # TODO: Add routine to update person information
                # print(f'Person already exists in database. {person}')
                pass

            db.insert_authorization(person, reader)
    
    print('Database built.\n')

    export = ExportData(db)
    export.export_authorizations()
    export.export_readers()
    