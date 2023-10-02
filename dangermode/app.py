import importlib.resources

from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastapi.responses import PlainTextResponse

from dangermode.routes import router
from dangermode.suggestions import RUN_CELL_PARSE_FAIL  # 从dangermode库中导入常量

# 创建一个FastAPI应用
# 设置服务器描述，以便在开发环境中ChatGPT不尝试使用HTTPS
app = FastAPI(servers=[{"url": "http://localhost:8000", "description": "本地服务器"}])

# 包含路由
app.include_router(router)

# 自定义的请求验证异常处理
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # 如果API路径是'/api/run_cell'
    if request.url.path == "/api/run_cell":
        # ChatGPT有时发送纯文本而非JSON。
        # 我们尝试提示ChatGPT应该发送符合我们首选架构的JSON。
        return PlainTextResponse(RUN_CELL_PARSE_FAIL, status_code=422)
    else:
        # 其他情况，调用FastAPI的默认请求验证异常处理
        return await request_validation_exception_handler(request, exc)

# 允许从软件包本身提供图像资源
static_directory = importlib.resources.files("dangermode") / "static"

# 挂载静态文件
app.mount("/static", StaticFiles(directory=str(static_directory)), name="static")

# 定义获取openapi.json的路由
# 在路由之外定义，以便我们可以调用app.openapi()
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    return app.openapi()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
