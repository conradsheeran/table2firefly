# table2firefly

本项目旨在将支付宝和微信支付的账单流水文件转换为 [Firefly III](https://www.firefly-iii.org/) 支持的 CSV 导入格式。它利用 AI 模型（如 Gemini 和 DeepSeek）自动对交易进行分类，简化记账流程。

## 功能

*   支持处理支付宝和微信支付的 `.ods`、`.xlsx`、`.csv` 格式账单文件
*   自动将账单文件转换为 `.csv` 格式以便处理
*   使用大语言模型智能识别和分类交易对方及交易类别
*   生成可直接导入 Firefly III 的标准 CSV 文件

## 目录结构

```
table2firefly/
├── input/                  # 存放原始的支付宝/微信支付账单文件 (.ods)
├── output/                 # 存放处理完成、可用于 Firefly III 导入的 CSV 文件
├── src/                    # 项目源代码
│   ├── main.py             # 项目主入口文件
│   ├── table_processing.py # 负责账单文件的读取和预处理
│   ├── bill_classifier_deepseek.py # 使用 DeepSeek 模型进行分类
│   └── bill_classifier_gemini.py   # 使用 Gemini 模型进行分类
├── tmp/                    # 存放中间过程生成的临时文件
├── environment.yml         # Conda 环境配置文件
└── README.md               # 本文档
```

## 安装

1.  克隆本项目到本地：
    ```bash
    git clone https://github.com/conradsheeran/table2firefly.git
    cd table2firefly
    ```
2.  确保您已安装 [Conda](https://docs.conda.io/en/latest/miniconda.html)
3.  使用 `environment.yml` 文件创建并激活 Conda 环境：
    ```bash
    conda env create -f environment.yml
    conda activate table2firefly
    ```
4.  **配置 API 密钥**：本项目需要使用 AI 模型进行交易分类。请通过设置环境变量来配置您的 API 密钥

    *   **对于 Gemini 模型 (默认)**:
        ```bash
        export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        ```
    *   **对于 DeepSeek 模型**:
        ```bash
        export DEEPSEEK_API_KEY="YOUR_DEEPSEEK_API_KEY"
        ```
    > **提示**: 您可以将 `export` 命令添加到您的 shell 配置文件中（如 `.bashrc`, `.zshrc`），这样就无需在每次打开新终端时都重新设置

## 使用方法

1.  将从支付宝或微信支付下载的原始账单文件（`.ods` 格式）放入 `input/` 目录。

2.  **选择 AI 模型 (可选)**：
    *   项目默认使用 **Gemini** 模型。
    *   如果您想切换到 **DeepSeek** 模型，请编辑 `src/main.py` 文件，将导入语句从：
        ```python
        from bill_classifier_gemini import BillClassifier
        ```
        修改为：
        ```python
        from bill_classifier_deepseek import BillClassifier
        ```
        并确保您已在第 4 步安装中设置了 `DEEPSEEK_API_KEY` 环境变量。

3.  运行主程序：
    ```bash
    python src/main.py
    ```
    脚本会自动完成以下操作：
    *   转换 `input/` 目录中的 `.ods` 文件为 CSV 格式。
    *   对 CSV 文件进行预处理和格式化。
    *   调用您选择的 AI 模型对每一笔交易进行分类。
    *   将最终结果保存到 `output/` 目录。

4.  处理完成后，生成的适用于 Firefly III 的 CSV 文件将保存在 `output/` 目录中。文件名与原始输入文件相同。

5.  登录您的 Firefly III Importer，进入 **导入/导出 -> 导入文件**，上传 `output/` 目录中生成的 CSV 文件即可。
