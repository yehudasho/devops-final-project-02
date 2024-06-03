pipeline {
    agent {
        kubernetes {
            yaml '''
            apiVersion: v1
            kind: Pod
            spec:
              containers:
              - name: maven
                image: maven:alpine
                command:
                - cat
                tty: true
              - name: mongodb
                image: mongo:latest
                env:
                - name: MONGO_INITDB_ROOT_USERNAME
                  value: "root"
                - name: MONGO_INITDB_ROOT_PASSWORD
                  value: "maor"
                - name: MONGO_INITDB_DATABASE
                  value: "mydb"
              - name: dind
                image: docker:latest
                command:
                - dockerd-entrypoint.sh
                args:
                - --host=tcp://127.0.0.1:2375
                - --host=unix:///var/run/docker.sock
                securityContext:
                  privileged: true
                volumeMounts:
                - name: docker-graph-storage
                  mountPath: /var/lib/docker
              - name: ez-docker-helm-build
                image: ezezeasy/ez-docker-helm-build:1.41
                imagePullPolicy: Always
                env:
                - name: DOCKER_HOST
                  value: tcp://127.0.0.1:2375
                securityContext:
                  privileged: true
            volumes:
            - name: docker-graph-storage
              emptyDir: {}
            '''
        }
    }

    environment {
        DOCKER_IMAGE = "maoravidan/projectapp"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('maven version') {
            steps {
                container('maven') {
                    sh 'mvn -version'
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                container('ez-docker-helm-build') {
                    script {
                        // Build Maven Docker image
                        sh "docker build -t ${DOCKER_IMAGE}:react ./test1"

                        // Build FastAPI Docker image
                        sh "docker build -t ${DOCKER_IMAGE}:fastapi ./fast_api"
                    }
                }
            }
        }

        stage('Run and Validate Containers') {
            steps {
                script {
                    // Run MongoDB container
                    sh '''
                    docker run -d --name mongodb -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=maor -e MONGO_INITDB_DATABASE=mydb -p 27017:27017 mongo:latest
                    '''
                    // Run FastAPI container
                    sh '''
                    docker run -d --name fastapi_app -p 8080:80 ${DOCKER_IMAGE}:fastapi
                    '''
                    // Validate FastAPI service is running
                    sh '''
                    sleep 10
                    curl -f http://localhost:8080
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                // Stop and remove containers
                sh 'docker stop mongodb fastapi_app || true'
                sh 'docker rm mongodb fastapi_app || true'
            }
            echo 'Pipeline post'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            emailext body: 'The build failed. Please check the build logs for details.',
                     subject: "Build failed: ${env.BUILD_NUMBER}",
                     to: 'avidanos75@gmail.com'
        }
    }
}
