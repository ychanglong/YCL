pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_VERSION = '1.29.2'
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
                    sh 'docker-compose -f docker-compose.yml up -d --build'
                }
            }
        }
        stage('Migrate') {
            steps {
                script {
                    // 运行数据库迁移
                    sh 'docker-compose exec web python manage.py migrate'
                }
            }
        }
        stage('Collect Static') {
            steps {
                script {
                    // 收集静态文件
                    sh 'docker-compose exec web python manage.py collectstatic --noinput'
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    // 运行测试
                    sh 'docker-compose exec web python manage.py test'
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