pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    docker.build('my-django-app')
                }
            }
        }


        stage('Deploy') {
            steps {
                script {
                    docker.image('my-django-app').run('-p 8000:8000 --name django-app-container')
                }
            }
        }
    }
}