/* A Scripted Pipeline can include conditional tests (shown above), 
loops, try/catch/finally blocks and even functions.
*/

// Declarative //
pipeline {
  agent any
  parameters {
    string(name: 'Greeting', defaultValue: 'Hello', description: 'How should I
  greet the world?')
  }
  stages {
    stage('Example') {
      steps {
        echo "${params.Greeting} World!"
      }
    }
  }
  /* An environment directive used in the top-level pipeline block 
  will apply to all steps within the Pipeline.
  */
  environment {
    CC = 'clang'
  }
  // Declarative Pipeline supports an environment directive
  /*
  An environment directive defined within a stage will only apply 
  the given environment variables to steps within the stage.
  */
  stages {
    stage('Example') {
        environment {
            DEBUG_FLAGS = '-g'
        }
        steps {
            sh 'printenv'
        }
    }
  }
  stages {
      stage('Example') {
        steps {
            echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
        }
    }
    stage('Build') {
        steps {
            sh 'make'
            // only for basic reporting and file archival
            archiveArtifacts artifacts: '**/target/*.jar', fingerprint: true
        }
    }
    // plugins for test recording, reporting and visualization
    // (even historical trend analysis and visualization)
    stage('Test') {
        steps {
            /* `make check` returns non-zero on test failures,
            * using `true` to allow the Pipeline to continue nonetheless
            */
            sh 'make check || true'
            junit '**/target/*.xml'
        }
    }
    // "post conditions" such as: always, unstable, success, failure, and changed.
    post {
      always {
        junit '**/target/*.xml'
      }
      failure {
        mail to: team@example.com, subject: 'The Pipeline failed :('
      }
    }
  }
    // can imply a variety of steps
  stage('Deploy') {
        when {
            expression {
                currentBuild.result == null || currentBuild.result == 'SUCCESS' ①
            }
        }
            steps {
                sh 'make publish'
            }

    }
  }
}
// Script //
properties([parameters([string(defaultValue: 'Hello', description: 'How should I greet
the world?', name: 'Greeting')])])
node {
  checkout scm
  echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
  echo "${params.Greeting} World!"
  // source code is assembled, compiled, or packaged.
  // use plugins for invoking any build tool
  // invoke make from a shell step (sh) for Unix/Linux, bat for Windows
  // users of Scripted Pipeline must use the withEnv step.
  withEnv(["PATH+MAVEN=${tool 'M3'}/bin"]) {
    sh 'mvn -B verify'
  }
  stage('Build') {
    sh 'make'
    archiveArtifacts artifacts: '**/target/*.jar', fingerprint: true
  }
  stage('Test') {
    /* `make check` returns non-zero on test failures,
    * using `true` to allow the Pipeline to continue nonetheless
    */
    // Groovy’s built-in try/catch/finally semantics
    try {
      // never return a non-zero exit code
      // need to check currentBuild.result to know if test faiure
      sh 'make check'
      // return a non-zero exit code
      // sh 'make check' || true
    }
    // a chance to capture test reports without return non-zero exit code
    finally {
      junit '**/target/*.xml'
    }
  }
  stage('Deploy') {
    // test failures, currentBuild value would be UNSTABLE
    if (currentBuild.result == null || currentBuild.result == 'SUCCESS') { ①
        sh 'make publish'
    }
  }
}