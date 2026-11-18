
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv venv
                    venv/bin/pip install --upgrade pip
                    venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    venv/bin/python -m pytest -v \
                    --junitxml=test-results.xml
                '''
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'app/*.py, requirements*.txt, README.md, test-results.xml',
                                 fingerprint: true
            }
        }
    }

    post {
        always {
            junit 'test-results.xml'
        }

        success {
            echo 'CampusTrack CI pipeline completed successfully!'
        }

        failure {
            echo 'CampusTrack CI pipeline failed. Check the logs.'
        }
    }
}
