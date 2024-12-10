pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/ychanglong/bosch.git'
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
                    sh 'echo "123456" | sudo -S docker-compose -f docker-compose.yml up -d'
                }
            }
        }
    }
}