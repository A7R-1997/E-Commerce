pipeline {
    agent any 

    environment {
        REGISTRY = "my-docker-registry.internal"
        IMAGE_NAME = "ecommerce-api"
        TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        // 1. مرحلة سحب الكود
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        // 2. مرحلة فحص جودة الكود (Flake8)
        stage('Code Linting & Static Analysis') {
            steps {
                bat 'pip install flake8'
                bat 'flake8 app/ tests/ --max-line-length=120'
            }
        }

        // 3. مرحلة تشغيل الخدمات عبر Docker Compose
        stage('Build & Run Services via Docker Compose') {
            steps {
                bat 'docker-compose up -d --build'
            }
        }

        // 4. مرحلة تشغيل اختبارات Pytest واستخراج التقارير
        stage('Run Pytest & Generate Coverage Reports') {
            steps {
                bat 'if not exist reports mkdir reports'
                bat 'docker-compose exec -T -e PYTHONPATH=. web pytest --cov=app --junitxml=reports/pytest-results.xml'
            }
        }

        // 5. مرحلة بناء صورة الإنتاج النهائية
        stage('Build Production Docker Image') {
            steps {
                bat "docker build -t ${REGISTRY}/${IMAGE_NAME}:${TAG} ."
            }
        }

        // 6. مرحلة الفحص الأمني واكتشاف الثغرات (DevSecOps)
        stage('Security & Vulnerability Scan') {
            steps {
                echo "1. فحص كود بايثون من الثغرات الأمنية باستخدام Bandit..."
                bat 'pip install bandit'
                bat 'bandit -r app/ -ll || exit /b 0'

                echo "2. فحص صورة Docker من الثغرات الأمنية باستخدام Trivy..."
                bat "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL ${REGISTRY}/${IMAGE_NAME}:${TAG}"
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