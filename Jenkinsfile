pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                echo 'Cloning repository...'
                git branch: 'master', url: 'https://github.com/YourUsername/YourRepo.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Start Flask App') {
            steps {
                echo 'Starting Flask app in background...'
                bat 'start /B python app.py'
                sleep 5  // wait for Flask server to start
            }
        }

        stage('Test File Upload with curl') {
            steps {
                echo 'Testing /post1 endpoint using curl...'

                // Replace COOKIE_VALUE with a valid session cookie for a logged-in user
                bat '''
curl -X POST http://127.0.0.1:5000/post1 ^
  -H "Cookie: session=sambhavvinay20054@gmail.com" ^
  -F "post1=@test_image.jpg" ^
  -F "caption=Test Caption"
'''
            }
        }
    }

    post {
        always {
            echo 'Stopping Flask server...'
            bat 'taskkill /IM python.exe /F || exit 0'
        }
    }
}
