import shutil

import pandas as pd
from pathlib import Path
from typing import List, Optional

class TableProcessing:
    """
    一个用于处理表格文件的工具类，包括从Excel到CSV的转换和CSV文件的清理。
    """

    def __init__(self, working_directory: str, output_directory: str):
        """
        初始化处理器。

        Args:
            working_directory (str): 包含源文件的工作目录。
            output_directory (str): 用于存放处理后文件的输出目录。
        """
        self.work_dir = Path(working_directory).resolve()
        self.output_dir = Path(output_directory).resolve()

        if not self.work_dir.is_dir():
            raise FileNotFoundError(f"指定的目录不存在: {self.work_dir}")

        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def convert_excel_to_csv(self, filename: str) -> bool:
        """
        将单个Excel文件转换为CSV格式，并进行表头重命名和数据清理。

        Args:
            filename (str): 要转换的Excel文件名（包含扩展名）。

        Returns:
            bool: 如果转换成功则返回 True，否则返回 False。
        """
        excel_file_path = self.work_dir / filename
        if not excel_file_path.is_file():
            print(f"错误: '{filename}' 未找到。")
            return False

        try:
            df = pd.read_excel(excel_file_path)

            header_mapping = {
                '交易时间': '交易时间', '交易类型': '交易分类', '交易对方': '交易对方',
                '商品': '商品说明', '收/支': '收/支', '金额(元)': '金额',
                '支付方式': '收/付款方式', '当前状态': '交易状态', '交易单号': '交易订单号',
                '商户单号': '商家订单号', '备注': '备注'
            }
            target_headers_order = [
                '交易时间', '交易分类', '交易对方', '商品说明', '收/支',
                '金额', '收/付款方式', '交易状态', '交易订单号', '商家订单号', '备注'
            ]

            if '金额(元)' in df.columns:
                df['金额(元)'] = df['金额(元)'].astype(str).str.replace('¥', '', regex=False).str.strip()

            df.rename(columns=header_mapping, inplace=True)

            final_df = pd.DataFrame()
            for col in target_headers_order:
                final_df[col] = df.get(col, pd.Series(dtype='object'))

            output_filepath = self.output_dir / f"{excel_file_path.stem}.csv"
            final_df.to_csv(output_filepath, index=False, encoding='utf-8-sig')
            return True
        except Exception as e:
            print(f"处理 '{filename}' 文件时发生错误: {e}")
            return False

    def copy_csv_files(self):
        """
        复制 CSV 到输出目录
        """
        csv_files = list(self.work_dir.glob('*.csv'))
        if not csv_files:
            return

        for path in csv_files:
            try:
                destination_path = self.output_dir / path.name
                shutil.copy2(path, destination_path)
            except Exception as e:
                print(f"复制 '{path.name}' 时失败: {e}")

    def clean_csv_files(self, specific_columns_to_drop: Optional[List[str]] = None):
        """
        清理 CSV 文件

        Args:
            specific_columns_to_drop (Optional[List[str]]):
                一个可选的字符串列表，指定除了默认列之外还需删除的列名
        """
        if specific_columns_to_drop is None:
            columns_to_drop = ['备注', '对方帐号']
        else:
            columns_to_drop = ['备注', '对方帐号'] + specific_columns_to_drop

        csv_files = list(self.output_dir.glob('*.csv'))

        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file, encoding='utf-8-sig', dtype=str).fillna('')
                original_columns_count = len(df.columns)
                actual_cols_to_drop = [col for col in columns_to_drop if col in df.columns]
                df.drop(columns=actual_cols_to_drop, inplace=True)
                df.dropna(axis=1, how='all', inplace=True)

                if len(df.columns) < original_columns_count:
                    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            except Exception as e:
                print(f"清理 '{csv_file.name}' 文件时发生错误: {e}")

    def add_currency_column(self, column_name: str = '币种', value: str = 'CNY', position: int = 5):
        """
        为输出目录中的所有 CSV 文件添加一个新列

        Args:
            column_name (str): 要添加的列的名称。默认为 '币种'
            value (str): 要为该列填充的默认值。默认为 'CNY'
            position (int): 新列的目标位置。默认为 5
        """
        csv_files = list(self.output_dir.glob('*.csv'))
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file, encoding='utf-8-sig', dtype=str)

                target_pos = max(0, position)
                target_pos = min(target_pos, len(df.columns))

                if column_name in df.columns:
                    current_pos = df.columns.get_loc(column_name)
                    if current_pos != target_pos:
                        col_series = df[column_name].copy()
                        df.drop(columns=[column_name], inplace=True)
                        adjusted_target_pos = min(target_pos, len(df.columns))
                        df.insert(loc=adjusted_target_pos, column=column_name, value=col_series)
                    else:
                        pass
                else:
                    if df.shape[0] > 0:
                        df.insert(loc=target_pos, column=column_name, value=value)
                    else:
                        cols = df.columns.tolist()
                        cols.insert(target_pos, column_name)
                        df = pd.DataFrame(columns=cols)

                df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            except Exception as e:
                print(f"'{csv_file.name}' 添加列时发生错误: {e}")

