pipeline {
    agent any

    environment {
        IMAGE_NAME = "docferuza2024/mock-api"
        IMAGE_TAG  = "latest"
        CONTAINER  = "mock-api"
        APP_PORT   = "8000"

        SSH_HOST = "YOUR.SERVER.IP"
        SSH_USER = "ubuntu"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Feruza-M/mock-api.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                  docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh """
                      echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                      docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('QA Tests') {
            steps {
                sh """
                  docker rm -f qa-${CONTAINER} || true
                  docker run -d --name qa-${CONTAINER} ${IMAGE_NAME}:${IMAGE_TAG}
                  sleep 5
                  docker exec qa-${CONTAINER} pytest
                  docker rm -f qa-${CONTAINER}
                """
            }
        }

        stage('Deploy to Remote Server') {
            steps {
                sshagent(['deploy-key']) {
                    sh """
                      ssh -o StrictHostKeyChecking=no ${SSH_USER}@${SSH_HOST} '
                        docker pull ${IMAGE_NAME}:${IMAGE_TAG} &&
                        docker rm -f ${CONTAINER} || true &&
                        docker run -d -p ${APP_PORT}:${APP_PORT} --name ${CONTAINER} ${IMAGE_NAME}:${IMAGE_TAG}
                      '
                    """
                }
            }
        }

        stage('Post-deploy Check') {
            steps {
                sh """
                  sleep 5
                  curl http://${SSH_HOST}:${APP_PORT}/order
                  curl http://${SSH_HOST}:${APP_PORT}/user
                  curl http://${SSH_HOST}:${APP_PORT}/catalog | jq '.[0]'
                """
            }
        }
    }

    post {
        always {
            sh "docker system prune -f"
        }
    }
}
