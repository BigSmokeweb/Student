// Runs a shell command on Linux (sh) or Windows (bat)
def run(String cmd) {
    if (isUnix()) {
        sh cmd
    } else {
        bat cmd
    }
}

pipeline {
    agent any

    tools {
        jdk 'JDK21'
        maven 'Maven3'
    }

    options {
        skipDefaultCheckout(true)
        timestamps()
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                script { run('mvn -B clean compile') }
            }
        }

        stage('Test') {
            steps {
                script { run('mvn -B test') }
            }
        }

        stage('Package') {
            steps {
                script { run('mvn -B package') }
            }
        }

        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
            }
        }
    }

    post {
        always {
            junit testResults: 'target/surefire-reports/*.xml',
                  allowEmptyResults: true
        }
        success {
            echo 'CI pipeline succeeded.'
        }
        failure {
            mail to: 'milindsahu1316@gmail.com',
                 subject: "Jenkins Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: """The Jenkins CI pipeline failed.

Job:    ${env.JOB_NAME}
Build:  #${env.BUILD_NUMBER}
Status: FAILURE
Logs:   ${env.BUILD_URL}console
"""
        }
    }
}
