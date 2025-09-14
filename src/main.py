import os
from pathlib import Path
from table_processing import TableProcessing
from bill_classifier_gemini import BillClassifier # 默认使用 Gemini，可切换为 DeepSeek

WORK_DIR = Path('../input')
TMP_DIR = Path('../tmp')
OUTPUT_DIR = Path('../output')

TMP_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# 根据导入的分类器选择 API Key
# 如果导入 bill_classifier_deepseek, 请使用 DEEPSEEK_API_KEY
API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")

processor = TableProcessing(working_directory=str(WORK_DIR), output_directory=str(TMP_DIR))
excel_files = [f for f in WORK_DIR.iterdir() if f.is_file() and f.suffix in ['.xlsx', '.ods']]

if not API_KEY:
    print("错误：环境变量 'GEMINI_API_KEY' 或 'DEEPSEEK_API_KEY' 未设置。")
else:
    for file_path in excel_files:
        # 1. 转换 ODS/XLSX 到 CSV 并存入 tmp 目录
        success = processor.convert_excel_to_csv(file_path.name)
        if success:
            # 2. 对 tmp 目录中的 CSV 文件进行预处理
            csv_filename = file_path.with_suffix('.csv').name
            processor.copy_csv_files()
            processor.clean_csv_files()
            processor.add_currency_column()
            processor.format_amount_by_type()

            # 3. 对预处理后的 CSV 文件进行分类
            print(f"开始对 {csv_filename} 进行分类...")
            classifier = BillClassifier(api_key=API_KEY)
            input_csv_path = TMP_DIR / csv_filename
            output_csv_path = OUTPUT_DIR / csv_filename
            classifier.process_bill(str(input_csv_path), str(output_csv_path))
            print(f"文件 {csv_filename} 处理完成，已保存到 {output_csv_path}")
