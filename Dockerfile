# 使用官方的Python基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /usr/src/app

# 复制项目依赖文件
COPY requirements.txt ./

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露Django运行的端口
EXPOSE 8000

# 运行Django开发服务器
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]