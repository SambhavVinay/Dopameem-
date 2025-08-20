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

        stage('Run Flask') {
            steps {
                echo 'Starting Flask server...'
                bat '''
                    start /B python app.py
                    ping 127.0.0.1 -n 10 >nul
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                bat 'curl -X POST http://127.0.0.1:5000/upload -F "file=@sample.jpg"'
            }
        }

        stage('Cleanup') {
            steps {
                echo 'Stopping Flask server...'
                bat 'taskkill /IM python.exe /F || exit 0'
            }
        }
    }
}
