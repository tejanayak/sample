pipeline {
  agent any
  environment {
    DB_HOST     = 'localhost'
    DB_PORT     = '5432'
    DB_NAME     = 'test_db'
    DB_USER     = 'postgres'
    DB_PASSWORD = 'your_postgres_password'
    PATH        = "${env.PATH};C:\\Program Files\\PostgreSQL\\14\\bin" // adjust version
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
          set PGPASSWORD=%DB_PASSWORD%
          psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -c "DROP DATABASE IF EXISTS %DB_NAME%;"
          psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -c "CREATE DATABASE %DB_NAME%;"
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
        set PGPASSWORD=%DB_PASSWORD%
        psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -c "DROP DATABASE IF EXISTS %DB_NAME%;"
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
