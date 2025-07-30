pipeline {
  agent any
  environment {
    DB_HOST     = 'localhost'
    DB_PORT     = '3306'
    DB_NAME     = 'test_db'
    DB_USER     = 'root'
    DB_PASSWORD = 'your_mysql_password'
    // Optionally add MySQL bin directory if needed:
    PATH        = "${env.PATH};C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin"
  }
  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', credentialsId: 'git-credentials', url: 'https://github.com/tejanayak/sample.git'
      }
    }
    stage('Setup Database') {
      steps {
        bat """
          mysql -h %DB_HOST% --port=%DB_PORT% -u %DB_USER% -p%DB_PASSWORD% -e "DROP DATABASE IF EXISTS \\"%DB_NAME%\\";"
          mysql -h %DB_HOST% --port=%DB_PORT% -u %DB_USER% -p%DB_PASSWORD% -e "CREATE DATABASE \\"%DB_NAME%\\";"
        """
        bat 'npm run migrate'
      }
    }
    stage('Install Dependencies') {
      steps {
        bat 'npm install'
      }
    }
    stage('Run Integration Tests') {
      steps {
        bat 'npm run test:integration'
      }
    }
  }
  post {
    always {
      bat """
        mysql -h %DB_HOST% --port=%DB_PORT% -u %DB_USER% -p%DB_PASSWORD% -e "DROP DATABASE IF EXISTS \\"%DB_NAME%\\";"
      """
    }
    success {
      echo 'Integration tests passed successfully!'
    }
    failure {
      echo 'Integration tests failed.'
    }
  }
}
