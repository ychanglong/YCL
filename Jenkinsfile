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
                }
            }
        }
    }
}