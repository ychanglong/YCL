pipeline {
    agent any

    environment {
        PATH = "/usr/venv/bin:$PATH"
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from Git
                git 'https://github.com/ychanglong/YCL.git'
            }
        }
        stage('Install dependencies') {
            steps {
                // Install Python dependencies
                sh 'echo 123456 | sudo -S python3 -m venv /usr/venv'
                sh '. /usr/venv/bin/activate'
                sh 'python3 manage.py test'
                sh 'nohup python3 manage.py runserver 0.0.0.0:8000 &'
            }
        }

    }
}
