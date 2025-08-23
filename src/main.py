import os
from pathlib import Path
from table_processing import TableProcessing
from bill_classifier import BillClassifier

WORK_DIR = '../input'
TMP_DIR = '../tmp'
OUTPUT_DIR = '../output'
DEEPSEEK_API_KEY = os.environ['DEEPSEEK_API_KEY']

processor = TableProcessing(working_directory=WORK_DIR, output_directory=TMP_DIR)
excel_files = [f for f in Path(WORK_DIR).iterdir() if f.is_file() and f.suffix in ['.xlsx']]

for file_path in excel_files:
    success = processor.convert_excel_to_csv(file_path.name)
    if success:
        processor.copy_csv_files()
        processor.clean_csv_files()
        processor.add_currency_column()

csv_files = [f for f in Path(TMP_DIR).iterdir() if f.is_file() and f.suffix == '.csv']

for file_path in csv_files:
    classifier = BillClassifier(api_key=DEEPSEEK_API_KEY)
    output_file_path = Path(OUTPUT_DIR).joinpath(file_path.name)
    classifier.process_bill(str(file_path), str(output_file_path))