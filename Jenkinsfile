pipeline {
    agent any

    environment {
    http_proxy='http://10.187.215.117:3128'
    https_proxy='https://10.187.215.117:3128'
    PATH = ""
    PYTHONPATH = "/usr/venv/bin"
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
                sh 'su -'
                sh '123456'
                // Install Python dependencies
                sh 'python3 -m venv /usr/venv'
                sh 'source /usr/venv/bin/activate'
                sh 'pip install django'
            }
        }

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
                sh 'python3 manage.py test'
            }
        }

        stage('Deploy') {
            steps {
                // Run Django migrations and collect static files
                sh 'python3 manage.py migrate'
                sh 'python3 manage.py collectstatic --noinput'

                // Restart Django server or use WSGI/Gunicorn
                sh 'python3 manage.py runserver 0.0.0.0:8000 &'
            }
        }
    }
}
