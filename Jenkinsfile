pipeline {
    agent any
    stages {
        stage('Checkout') {
//             steps {
//                 // 检出项目代码
//                 git 'https://github.com/ychanglong/YCL.git'
//             }
//         }
        stage('Build') {
            steps {
                script {
                    // 使用 Docker Compose 构建和启动服务
                    sh 'docker-compose -f docker-compose.yml up -d --build'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // 部署步骤
                    sh 'docker-compose -f docker-compose.yml up -d'
                }
            }
        }
    }

    post {
        always {
            // 清理步骤
            script {
                sh 'docker-compose down'
            }
        }
    }
}