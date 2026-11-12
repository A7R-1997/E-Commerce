pipeline {
    agent any 

    // متغيرات عامة تستخدم داخل مراحل الـ Pipeline
    environment {
        REGISTRY = "my-docker-registry.internal" // عنوان سجل صور Docker الخاص بالشركة
        IMAGE_NAME = "ecommerce-api"             // اسم صورة الحاوية الخاصة بالتطبيق
        TAG = "${env.BUILD_NUMBER}"              // إصدار الصورة يعتمد على رقم البناء الحالي في Jenkins
    }

    // المراحل الأساسية لمسار العمل (CI/CD Stages)
    stages {
        
        // 1. مرحلة سحب الكود
        stage('Checkout Code') {
            steps {
                checkout scm // سحب أحدث نسخة من الكود البرمجي من مستودع GitHub
            }
        }

        // 2. مرحلة فحص الجودة (Static Code Analysis)
        stage('Code Linting & Static Analysis') {
            steps {
                sh 'pip install flake8'         // تثبيت أداة الفحص النحوي لكود بايثون
                sh 'flake8 app/ tests/'         // فحص مجلد التطبيق والاختبارات بحثاً عن أي أخطاء برمجية
            }
        }

        // 3. مرحلة تشغيل الخدمات عبر Docker Compose
        stage('Build & Run Services via Docker Compose') {
            steps {
                sh 'docker-compose up -d --build' // بناء وتشغيل حاوية الـ API وقاعدة البيانات في الخلفية
            }
        }

        // 4. مرحلة تشغيل اختبارات Pytest واستخراج تقارير التغطية
        stage('Run Pytest & Generate Coverage Reports') {
            steps {
                // تشغيل الاختبارات داخل الحاوية وتوليد تقرير بصيغة XML
                sh 'docker-compose exec -T web pytest --cov=app --junitxml=reports/pytest-results.xml'
            }
        }

        // 5. مرحلة بناء صورة الإنتاج النهائية (Production Docker Image)
        stage('Build Production Docker Image') {
            steps {
                // بناء صورة Docker النهائية ووسمها بالمتغيرات المعرفة مسبقاً
                sh 'docker build -t ${REGISTRY}/${IMAGE_NAME}:${TAG} .'
            }
        }

        // 6. مرحلة الفحص الأمني والثغرات
        stage('Security & Vulnerability Scan') {
            steps {
                echo "Running security scan on container image..." // مكان مخصص لإضافة أدوات فحص الأمان (مثل Trivy)
            }
        }
    }

    // الإجراءات التي تنفذ بعد انتهاء المراحل (سواء نجاحاً أو فشلاً)
    post {
        always {
            junit 'reports/pytest-results.xml'   // قراءة تقارير الاختبارات وعرضها في لوحة تحكم Jenkins
            sh 'docker-compose down -v'          // إيقاف وحذف الحاويات وقاعدة البيانات لتنظيف البيئة دائماً
        }
        success {
            echo "Pipeline completed successfully! Microservice built and tested." // رسالة تظهر عند نجاح كل المراحل
        }
        failure {
            echo "Pipeline failed. Check test reports and logs." // رسالة تنبيه تظهر إذا حدث خطأ في أي مرحلة
        }
    }
}