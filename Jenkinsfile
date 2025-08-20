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
                echo 'Running tests against Flask app...'
                bat '''
                    start /B python app.py
                    timeout /T 5
                    pytest -v test_upload.py
                '''
            }
        }
    }
    post {
        always {
            echo 'Killing leftover Flask process...'
            bat 'taskkill /F /IM python.exe || exit 0'
        }
    }
}
