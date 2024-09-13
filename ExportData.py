from Database import Database
import openpyxl as opx

class ExportData:
    def __init__(self, db) -> None:
        if not isinstance(db, Database):
            self.db = Database(db)
        else:
            self.db = db


    def export_authorizations(self):
        export = opx.Workbook()
        sheet = export.active

        print('Exporting authorizations...')
        sheet.append(['Person Number', 'First Name', 'Last Name', 'Card Number', 'Email', 'Reader Number', 'Location Blueprint', 'Location Hospital', 'Location Name'])

        authorizations = self.db.get_authorizations()
        readers = self.db.get_readers()
        readers_with_authorizations = set([authorizations[1] for authorizations in authorizations])
        print('Readers_with_authorizations:', len(readers_with_authorizations))
        progress = 0
        complete = len(authorizations)
        for authorization in authorizations:
            progress += 1
            print(f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r")
            reader = self.db.select_reader(authorization[1])
            person = self.db.select_person(authorization[0])

            row = [person[0], person[1], person[2], person[3], person[4], reader[0], reader[1], reader[2], reader[3]]
            sheet.append(row)
        
        print('Checking for missing authorizations...')
        progress = 0
        complete = len(readers)
        count = 0
        for reader in readers:
            progress += 1
            print(f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r")
            if reader[0] not in readers_with_authorizations:
                row = [None, None, None, None, None, reader[0], reader[1], reader[2], reader[3]]
                sheet.append(row)
                count += 1
        
        print(f'Found {count} missing authorizations.')
        export.save('source_documents/Output.xlsx')
        print('Export complete.')
        print('Output saved to source_documents/Output.xlsx')
    

if __name__ == '__main__':
    db = Database('test.db')
    export = ExportData(db)
    export.export_authorizations()