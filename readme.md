# Readers Extract

This project processes and manages data about readers, personnel, and their authorizations from Excel files, storing the results in a SQLite database and exporting processed data to Excel.

## Features

- Reads and maps data from Excel files about readers and personnel.
- Maps authorizations between personnel and readers.
- Stores all data in a local SQLite database.
- Exports authorizations, readers, and department data to Excel files.

## Requirements

- Python 3.11+
- [openpyxl](https://pypi.org/project/openpyxl/)
- [Unidecode](https://pypi.org/project/Unidecode/)

Install dependencies with:

```sh
pip install -r requirements.txt
```

## Input files format

1. export_readers.xlsx
    List of all readers
    - columns must have no names on first line
    - order of columns: 
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`budova`|`cislo ctecky`|`cislo mistnosti`|`nazev mistnosti`

2. export_readers_app.xlsx
    List of readers exported from bvmain django app
    - columns must have no names on first line
    - order of columns:
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`id`|`reader_number`|`reader_location`|`reader_type`|`reader_abi_location`

3. export_employees.xlsx
    Export from employee database
    - columns must not have no names on first line
    - order of columns:
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`icp`|`email`|`jmeno`|`prijmeni`|`titul`|`cislokarty`

4. export_efas.xlsx
    Export from database of rooms
    - columns can contain names in first row
    - order of columns:
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Kod mistnosti`|`Nazev standard`|`Doplnek nazvu`|`Kod projekt`|`Vrchni sestra\Ved.odb`|`Stanicni sestra/Ved.odb`|`Najemce`
        

## Usage

1. Place your source Excel files in the `source_documents/` directory:
    - `export_readers.xlsx`
    - `export_readers_app.xlsx`
    - `export_employees.xlsx`
    - `export_efas.xlsx`

2. Run the main script:

```sh
python main.py
```

3. The script will:
    - Read and process the data.
    - Build or update the SQLite database (`database.db`).
    - Export results to the `output_documents/` directory:
        - `AuthorizationsOutput.xlsx`
        - `ReadersOutput.xlsx`
        - `DepartmentsOutput.xlsx`

4. You can also just export data when database is already built:

```sh
python ExportData.py
```

## Output

- All processed data will be available in the `output_documents/` folder.
- The database file will be created or updated in the project root.

## Notes

- Make sure the source Excel files are formatted as expected.
- The script prints progress information to the console.

## Project Structure

- `main.py` — Entry point for running the data processing pipeline.
- `Database.py` — Handles SQLite database operations.
- `DataReaders.py` — Reads and maps data from Excel files.
- `ExportData.py` — Exports processed data to Excel.
- `Person.py`, `Reader.py` — Data models.
- `Formater.py` — Utility for formatting strings.
- `requirements.txt` — Python dependencies.
