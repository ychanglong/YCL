pipeline {
    agent any

    environment {
        http_proxy = 'http://10.187.215.117:3128'
        https_proxy = 'http://10.187.215.117:3128'
        no_proxy = 'localhost,127.0.0.1,.bosch.com'
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
                    sh 'echo "123456" | sudo docker-compose -f docker-compose.yml up -d --build'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // 部署步骤
                    sh 'echo "123456" | sudo docker-compose -f docker-compose.yml up -d'
                }
            }
        }
    }
}