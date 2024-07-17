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

         stage('Install pip') {
            steps {
                sh 'sudo apt update && sudo apt install -y python3-pip'
            }
        }

//         stage('Install dependencies') {
//             steps {
//                 // Install Python dependencies
//                 sh 'pip install -r requirements.txt'
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
