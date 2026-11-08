pipeline {
    agent any

    tools {
        // تأكد من ضبط اسم إصدار بايثون وملحق الـ pip في خادم Jenkins لديك (Manage Jenkins > Tools)
        // أو يمكنك استبداله بالاعتماد على بايثون المثبت في النظام مباشرة.
        // يمكننا تبسيط الأوامر للاعتماد على بيئة النظام مباشرة كالتالي:
    }

    stages {
        stage('Checkout Code') {
            steps {
                // جلب الكود من المستودع الخاص بك
                checkout scm
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    ./venv/bin/python -m pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Code Quality (Flake8)') {
            steps {
                // فحص جودة الكود ومعايير كتابته
                sh '''
                    ./venv/bin/flake8 app.py test_app.py
                '''
            }
        }

        stage('Run Tests (Pytest)') {
            steps {
                // تنفيذ اختبارات الوحدات البرمجية وتوليد تقرير
                sh '''
                    ./venv/bin/pytest --junitxml=test-reports/results.xml
                '''
            }
            post {
                always {
                    // حفظ نتائج الاختبارات في لوحة تحكم Jenkins
                    junit 'test-reports/results.xml'
                }
            }
        }
    }

    post {
        success {
            echo '🎉 تم بناء المشروع واجتياز كافة الاختبارات بنجاح تام!'
        }
        failure {
            echo '❌ فشل المشروع في إحدى مراحل الفحص أو الاختبار!'
        }
    }
}