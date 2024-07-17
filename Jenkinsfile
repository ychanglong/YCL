pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    // 使用 Docker 构建镜像
                    docker.build('OA-project')
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    // 使用 docker-compose 部署
                    sh 'docker-compose down'
                    sh 'docker-compose up -d'
                }
            }
        }
    }
}
