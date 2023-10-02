"""用于帮助ChatGPT解决问题的建议"""

# 定义一个字符串常量RUN_CELL_PARSE_FAIL，用于提示期望的JSON格式。
# 该字符串用于在'/api/run_cell'端点收到不符合预期的JSON格式时，给出提示。
RUN_CELL_PARSE_FAIL = """
运行代码单元的端点期望的JSON格式类似于 `{ "code": "import pandas as pd\\nprint('hello world')" }`。
""".strip()
