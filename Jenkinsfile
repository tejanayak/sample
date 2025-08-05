pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/tejanayak/sample.git', branch: 'main'
            }
        }
        stage('Setup Environment') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install flask mysql-connector-python
                '''
            }
        }
        stage('Run Python') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    python api.py
                '''
            }
        }
    }
    post {
        always {
            bat '''
                if exist venv (
                    rmdir /s /q venv
                )
            '''
        }
    }
}
