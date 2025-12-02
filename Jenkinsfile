pipeline {
    agent any

    environment {
        APP_IMAGE      = "ci-cd-testing-app:latest"
        SELENIUM_IMAGE = "ci-cd-testing-app-selenium:latest"
        APP_CONTAINER  = "ci-cd-testing-app-container"
        APP_PORT       = "5000"
    }

    stages {

        /* ---------------------------
              CHECKOUT STAGE
        ---------------------------- */
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        /* ---------------------------
              CODE LINTING
        ---------------------------- */
        stage('Code Linting') {
            steps {
                echo "Running code linting..."
                sh '''
                    # Install flake8 for the Jenkins user only
                    python3 -m pip install --user flake8

                    # Run linting via python module so PATH issues don't matter
                    python3 -m flake8 app || true
                '''
            }
        }

        /* ---------------------------
              CODE BUILD
        ---------------------------- */
        stage('Code Build') {
            steps {
                echo "Building application (installing dependencies)..."
                sh '''
                    # Install app dependencies for the Jenkins user only
                    python3 -m pip install --user -r app/requirements.txt

                    # Byte-compile Python files
                    python3 -m compileall app
                '''
            }
        }

        /* ---------------------------
              UNIT TESTING
        ---------------------------- */
        stage('Unit Testing') {
            steps {
                echo "Running unit tests..."
                sh '''
                    # Install pytest for the Jenkins user only
                    python3 -m pip install --user pytest

                    # Run unit tests
                    python3 -m pytest -q tests/unit
                '''
            }
        }

        /* ---------------------------
          DOCKER BUILD + DEPLOYMENT
        ---------------------------- */
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

                    echo "Running new app container..."
                    sh '''
                        docker run -d --name "$APP_CONTAINER" -p "$APP_PORT":5000 "$APP_IMAGE"
                    '''

                    echo "Waiting for app to start..."
                    sh 'sleep 10'
                }
            }
        }

        /* ---------------------------
              SELENIUM TESTING
        ---------------------------- */
        stage('Selenium Testing') {
            steps {
                script {

                    echo "Building Selenium test image..."
                    sh '''
                        docker build -t "$SELENIUM_IMAGE" -f Dockerfile.selenium .
                    '''

                    echo "Running Selenium container tests..."
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

    /* ---------------------------
         POST PIPELINE ACTIONS
    ---------------------------- */
    post {
        always {
            echo "Cleaning up leftover containers..."
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
            echo "Pipeline failed 💥 — check logs for details."
        }
    }
}
