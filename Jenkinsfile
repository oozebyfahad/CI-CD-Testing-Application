pipeline {
    agent any

    environment {
        // You can rename these if you want
        APP_IMAGE      = "ci-cd-testing-app:latest"
        SELENIUM_IMAGE = "ci-cd-testing-app-selenium:latest"
        APP_CONTAINER  = "ci-cd-testing-app-container"
        APP_PORT       = "5000"
    }

    stages {
        stage('Checkout') {
            steps {
                // Use the same repo Jenkins pulled the Jenkinsfile from
                checkout scm
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
                    sh '''
                    docker build -t "$APP_IMAGE" -f Dockerfile .
                    '''

                    echo "Stopping old container if running..."
                    sh '''
                    if [ "$(docker ps -q -f name=$APP_CONTAINER)" ]; then
                      docker stop "$APP_CONTAINER"
                      docker rm "$APP_CONTAINER"
                    fi
                    '''

                    echo "Running app container..."
                    sh '''
                    docker run -d --name "$APP_CONTAINER" -p "$APP_PORT":5000 "$APP_IMAGE"
                    '''

                    echo "Waiting for app to start..."
                    sh 'sleep 10'
                }
            }
        }

        stage('Selenium Testing') {
            steps {
                script {
                    echo "Building Selenium test image..."
                    sh '''
                    docker build -t "$SELENIUM_IMAGE" -f Dockerfile.selenium .
                    '''

                    echo "Running Selenium tests container..."
                    sh '''
                    docker run --rm \
                       --network host \
                       -e APP_URL=http://localhost:"$APP_PORT" \
                       "$SELENIUM_IMAGE"
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up containers..."
            sh '''
            if [ "$(docker ps -q -f name=$APP_CONTAINER)" ]; then
              docker stop "$APP_CONTAINER"
              docker rm "$APP_CONTAINER"
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
