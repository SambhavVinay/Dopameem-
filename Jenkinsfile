pipeline
{
    agent any
    
        stages
        {
            stage('Clone')
            {
                steps
                {
                    echo 'cloning repo..'
                    git branch:'master', url:'https://github.com/SambhavVinay/Dopameem-'
                }
            }
            stage('install dependencies')
            {
                steps
                {
                    echo 'installing Prerequisites...'
                    bat 'pip install -r requirements.txt'
                }
            }
            stage('Flask Run')
            {
                steps{
                    echo 'running flask...'
                    bat '''
                        start /B python app.py
                        ping 127.0.0.1 -n 5 >nul
                    '''
                }
            }
            stage('Dopameme Posts Upload Test')
            {
                steps
                {
                    echo 'logging in...'
                    bat '''
                        curl -X POST http://127.0.0.1:5000/login ^
                        -d "username=testuser" ^
                        -d "password=testpass" ^
                        -c cookies.txt
                    '''

                    echo 'upload posts Test..'
                    bat '''
                        curl -X POST http://127.0.0.1:5000/post1 ^
                        -b cookies.txt
                        -F "post1=@C:/Users/Admin/OneDrive/Desktop/siberianhusky-test.jpg" ^
                        -F "caption=Syberian Husky" ^ 
                        -L                
                    '''
                }
            }

        }
    
}