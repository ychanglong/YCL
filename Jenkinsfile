pipeline {
    agent any

    environment {
    http_proxy='http://10.187.215.117:3128'
    https_proxy='https://10.187.215.117:3128'
    PATH = ""
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
//         stage('Install dependencies') {
//             steps {
//                 // Install Python dependencies
//                 sh 'python3 -m venv /usr/venv'
//                 sh 'source /usr/venv'
//                 sh 'pip install django'
//             }
//         }

        stage('Run echo') {
            steps {
                // Run Django tests
                sh 'echo manage.py'
                sh 'echo $path'
            }
        }

        stage('Run tests') {
            steps {
                // Run Django tests
                sh '/usr/bin/python3.9 manage.py test'
            }
        }

        stage('Deploy') {
            steps {
                // Run Django migrations and collect static files
                sh '/usr/bin/python3.9 manage.py migrate'
                sh '/usr/bin/python3.9 manage.py collectstatic --noinput'

                // Restart Django server or use WSGI/Gunicorn
                sh '/usr/bin/python3.9 manage.py runserver 0.0.0.0:8000 &'
            }
        }
    }
}
