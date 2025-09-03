import pandas as pd
from openai import OpenAI
from typing import List

class BillClassifier:
    """
    一个用于对账单交易进行分类的类
    """
    _TARGET_CATEGORIES: List[str] = [
        'DigitalOcean', '交通', '京东', '外卖', '淘宝',
        '话费', '超市', '食堂', '餐厅', '药店', '其它'
    ]

    def __init__(self, api_key: str):
        """
        初始化分类器。

        Args:
            api_key (str): 用于访问 DeepSeek API 的密钥

        Raises:
            ValueError: 如果未提供 API 密钥
            Exception: 如果 API 客户端初始化失败
        """
        base_url = "https://gemini.conraaad.com/openai/v1"
        model_name = "gemini-1.5-flash"

        if not base_url or not model_name:
            raise ValueError("错误：必须提供 base_url 和 model_name。")
        try:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
            self.model_name = model_name
        except Exception as e:
            raise Exception(f"初始化 API 客户端时出错: {e}")

    def _get_category_from_gemini(self, merchant: str, description: str) -> str:
        """
        调用 Gemini API 对交易进行分类。
        """
        prompt = f"""
        你是一个智能账单分类助手。
        请根据给出的'交易对方'和'商品说明'，将这笔交易分类到以下类别中的一个。
        你必须只返回类别名称，不要任何多余的解释、句子或标点符号。

        可用类别: {', '.join(self._TARGET_CATEGORIES)}

        特别说明:
        1. 外卖 vs 餐厅: 如果'交易对方'是美团、饿了么等外卖平台，且'商品说明'是某个餐厅的餐品，请分类为'外卖'。如果'交易对方'本身就是一个餐厅的名字(如'海底捞'、'肯得基')，请分类为'餐厅'。
        2. 其它: 如果交易无法明确归入以上任何一个类别，请分类为'其它'。

        ---
        交易对方: {merchant}
        商品说明: {description}
        ---

        分类结果:
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "你是一个智能账单分类助手，严格按照指令返回结果。"},
                    {"role": "user", "content": prompt},
                ],
                stream=False,
                max_tokens=20,
                temperature=0,
            )
            category = response.choices[0].message.content.strip()

            return category if category in self._TARGET_CATEGORIES else '其它'
        except Exception:
            return '其它'
    # --- MODIFIED END ---

    def _classify_transaction(self, row: pd.Series) -> str:
        """
        对单笔交易进行分类的核心函数。
        """
        merchant = str(row['交易对方'])
        description = str(row['商品说明'])

        # 规则 0：处理信息极度模糊的交易
        generic_descriptions = ['二维码支付', '移动支付', '扫码产品', '收钱码收款', '经营码交易']
        if description in generic_descriptions and (merchant == '/' or merchant == ''):
            return '其它'

        # 规则 1：食堂判断
        if any(keyword in description or keyword in merchant for keyword in ['甘饴园', '汀香园']):
            return '食堂'

        # 规则 2：外卖平台判断
        delivery_platforms = ['饿了么', '美团', '淘宝闪购']
        if any(platform in merchant or platform in description for platform in delivery_platforms):
            pharmacy_keywords = ['药', '药店', '买药', '益丰', '大参林', '海王', '老百姓', '同仁堂', '大药房', '药房']
            if any(keyword in description for keyword in pharmacy_keywords):
                return '药店'

            supermarket_keywords = ['超市', '便利店', '便利蜂', '7-ELEVEN', '罗森', '全家', '美佳宜', '新佳宜', '水果',
                                    '绿叶水果']
            if any(keyword in description for keyword in supermarket_keywords):
                return '超市'

            return '外卖'

        # 规则 3：交通出行判断
        traffic_keywords = ['滴滴', '高德', '打车', '火车票', '12306', '地铁', '公交', '航班', '机票', '轨道交通']
        if any(keyword in description or keyword in merchant for keyword in traffic_keywords):
            return '交通'

        # 规则 4：其他明确的规则
        if '京东' in merchant:
            return '京东'
        if '淘宝' in merchant or '天猫' in merchant:
            return '淘宝'

        supermarket_merchants = ['超市', '便利店', '零食很忙', '步步高', 'KK-Store', "KKV", '美宜佳', '新佳宜',
                                 '绿叶水果', '7-ELEVEN', '罗森', '全家']
        if any(keyword in merchant for keyword in supermarket_merchants):
            return '超市'

        return self._get_category_from_gemini(merchant, description)

    def process_bill(self, input_path: str, output_path: str):
        """
        读取、处理并保存账单文件

        Args:
            input_path (str): 输入的 CSV 文件路径
            output_path (str): 输出的 CSV 文件路径

        Raises:
            FileNotFoundError: 如果输入文件不存在
            ValueError: 如果输入文件缺少必要的列
            Exception: 如果在读写文件过程中发生其他错误
        """
        try:
            df = pd.read_csv(input_path, encoding='utf-8-sig')
        except FileNotFoundError:
            raise FileNotFoundError(f"错误：找不到输入文件 '{input_path}'")
        except Exception as e:
            raise Exception(f"读取文件 '{input_path}' 时出错: {e}")

        required_columns = ['交易对方', '商品说明']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"错误：输入文件缺少必要的列。需要包含: {', '.join(required_columns)}")

        df['交易对方'] = df.apply(self._classify_transaction, axis=1)

        try:
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"处理完成！结果已保存到 '{output_path}'")
        except Exception as e:
            raise Exception(f"保存文件到 '{output_path}' 时出错: {e}")
