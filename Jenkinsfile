pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/ychanglong/YCL.git'
            }
        }
        stage('Build') {
            steps {
                script {
                    sh 'echo "123456" | sudo -S docker-compose -f docker-compose.yml up -d --build'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    // 启动 Docker 容器
                    sh 'echo "123456" | sudo -S docker-compose -f docker-compose.yml up -d'

                    // 等待 MySQL 启动，确保数据库准备好接受连接
                    sleep(10)  // 根据 MySQL 启动时间调整秒数

                    // 运行 Django 数据库迁移
                    sh 'echo "123456" | sudo -S docker-compose exec web python manage.py makemigrations'
                    sh 'echo "123456" | sudo -S docker-compose exec web python manage.py migrate'
                }
            }
        }
    }
}