from typing import Union
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response
from IPython import get_ipython
from IPython.utils.capture import capture_output

# 导入自定义模型和其他工具
from dangermode.models import (
    DisplayData,
    ErrorData,
    RunCellRequest,
    RunCellResponse,
    image_store,
)
from dangermode.suggestions import RUN_CELL_PARSE_FAIL  # 从dangermode库中导入常量

# 创建一个API路由器
router = APIRouter()

# 处理AI插件JSON信息的路由
@router.get("/.well-known/ai-plugin.json", include_in_schema=False)
async def get_ai_plugin_json():
    return {
        # 插件的各种元数据和信息
        "schema_version": "v1",
        "name_for_human": "Notebook Session",
        "name_for_model": "notebook_session",
        "description_for_human": "允许ChatGPT在你正在运行的IPython内核和Jupyter Notebook中操作数据。",
        "description_for_model": "IPython/Jupyter Notebook的插件。你可以检查变量并运行代码。",
        "auth": {"type": "none"},  # 无需认证 😂😭
        "api": {
            "type": "openapi",
            "url": "http://localhost:8000/openapi.json",
            "is_user_authenticated": False,
        },
        "logo_url": "http://localhost:8000/static/images/logo.png",
        "contact_email": "rgbkrk@gmail.com",
        "legal_info_url": "https://github.com/rgbkrk/honchkrow/issues",
    }

# 获取图片的路由
@router.get("/images/{image_name}", include_in_schema=False)
async def get_image(image_name: str) -> Response:
    try:
        image_bytes = image_store.get_image(image_name)
        return Response(image_bytes, media_type="image/png")
    except KeyError as ke:
        raise HTTPException(status_code=404, detail="图片未找到")

# 获取变量的路由
@router.get("/api/variable/{variable_name}")
async def get_variable(variable_name: str) -> Union[DisplayData, ErrorData]:
    '''获取存在的变量'''
    try:
        ip = get_ipython()
        value = ip.user_ns[variable_name]
        return DisplayData.from_tuple(ip.display_formatter.format(value))
    except KeyError as ke:
        raise HTTPException(status_code=404, detail=f"变量 {variable_name} 未定义")

# 执行代码单元的路由
@router.post("/api/run_cell")
async def execute(request: RunCellRequest) -> RunCellResponse:
    '''执行一个代码单元并返回结果
    执行格式是
    ```json
    {
        "code": "print('hello world')"
    }
    ```
    '''
    code = request.code
    if code is None or code == "":
        raise HTTPException(
            status_code=400,
            detail=RUN_CELL_PARSE_FAIL,
        )
    try:
        with capture_output() as captured:
            ip = get_ipython()
            result = ip.run_cell(code)
        if result.success:
            return RunCellResponse.from_result(result.result, captured.stdout, captured.stderr, captured.outputs)
        else:
            return RunCellResponse.from_error(result.error_in_exec)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行代码时出错: {e}")
