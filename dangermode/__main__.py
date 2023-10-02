import os
from jupyter_console.app import ZMQTerminalIPythonApp, flags, aliases
from traitlets import Bool, Dict
from traitlets.config import catch_config_error, boolean_flag

# 需要用户交互的横幅
user_interaction_required_banner = """
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
🚨🚨 危险模式准备激活 🚨🚨
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨

这是一个预加载了dangermode库的Jupyter控制台实例。

要在本地机器上启动ChatGPT插件服务器🙈

激活危险模式：
activate_dangermode()
"""

# Docker环境中的横幅
docker_banner = """
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
🚨🚨 危险模式已为ChatGPT激活 🚨🚨
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨

服务器已上线，在8000端口运行。

通过ChatGPT进行配置：https://github.com/rgbkrk/dangermode#enabling-on-chatgpt

这是一个标准的IPython会话，ChatGPT也可以访问。
"""

# 更新标志
flags.update(
    boolean_flag(
        "totally-in-docker", "DangerModeIPython.totally_in_docker", "在Docker中立即激活危险模式"
    )
)

# 定义DangerModeIPython类
class DangerModeIPython(ZMQTerminalIPythonApp):
    flags = Dict(flags)  # 定义标志

    # 在Docker中是否立即激活危险模式
    totally_in_docker = Bool(
        False, config=True, help="在Docker中运行activate_dangermode(host='0.0.0.0')"
    )

    # 初始化横幅
    def init_banner(self):
        if self.totally_in_docker:
            self.shell.banner = docker_banner
            self.shell.show_banner()
            return

        self.shell.banner = user_interaction_required_banner
        self.shell.show_banner()

    # 初始化函数
    def initialize(self, argv=None):
        super().initialize(argv)
        self.shell.run_cell("from dangermode import activate_dangermode", store_history=False)

        if self.totally_in_docker:
            self.shell.run_cell("activate_dangermode(host='0.0.0.0')", store_history=False)

# 主函数
main = launch_new_instance = DangerModeIPython.launch_instance

# 程序入口
if __name__ == "__main__":
    main()
