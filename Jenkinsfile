pipeline {
    agent any

    stages {

        stage('Gitleaks Scan') {
            steps {
                sh 'gitleaks detect --source . --no-git'
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
