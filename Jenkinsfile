pipeline {
    agent any
    stages {
        stage ('SCM checkout') {
            steps {
                script {
                    git branch: 'main', credentialsId: 'git-cred', url: 'https://github.com/Krishm2401/pythonweb.git'
                }
            }
        }
        stage('Set up Python') {
            steps {
                script {
                    def pythonVersion = '3'
                    sh "python3 -m pip install --upgrade pip"
                    sh "python3 -m pip install -r requirements.txt"
                }
            }
        }
        stage ('SonarQube Code analysis') {
            steps {
                script {
                    def scannerHome = tool 'sonarscanner4'
                    withSonarQubeEnv('sonar-pro') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=big-python"
                    }
                }
            }
        }
        stage('Docker Build Images') {
            steps {
                script {
                    sh 'docker build -t krishm2401/bigidhub2:v1 .'
                    sh 'docker images'
                }
            }
        }
        stage('Docker Push') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerPass', usernameVariable: 'dockerUser', passwordVariable: 'dockerPassword')]) {
                        sh "docker login -u ${dockerUser} -p ${dockerPassword}"
                        sh 'docker push krishm2401/bigidhub2:v1'
                        sh 'trivy image krishm2401/bigidhub2:v1 > scanning.txt'
                        // sh 'trivy fs --format table -o trivy_report.html'
                    }
                }
            }
        }
        stage('Deploy on k8s') {
            steps {
                script {
                    withKubeCredentials(kubectlCredentials: [[caCertificate: '', clusterName: 'eks.k8s.local', contextName: '', credentialsId: 'kubernetes', namespace: 'webapps', serverUrl: 'api-eks-k8s-local-jj1tc0-9ca525dbfa608d5d.elb.ap-south-1.amazonaws.com']]) {
                        sh 'kubectl create secret generic helm --from-file=.dockerconfigjson=/opt/docker/config.json --type kubernetes.io/dockerconfigjson --dry-run=client -oyaml > secret.yaml'
                        // sh 'kubectl apply -f secret.yaml'
                        // sh 'kubectl apply -f deployment.yaml'
                        // sh 'kubectl apply -f service.yaml'
                        sh 'helm package ./webapp'
                        sh 'helm list -n webapps -q | xargs -L1 helm uninstall -n webapps'
                        sh 'helm install web98 ./webapp-0.1.0.tgz'
                        sh 'helm ls'
                        sh 'kubectl get pods -o wide'
                        sh 'kubectl get svc'
                    }
                }
            }
        }
    }
    post { 
    always { 
        script { 
            def jobName = env.JOB_NAME 
            def buildNumber = env.BUILD_NUMBER 
            def pipelineStatus = currentBuild.result ?: 'UNKNOWN' 
            def bannerColor = pipelineStatus.toUpperCase() == 'SUCCESS' ? 'green' : 'red' 
                         
                         def body = """<html> 
                            <body> 
                                <div style="border: 4px solid ${bannerColor}; padding: 10px;"> 
                                    <h2>${jobName} - Build ${buildNumber}</h2> 
                                    <div style="background-color: ${bannerColor}; padding: 10px;"> 
                                        <h3 style="color: white;">Pipeline Status: ${pipelineStatus.toUpperCase()}</h3> 
                                    </div> 
                                    <p>Check the <a href="${BUILD_URL}">console output</a>.</p> 
                                </div> 
                            </body> 
                        </html>""" 
            emailext ( 
                subject: "${jobName} - Build ${buildNumber} - ${pipelineStatus.toUpperCase()}", 
                body: body, 
                to: 'recipent-bharathanavanee@gmail.com', 
                from: 'bharathanavanee@gmail.com', 
                replyTo: 'bharathanavanee@gmail.com', 
                mimeType: 'text/html', 
                attachmentsPattern: 'scanning.txt' 
            ) 
        } 
    } 
}
}
