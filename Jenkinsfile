pipeline {
    agent any

    environment {
        IMAGE_NAME = "bhumikadesh/flask-devsecops-app"
        IMAGE_TAG = "v${BUILD_NUMBER}"

        GITOPS_REPO = "https://github.com/bhumikad1953-desh/flask-devsecops-gitops.git"
        GITOPS_BRANCH = "main"
    }

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
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh """
                trivy image \
                --severity HIGH,CRITICAL \
		${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Update GitOps Repository') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-token',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {

                    sh """
                    rm -rf gitops

                    git clone https://${GIT_USER}:${GIT_TOKEN}@github.com/bhumikad1953-desh/flask-devsecops-gitops.git gitops

                    cd gitops

                    sed -i 's|image:.*|image: ${IMAGE_NAME}:${IMAGE_TAG}|' k8s/deployment.yaml

                    git config user.email "jenkins@local"
                    git config user.name "Jenkins"

                    git add .

                    git commit -m "Updated image to ${IMAGE_TAG}" || true

                    git push origin ${GITOPS_BRANCH}
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }

        failure {
            echo "Pipeline failed. Please check the console output."
        }
    }
}
