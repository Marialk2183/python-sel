pipeline {
  agent any
  options { timestamps() }

  environment {
    CI        = '1'              // run tests headless
    VENV      = '.venv'
    WDM_LOCAL = '1'              // cache chromedriver locally
    WDM_CACHE = "${WORKSPACE}\\wdm-cache"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Setup Python') {
      steps {
        powershell '''
          $ErrorActionPreference = "Stop"
          Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

          if (Test-Path $env:VENV) { Remove-Item -Recurse -Force $env:VENV }
          py -3.11 -m venv $env:VENV

          . ".\\$($env:VENV)\\Scripts\\Activate.ps1"
          python -m pip install --upgrade pip
          if (Test-Path requirements.txt) {
            pip install -r requirements.txt
          } else {
            pip install pytest pytest-cov selenium webdriver-manager
          }

          if (-not (Test-Path reports)) { New-Item -ItemType Directory -Path reports | Out-Null }
        '''
      }
    }

    stage('Run Tests') {
      steps {
        powershell '''
          $ErrorActionPreference = "Stop"
          Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
          . ".\\$($env:VENV)\\Scripts\\Activate.ps1"
          $env:CI = "1"
          pytest
        '''
      }
      post {
        always {
          junit 'reports/junit.xml'
          // If you installed the "Code Coverage API" plugin, you can publish coverage:
          // publishCoverage adapters: [coberturaAdapter('reports/coverage.xml')], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
          archiveArtifacts artifacts: 'reports/**', fingerprint: true, onlyIfSuccessful: false
        }
      }
    }
  }
}
