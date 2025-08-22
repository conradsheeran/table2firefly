from pathlib import Path
from table_processing import TableProcessing

WORK_DIR = '../input'
OUTPUT_DIR = '../tmp'

processor = TableProcessing(working_directory=WORK_DIR, output_directory=OUTPUT_DIR)
excel_files = [f for f in Path(WORK_DIR).iterdir() if f.is_file() and f.suffix in ['.xlsx']]

for file_path in excel_files:
    success = processor.convert_excel_to_csv(file_path.name)
    if success:
        processor.copy_csv_files()
        processor.clean_csv_files()
        processor.add_currency_column()