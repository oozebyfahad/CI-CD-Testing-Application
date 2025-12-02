pipeline {
    agent any

    environment {
        APP_IMAGE      = "your-docker-username/your-app:latest"
        SELENIUM_IMAGE = "your-docker-username/your-app-selenium:latest"
        APP_CONTAINER  = "your-app-container"
        APP_PORT       = "5000"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/your-username/your-repo.git'
            }
        }

        stage('Code Linting') {
            steps {
                echo "Running code linting..."
                sh '''
                pip install --upgrade pip
                pip install flake8
                flake8 app || true
                '''
            }
        }

        stage('Code Build') {
            steps {
                echo "Building application (installing deps)..."
                sh '''
                pip install -r app/requirements.txt
                python -m compileall app
                '''
            }
        }

        stage('Unit Testing') {
            steps {
                echo "Running unit tests..."
                sh '''
                pip install pytest
                pytest -q tests/unit
                '''
            }
        }

        stage('Containerized Deployment') {
            steps {
                script {
                    echo "Building Docker image for app..."
                    sh """
                    docker build -t ${APP_IMAGE} -f Dockerfile .
                    """

                    // Stop and remove any old container
                    sh """
                    if [ "$(docker ps -q -f name=${APP_CONTAINER})" ]; then
                      docker stop ${APP_CONTAINER}
                      docker rm ${APP_CONTAINER}
                    fi
                    """

                    echo "Running app container..."
                    sh """
                    docker run -d --name ${APP_CONTAINER} -p ${APP_PORT}:5000 ${APP_IMAGE}
                    """

                    // Optional: small delay to ensure app is up
                    sh "sleep 10"
                }
            }
        }

        stage('Selenium Testing') {
            steps {
                script {
                    echo "Building Selenium test image..."
                    sh """
                    docker build -t ${SELENIUM_IMAGE} -f Dockerfile.selenium .
                    """

                    echo "Running Selenium tests container..."
                    // We pass APP_URL via env var
                    sh """
                    docker run --rm \
                       --network host \
                       -e APP_URL=http://localhost:${APP_PORT} \
                       ${SELENIUM_IMAGE}
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up containers..."
            sh '''
            if [ "$(docker ps -q -f name=${APP_CONTAINER})" ]; then
              docker stop ${APP_CONTAINER}
              docker rm ${APP_CONTAINER}
            fi
            '''
        }
        success {
            echo "Pipeline succeeded 🎉"
        }
        failure {
            echo "Pipeline failed 💥 — check logs in each stage."
        }
    }
}
