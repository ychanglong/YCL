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

//          stage('Install pip') {
//             steps {
//                 sh 'sudo apt-get update && sudo apt-get install -y python3-pip'
//             }
//         }
        stage('Install dependencies') {
            steps {
                // Install Python dependencies
                sh 'echo 123456 | sudo -S python3 -m venv /usr/venv'
                sh '. /usr/venv/bin/activate'
                sh 'python3 manage.py test'
                sh 'nohup python3 manage.py runserver 0.0.0.0:8000 &'
            }
        }

        stage('Check nohup.out') {
            steps {
                sh 'ls -l nohup.out'
                sh 'cat nohup.out'
            }
        }

        stage('Run echo') {
            steps {
                // Run Django tests
                sh 'echo manage.py'
                sh 'echo $path'
            }
        }

    }
}
