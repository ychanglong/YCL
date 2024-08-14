# Use an official Python runtime as a parent image
FROM python:3.9

# 设置代理（如果需要）
ENV HTTP_PROXY=http://10.187.215.117:3128
ENV HTTPS_PROXY=http://10.187.215.117:3128

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app/

#RUN mkdir -p /etc/pip.conf.d \
#    && echo "[global]" > /etc/pip.conf \
#    && echo "index-url = https://pypi.org/simple/" >> /etc/pip.conf \
#    && echo "[index]" >> /etc/pip.conf \
#    && echo "index = https://pypi.org/simple/" >> /etc/pip.conf \
#    && echo "proxy = http://10.187.215.117:3128" >> /etc/pip.conf

RUN #pip config list
# 创建 Docker Daemon 配置目录
RUN #mkdir -p /etc/docker/daemon.json.d

# 创建 daemon.json 文件，确保 JSON 格式正确
RUN #echo '{"http-proxy": "http://10.187.215.117:3128","https-proxy": "http://10.187.215.117:3128","dns": ["10.54.12.44", "10.187.50.203"]}' > /etc/docker/daemon.json


RUN #cat /etc/docker/daemon.json
RUN #cat /etc/resolv.conf

RUN #echo $(cat /etc/resolv.conf)

# 安装虚拟环境包
RUN #pip install virtualenv --proxy http://10.187.215.117:3128 -v

# 创建并激活虚拟环境
RUN #python3 -m virtualenv venv

# 使用 shell 执行命令以激活虚拟环境
RUN #. /app/venv/bin/activate

# 在虚拟环境中安装依赖
RUN #pip install django --proxy http://10.187.215.117:3128 -v

# 设置环境变量以使用虚拟环境中的 Python 和 pip
#ENV PATH="/app/venv/bin:$PATH"

EXPOSE 8111

# Collect static files (if needed)
# RUN python manage.py collectstatic --noinput

# Run the application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8111"]