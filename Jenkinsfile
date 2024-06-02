pipeline {
    agent {
        kubernetes{
            yaml '''
            apiVersion: v1
            Kind: Pod
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


    environment{
        DOCKER_IMAGE = "maoravidan/projectapp"

    }



    stages{
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }



        stage('maven version'){
            steps{
                container('maven'){
                    sh 'mvn -version'
                }
            }
        }





        stage('Build and Push Docker Image') {
            when {
                branch 'main'
            }
            steps {
                container('ez-docker-helm-build') {
                    script {
                        withDockerRegistry(credentialsId: 'docker-hub'){
                        // Build Docker image
                            sh "docker build -t ${DOCKER_IMAGE}:${env.BUILD_NUMBER} ./test1"
                            sh "docker build -t ${DOCKER_IMAGE}:latest ."

                        // Push Docker image to Docker Hub
                            sh "docker push ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                            sh "docker push ${DOCKER_IMAGE}:latest"
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
            steps{
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



        stage('Trigger next update pipline') {
            when {
                branch 'main'
            }
            steps {
                build job: 'update', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER)]
            }
        }


    }



    post {
        failure {
            emailext body: 'The build failed. Please check the build logs for details.',
                     subject: "Build failed: ${env.BUILD_NUMBER}",
                     to: 'avidanos75@gmail.com'
'
        }
    }
}
