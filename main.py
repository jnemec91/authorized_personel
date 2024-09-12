from DataReaders import ReaderMapper, PersonMapper, AuthorizationMapper
from Database import Database
from Person import Person
from Reader import Reader


if __name__ == '__main__':
    reader_mapper = ReaderMapper('source_documents/export_readers.xlsx')
    readers = reader_mapper.get_readers()
    # print(readers)

    person_mapper = PersonMapper('source_documents/export_employees.xlsx')
    personel = person_mapper.get_people()
    # print(personel)

    authorization_mapper = AuthorizationMapper('source_documents/Export.xlsx', readers=readers, personel=personel)
    authorized_readers = authorization_mapper.get_authorizations()

    for reader in authorized_readers:
        print(reader.reader_number, reader.location_blueprint, reader.location_hospital, [str(i) for i in reader.authorized_personel])
        
    print(len(authorized_readers))

    db = Database('test.db')
    for person in personel:
        db.insert_person(person)
    for reader in readers:
        db.insert_reader(reader)
        for person in reader.authorized_personel:
            db.insert_authorization(person, reader)



    