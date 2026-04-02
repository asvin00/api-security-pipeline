pipeline {

    // "agent any" = run this pipeline on any available Jenkins build agent
    // An agent is the machine that actually runs the build commands
    agent any

    // Environment variables — available to ALL stages below
    // Think of these as global constants for the pipeline
    environment {
        APP_NAME  = 'my-python-app'
        VENV_DIR  = 'venv'           // name of the Python virtual environment folder
        PYTHON    = 'python3'         // command to invoke Python
    }

    // Trigger: automatically run when GitHub sends a push webhook
    triggers {
        githubPush()
    }

    stages {

        // ─────────────────────────────────────────────────────
        // STAGE 1: Checkout
        // Jenkins downloads the latest code from GitHub
        // "scm" = Source Code Management (Git in our case)
        // ─────────────────────────────────────────────────────
        stage('Checkout') {
            steps {
                echo '📥 Pulling latest code from GitHub...'
                checkout scm
                echo "✅ Code checked out. Branch: ${env.BRANCH_NAME}, Commit: ${env.GIT_COMMIT}"
            }
        }

        // ─────────────────────────────────────────────────────
        // STAGE 2: Dependency Install
        // Creates a Python virtual environment, then installs
        // all packages listed in requirements.txt
        // A venv = isolated Python environment so packages
        // don't conflict with the system Python
        // ─────────────────────────────────────────────────────
        stage('Dependency Install') {
            steps {
                echo '📦 Creating virtual environment and installing dependencies...'
                sh '''
                    # Create a fresh virtual environment
                    python3 -m venv venv

                    # Activate it (. = source = run the activate script)
                    . venv/bin/activate

                    # Upgrade pip to latest version
                    pip install --upgrade pip

                    # Install everything in requirements.txt
                    pip install -r requirements.txt

                    # Show what was installed (good for debugging)
                    pip list

                    echo "✅ All dependencies installed!"
                '''
            }
        }

        // ─────────────────────────────────────────────────────
        // STAGE 3: Build OK? Gate
        // Verifies the app can be imported without errors
        // If main.py has a syntax error, this stage fails here
        // before we even run tests — faster feedback
        // ─────────────────────────────────────────────────────
        stage('Build OK?') {
            steps {
                echo '🔍 Checking app can be imported (syntax + import check)...'
                sh '''
                    . venv/bin/activate
                    # Try to import the app — if there are syntax errors, this fails
                    python3 -c "from app.main import app; print('App imported OK ✅')"
                '''
            }
        }

        // ─────────────────────────────────────────────────────
        // STAGE 4: Pytest Unit Tests
        // Runs all test functions in the tests/ folder
        //
        // Flags explained:
        //   --junitxml  = saves results in XML (Jenkins reads this)
        //   --cov=app   = measure coverage of the app/ folder
        //   --cov-report= generate coverage reports
        //   -v          = verbose (show each test name)
        // ─────────────────────────────────────────────────────
        stage('Pytest Unit Tests') {
            steps {
                echo '🧪 Running Pytest unit tests...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ \
                        --junitxml=test-results.xml \
                        --cov=app \
                        --cov-report=xml:coverage.xml \
                        --cov-report=term-missing \
                        -v
                '''
            }
            post {
                always {
                    // "always" runs whether tests passed or failed
                    // Publish test results so Jenkins shows a test report UI
                    junit 'test-results.xml'
                }
                success {
                    echo '✅ All tests passed!'
                }
                failure {
                    echo '❌ Some tests FAILED. Fix your code and push again.'
                    // "error" stops the pipeline immediately with a failure message
                    error("Pipeline aborted — unit tests failed")
                }
            }
        }

        // ─────────────────────────────────────────────────────
        // STAGE 5: Tests Pass? (Decision Gate)
        // This stage only runs if Stage 4 succeeded
        // It's the green "Tests Pass?" diamond in the architecture
        // If we reach here, all tests passed ✅
        // ─────────────────────────────────────────────────────
        stage('Tests Pass?') {
            steps {
                echo '✅ Tests passed — proceeding to Dev Stage Complete'
                sh '''
                    . venv/bin/activate
                    # Show final coverage summary
                    coverage report --show-missing
                '''
            }
        }

        // ─────────────────────────────────────────────────────
        // STAGE 6: Dev Stage Complete
        // This is the final stage of Phase 1
        // Prints a summary of the build and signals readiness
        // for Phase 2 (Security scanning)
        // ─────────────────────────────────────────────────────
        stage('Dev Stage Complete') {
            steps {
                echo '🎉 Phase 1 — Build Stage Complete!'
                sh """
                    echo "=================================="
                    echo "  BUILD SUMMARY"
                    echo "=================================="
                    echo "  App:     ${APP_NAME}"
                    echo "  Build:   #${BUILD_NUMBER}"
                    echo "  Branch:  ${BRANCH_NAME}"
                    echo "  Commit:  ${GIT_COMMIT}"
                    echo "  Result:  PASSED ✅"
                    echo "  Next:    Phase 2 - Security Scan"
                    echo "=================================="
                """
            }
        }

    } // end stages

    // ─────────────────────────────────────────────────────
    // POST-PIPELINE ACTIONS
    // These run after ALL stages complete (or fail)
    // ─────────────────────────────────────────────────────
    post {
        success {
            echo "✅ Pipeline #${BUILD_NUMBER} completed successfully on branch ${BRANCH_NAME}"
        }
        failure {
            echo "❌ Pipeline #${BUILD_NUMBER} FAILED. Check the red stage above for details."
        }
        always {
            // Clean up the virtualenv after every build (save disk space)
            sh 'rm -rf venv'
            echo '🧹 Workspace cleaned up.'
        }
    }

} // end pipeline