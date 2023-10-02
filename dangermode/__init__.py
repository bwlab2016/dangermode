"""Dangermode 主包"""

# 作者和邮件信息
__author__ = """黑白"""
__email__ = "seth@9ishell.com"
__version__ = "1.0.0"  # 当前版本号

# 激活危险模式插件的函数
def activate_dangermode(host="127.0.0.1"):
    """
    激活ChatGPT的危险模式插件。🚨

    主要用于Jupyter控制台或IPython内核，比如在Jupyter Notebook或JupyterLab中。
    """
    # 导入所需库
    import asyncio
    import atexit
    import uvicorn

    from dangermode.app import app  # 从dangermode包导入app

    # 设置服务器配置
    config = uvicorn.Config(app, host=host)
    # 创建服务器实例
    server = uvicorn.Server(config)

    # 获取当前事件循环
    loop = asyncio.get_event_loop()
    # 在事件循环中创建一个新任务来启动服务器
    loop.create_task(server.serve())

    # 当程序退出时，注册一个关闭服务器的函数
    atexit.register(lambda: asyncio.run(server.shutdown()))

    # 返回服务器实例
    return server

# 设置包的__all__变量，声明模块公开的接口
__all__ = ["activate_dangermode"]
