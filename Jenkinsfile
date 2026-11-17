pipeline {
    agent any 

    environment {
        REGISTRY = "my-docker-registry.internal"
        IMAGE_NAME = "ecommerce-api"
        TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Code Linting & Static Analysis') {
            steps {
                bat 'python -m pip install flake8'
                bat 'python -m flake8 app/ tests/ --max-line-length=120 --exit-zero'
            }
        }

        stage('Build & Run Services via Docker Compose') {
            steps {
                bat 'docker-compose up -d db'
                bat 'ping 127.0.0.1 -n 8 > nul'
                bat 'docker-compose up -d --build web'
                bat 'ping 127.0.0.1 -n 4 > nul'
            }
        }

        stage('Run Pytest & Generate Coverage Reports') {
            steps {
                bat 'if not exist reports mkdir reports'
                bat 'docker-compose exec -T -e PYTHONPATH=. web pytest --cov=app --junitxml=reports/pytest-results.xml'
            }
        }

        stage('Build Production Docker Image') {
            steps {
                bat "docker build -t ${REGISTRY}/${IMAGE_NAME}:${TAG} ."
            }
        }

        stage('Security & Vulnerability Scan') {
            steps {
                echo "1. فحص كود بايثون من الثغرات الأمنية باستخدام Bandit..."
                bat 'python -m pip install bandit'
                bat 'python -m bandit -r app/ -ll || exit /b 0'

                echo "2. فحص صورة Docker من الثغرات الأمنية باستخدام Trivy..."
                bat "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL ${REGISTRY}/${IMAGE_NAME}:${TAG} || exit /b 0"
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/pytest-results.xml'
            bat 'docker-compose down -v'
        }
        success {
            echo "Pipeline completed successfully! Microservice built, tested, and scanned."
        }
        failure {
            echo "Pipeline failed. Check test reports and security logs."
        }
    }
}