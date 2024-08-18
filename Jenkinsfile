pipeline {
    agent any
    stages {
        stage ('SCM checkout') {
            steps {
                script{
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
         stage ('SonarQube Code analysis'){
            steps {
                script{
                    def scannerHome = tool 'sonarscanner4';
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
                    withCredentials([usernamePassword(credentialsId: 'dockerPass', usernameVariable: 'krishm2401', passwordVariable: 'dockerPassword')]) {
                        sh "docker login -u krishm2401 -p ${dockerPassword}"
                        sh 'docker push krishm2401/bigidhub2:v1'
                        // sh 'trivy image krishm2401/bigidhub:v1 > scan.txt'
                    }
                }
            }
        }
        stage('Deploy on k8s') {
            steps {
                script {
                    withKubeCredentials(kubectlCredentials: [[caCertificate: '', clusterName: 'eks.k8s.local', contextName: '', credentialsId: 'kubernetes', namespace: 'webapps', serverUrl: 'api-eks-k8s-local-jj1tc0-9ca525dbfa608d5d.elb.ap-south-1.amazonaws.com']]) {
                        sh 'kubectl create secret generic helm --from-file=.dockerconfigjson=/opt/docker/config.json  --type kubernetes.io/dockerconfigjson --dry-run=client -oyaml > secret.yaml'
                        // sh 'kubectl apply -f secret.yml'
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
}    
