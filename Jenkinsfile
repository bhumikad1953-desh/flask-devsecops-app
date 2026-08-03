pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Gitleaks Scan') {
            steps {
                sh 'gitleaks detect --source . --no-git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarQubeScanner'
                    withSonarQubeEnv('SonarQube') {
                        sh """
                        ${scannerHome}/bin/sonar-scanner \
                          -Dsonar.projectKey=flask-devsecops-app \
                          -Dsonar.projectName=flask-devsecops-app \
                          -Dsonar.sources=. \
                          -Dsonar.python.version=3
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask-devsecops-app:v1 .'
            }
        }

        stage('Tag Docker Image') {
            steps {
                sh 'docker tag flask-devsecops-app:v1 bhumikadesh/flask-devsecops-app:v1'
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push bhumikadesh/flask-devsecops-app:v1'
            }
        }
    }
}
