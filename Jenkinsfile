pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_VERSION = '1.29.2'
    }

    stages {
        stage('Checkout') {
            steps {
                // 检出项目代码
                git 'https://github.com/ychanglong/YCL.git'
            }
        }
        stage('Build') {
            steps {
                script {
                    // 使用 Docker Compose 构建和启动服务
                    bat 'docker-compose -f docker-compose.yml up -d --build'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // 部署步骤
                    bat 'docker-compose -f docker-compose.yml up -d'
                }
            }
        }
    }
}