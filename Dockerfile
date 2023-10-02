# 使用基础镜像
FROM jupyter/scipy-notebook

# 安装常用命令
USER root
RUN apt update && apt install -y  telnet wget

# 设置环境变量
ENV GRANT_SUDO=yes

# 切换回 jovyan 用户
USER jovyan

# 安装所需的 Python 包
RUN pip install ipython fastapi jupyter-console uvicorn -i https://mirrors.aliyun.com/pypi/simple/

# 设置工作目录
WORKDIR /usr/src

# 复制项目文件
COPY poetry.lock pyproject.toml README.md ./
COPY dangermode ./dangermode
COPY fonts /usr/share/fonts/truetype/
RUN fc-cache -fv
RUN rm /home/jovyan/.cache/matplotlib -rf

# 安装项目依赖
RUN pip install  -i https://mirrors.aliyun.com/pypi/simple/ -e .

# 切换回用户的主目录
WORKDIR /home/jovyan

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "-m", "dangermode", "--totally-in-docker"]