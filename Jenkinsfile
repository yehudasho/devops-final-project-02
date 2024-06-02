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
                - name: POSTGRES_USER
                  value: "mongo"
                - name: POSTGRES_PASSWORD
                  value: "mongo"
                - name: POSTGRES_DB
                  value: "mydb"
                - name: HOST
                  value: "localhost"
              - name: ez-docker-helm-build
                image: ezezeasy/ez-docker-helm-build:1.41
                imagePullPolicy: Always
                securityContext:
                  privileged: true
            '''
        }
    }

    environment {
        DOCKER_IMAGE = "maoravidan/projectapp"
        FASTAPI_IMAGE = "maoravidan/projectapp"
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

        stage('Build and Push Docker Images') {
            when {
                branch 'main'
            }
            steps {
                container('ez-docker-helm-build') {
                    script {
                        withDockerRegistry(credentialsId: 'docker-hub') {
                            // Build and Push Maven Docker image
                            sh "docker build -t ${DOCKER_IMAGE}:${env.BUILD_NUMBER} ./test1"
                            sh "docker build -t ${DOCKER_IMAGE}:react ./test1"
                            sh "docker push ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                            sh "docker push ${DOCKER_IMAGE}:react"

                            // Build and Push FastAPI Docker image
                            sh "docker build -t ${FASTAPI_IMAGE}:${env.BUILD_NUMBER} ./fast_api"
                            sh "docker build -t ${FASTAPI_IMAGE}:fastapi ./fast_api"
                            sh "docker push ${FASTAPI_IMAGE}:${env.BUILD_NUMBER}"
                            sh "docker push ${FASTAPI_IMAGE}:fastapi"
                        }
                    }
                }
            }
        }

        stage('merge request') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'maor_git', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
                        sh """
                        curl -X POST -u ${GITHUB_USER}:${GITHUB_TOKEN} -d '{
                            "title": "Merge feature to main",
                            "head": "feature",
                            "base": "main"
                        }' https://api.github.com/repos/maor75/Sela_Project/pulls
                        """
                    }
                }
            }
        }
    }

   post {
    always {
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
