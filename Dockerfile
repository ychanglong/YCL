ARG DNS_SERVERS
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

# 安装虚拟环境包
RUN mkdir -p /etc/docker/daemon.json.d && echo '{"dns": ["'"${DNS_SERVERS}"'"]}' > /etc/docker/daemon.json

RUN cat /etc/resolv.conf

RUN echo $(cat /etc/resolv.conf)

RUN pip install virtualenv

# 创建并激活虚拟环境
RUN python3 -m virtualenv venv

# 使用 shell 执行命令以激活虚拟环境
RUN . /app/venv/bin/activate

# 在虚拟环境中安装依赖
RUN pip install django

# 设置环境变量以使用虚拟环境中的 Python 和 pip
ENV PATH="/app/venv/bin:$PATH"

EXPOSE 8111

# Collect static files (if needed)
# RUN python manage.py collectstatic --noinput

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8111"]