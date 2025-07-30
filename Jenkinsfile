pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/tejanayak/sample.git', branch: 'main'
      }
    }
    stage('Run Python') {
      steps {
        bat 'hello.py'
      }
    }
  }
}
