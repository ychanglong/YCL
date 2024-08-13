# Use an official Python runtime as a parent image
FROM python:3.9
#ENV HTTP_PROXY=http://10.187.215.117:3128
#ENV HTTPS_PROXY=http://10.187.215.117:3128


# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app/

#RUN mkdir -p /etc/pip.conf.d \
#    && echo "[global]" > /etc/pip.conf \
#    && echo "index-url = https://anu9rng:AP6eY5xuhS1MqAdy5jedftw3ndQq7MHjXL8Rpb@rb-artifactory.bosch.com/artifactory/api/pypi/python-virtual/simple" >> /etc/pip.conf \
#    && echo "[index]" >> /etc/pip.conf \
#    && echo "index = https://anu9rng:AP6eY5xuhS1MqAdy5jedftw3ndQq7MHjXL8Rpb@rb-artifactory.bosch.com/artifactory/api/pypi/python-virtual/" >> /etc/pip.conf
#
## 安装虚拟环境包
#RUN pip install --upgrade pip
RUN #pip install virtualenv

# 创建并激活虚拟环境
RUN #python -m virtualenv venv

# 使用 shell 执行命令以激活虚拟环境
RUN . /etc/docker/venv/bin/activate

# 在虚拟环境中安装依赖
RUN pip install django

# 设置环境变量以使用虚拟环境中的 Python 和 pip
ENV PATH="/app/venv/bin:$PATH"

EXPOSE 8111

# Collect static files (if needed)
# RUN python manage.py collectstatic --noinput

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8111"]