pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                echo 'Cloning repository...'
                git branch: 'master', url: 'https://github.com/SambhavVinay/Dopameem-'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Starting Flask and running tests...'
                bat '''
                    start "FlaskApp" python app.py
                    timeout /T 10
                    pytest -v test_upload.py
                '''
            }
        }
    }

    post {
        always {
            echo 'Stopping Flask process...'
            bat 'taskkill /F /FI "WINDOWTITLE eq FlaskApp" || exit 0'
        }
    }
}
