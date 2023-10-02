import base64
from typing import Dict, List, Optional, Tuple

from IPython import get_ipython
from pydantic import BaseModel

# 定义一个用于运行笔记本中单元格的请求模型
class RunCellRequest(BaseModel):
    '''运行notebook中的单元格的请求'''
    code: str  # 要执行的代码

# 定义展示数据的模型
class DisplayData(BaseModel):
    '''display_data和execute_result消息使用这种格式。'''
    data: Optional[dict] = None  # 数据部分
    metadata: Optional[dict] = None  # 元数据部分

    # 类方法，用于从元组创建DisplayData实例
    @classmethod
    def from_tuple(cls, formatted: Tuple[dict, dict]):
        return cls(data=formatted[0], metadata=formatted[1])

# 定义图像数据的模型
class ImageData(BaseModel):
    '''公共URL的图像数据'''
    data: bytes  # 图像的字节数据
    url: str  # 图像的URL

# 定义用于存储图像的内存仓库的模型
class ImageStore(BaseModel):
    '''一个用于存储在notebook中显示的图像的内存仓库'''
    image_store: Dict[str, ImageData] = {}  # 图像存储字典

    # 存储所有图像数据并转换为前端可以获取的URL
    def store_images(self, dd: DisplayData) -> DisplayData:
        if dd.data and "image/png" in dd.data:
            image_name = f"image-{len(self.image_store)}.png"
            image_data = base64.b64decode(dd.data["image/png"])
            self.image_store[image_name] = ImageData(data=image_data, url=f"http://localhost:8000/images/{image_name}")
            dd.data["image/png"] = self.image_store[image_name].url
        return dd

    # 获取指定名称的图像数据
    def get_image(self, image_name: str) -> bytes:
        return self.image_store[image_name].data

    # 清除图像存储
    def clear(self):
        self.image_store = {}

# 初始化一个全局的图像存储实例
image_store = ImageStore()

# 定义错误数据的模型
class ErrorData(BaseModel):
    error: str  # 错误信息

    # 类方法，用于从异常创建ErrorData实例
    @classmethod
    def from_exception(cls, e: Exception):
        return cls(error=str(e) if str(e) else type(e).__name__)

# 定义运行单元格的响应模型
class RunCellResponse(BaseModel):
    '''输出、标准输出、标准错误以及成功或失败的状态信息的集合'''
    success: bool = False  # 是否成功
    execute_result: Optional[DisplayData] = None  # 执行结果
    error: Optional[str] = ""  # 错误信息
    stdout: Optional[str] = ""  # 标准输出
    stderr: Optional[str] = ""  # 标准错误
    displays: List[DisplayData] = []  # 展示的数据列表

    # 类方法，用于从结果、标准输出和标准错误创建RunCellResponse实例
    @classmethod
    def from_result(cls, result, stdout, stderr, displays):
        ip = get_ipython()
        execute_result = DisplayData.from_tuple(ip.display_formatter.format(result))
        displays = [DisplayData(data=d.data, metadata=d.metadata) for d in displays]

        # 将所有图像数据转换为前端可以获取的URL
        displays = [image_store.store_images(d) for d in displays]
        execute_result = image_store.store_images(execute_result)

        return cls(
            success=True,
            execute_result=execute_result,
            stdout=stdout,
            stderr=stderr,
            displays=displays,
        )

    # 类方法，用于从错误创建RunCellResponse实例
    @classmethod
    def from_error(cls, error):
        return cls(
            success=False,
            result=None,
            error=f"执行代码出错：{error}",
        )
