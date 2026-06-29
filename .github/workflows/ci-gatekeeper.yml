name: CI Gatekeeper

on:
  pull_request:
    branches:
      - main

  push:
    branches:
      - main

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
  SECRET_KEY: ${{ secrets.SECRET_KEY }}

jobs:
  build-and-push:

    runs-on: ubuntu-latest

    permissions:
      contents: write
      packages: write
      pages: write
      id-token: write

    defaults:
      run:
        shell: bash --noprofile --norc -euo pipefail {0}

    steps:

    ##################################################
    # Checkout
    ##################################################

    - name: Checkout Repository
      uses: actions/checkout@v4

    ##################################################
    # Required CI Inputs
    ##################################################

    - name: Validate Required CI Inputs
      run: |
        test -n "${SECRET_KEY}"
        test -f backend/requirements.txt
        test -f backend/Dockerfile
        test -f backend/pytest.ini
        test -f backend/tests/selenium/test_selenium_login.py
        test -f backend/tests/selenium/test_selenium_income.py
        test -f frontend/package-lock.json
        test -f frontend/tsconfig.json
        test -f frontend/tsconfig.app.json  
        test -f frontend/tsconfig.spec.json
        test -f frontend/src/test.ts
        test -f database/performance_profile.jmx

    ##################################################
    # Python
    ##################################################

    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.11"
        cache: pip

    ##################################################
    # Node
    ##################################################

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: "24"
        cache: npm
        cache-dependency-path: frontend/package-lock.json

    ##################################################
    # Chrome (Angular + Selenium)
    ##################################################

    - name: Setup Chrome
      uses: browser-actions/setup-chrome@v1

    - name: Configure Chrome Binary
      run: |
        CHROME_BIN_PATH="$(command -v chrome)"
        test -x "${CHROME_BIN_PATH}"
        echo "CHROME_BIN=${CHROME_BIN_PATH}" >> "${GITHUB_ENV}"

    ##################################################
    # Docker Buildx
    ##################################################

    - name: Setup Docker Buildx
      uses: docker/setup-buildx-action@v3

    ##################################################
    # Backend Dependencies
    ##################################################

    - name: Install Backend Dependencies
      working-directory: backend
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest selenium webdriver-manager allure-pytest pytest-cov

    ##################################################
    # Backend Tests
    ##################################################

    - name: Run Backend Unit Tests
      working-directory: backend
      run: |
        PYTHONPATH=. pytest tests/unit -v --alluredir=allure-results --cov=. --cov-report=html --cov-report=term-missing

    - name: Run Backend Integration Tests
      working-directory: backend
      run: |
        PYTHONPATH=. pytest tests/integration -v --alluredir=allure-results --cov=. --cov-report=html --cov-report=term-missing

    ##################################################
    # Frontend Dependencies
    ##################################################

    - name: Install Frontend Dependencies
      working-directory: frontend
      run: npm ci

    ##################################################
    # Angular Tests
    ##################################################

    - name: Run Angular Tests
      working-directory: frontend
      run: npx ng test --configuration=ci

    ##################################################
    # Build Docker Images
    ##################################################

    - name: Build Backend Image
      run: |
        docker build \
          -t finbud-backend:latest \
          ./backend

    - name: Build Frontend Image
      run: |
        docker build \
          --no-cache \
          -t finbud-frontend:latest \
          ./frontend

    ##################################################
    # Start Containers
    ##################################################

    - name: Start Backend
      run: |
        docker run -d \
          --name backend-test \
          -e SECRET_KEY="${SECRET_KEY}" \
          -p 8000:8000 \
          finbud-backend:latest

        if [ "$(docker inspect -f '{{.State.Running}}' backend-test)" != "true" ]; then
          docker logs backend-test
          exit 1
        fi

    - name: Start Frontend
      run: |
        docker run -d \
          --name frontend-test \
          -p 4200:80 \
          finbud-frontend:latest

        if [ "$(docker inspect -f '{{.State.Running}}' frontend-test)" != "true" ]; then
          docker logs frontend-test
          exit 1
        fi

    ##################################################
    # Wait for Backend
    ##################################################

    - name: Wait for Backend
      run: |
        for i in {1..30}; do
          if [ "$(docker inspect -f '{{.State.Running}}' backend-test)" != "true" ]; then
            docker logs backend-test
            exit 1
          fi

          if curl -fs http://localhost:8000/health; then
            echo "Backend ready."
            exit 0
          fi

          echo "Waiting for backend..."
          sleep 2
        done

        docker logs backend-test || true
        exit 1

    ##################################################
    # Wait for Frontend
    ##################################################

    - name: Wait for Frontend
      run: |
        for i in {1..30}; do
          if [ "$(docker inspect -f '{{.State.Running}}' frontend-test)" != "true" ]; then
            docker logs frontend-test
            exit 1
          fi

          if curl -fs http://localhost:4200; then
            echo "Frontend ready."
            exit 0
          fi

          echo "Waiting for frontend..."
          sleep 2
        done

        docker logs frontend-test || true
        exit 1

    ##################################################
    # Selenium Tests
    ##################################################

    - name: Run Selenium Regression Tests via Pytest Allure
      working-directory: backend
      run: |
        PYTHONPATH=. pytest tests/selenium -v --alluredir=allure-results

    - name: Dump Backend Logs on Failure
      if: failure() # 🚨 This triggers automatically ONLY if the step above fails
      run: |
        docker logs backend-test
        docker logs frontend-test

    ##################################################
    # Install Apache JMeter
    ##################################################

    - name: Install Apache JMeter
      run: |
        sudo apt-get update

        sudo apt-get install -y \
          openjdk-17-jre \
          wget \
          unzip

        wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.6.3.zip

        unzip apache-jmeter-5.6.3.zip

        echo "$PWD/apache-jmeter-5.6.3/bin" >> $GITHUB_PATH

    ##################################################
    # Verify JMeter
    ##################################################

    - name: Verify JMeter
      run: jmeter --version

    ##################################################
    # Run JMeter
    ##################################################

    - name: Run JMeter Performance Test
      run: |
        jmeter \
          -n \
          -t database/performance_profile.jmx \
          -JHOST=localhost \
          -JPORT=8000 \
          -l results.jtl \
          -e \
          -o jmeter-report

    ##################################################
    #  Report Artifact Collection & Packaging
    ##################################################

    - name: Upload JMeter Report
      id: jmeter_upload
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: jmeter-report
        path: jmeter-report/

    - name: Upload Selenium Report
      id: selenium_upload
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: selenium-report
        path: backend/allure-results/
        if-no-files-found: ignore

    - name: Upload Backend Test Report
      id: backend_upload
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: backend-test-report
        path: backend/coverage/
        if-no-files-found: ignore

    - name: Package All Reports
      id: package_reports
      if: always()
      run: |
        mkdir -p all-reports
        cp -r jmeter-report all-reports/ || true
        cp -r backend/coverage all-reports/backend-coverage || true
        cp -r backend/allure-results all-reports/backend-allure-results || true
        zip -r all-reports.zip all-reports

    - name: Upload Combined Reports
      id: combined_upload
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: all-reports
        path: all-reports.zip

    ##################################################
    # Interactive Download Dashboard Summary
    ##################################################

    - name: Generate Report Download Dashboard
      if: always()
      run: |
        echo "## 📊 Test & Performance Reports Dashboard" >> $GITHUB_STEP_SUMMARY
        echo "Click the direct download actions below to retrieve the test asset bundles instantly:" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "| Report Asset Target | Quick-Download Button Link |" >> $GITHUB_STEP_SUMMARY
        echo "| :--- | :--- |" >> $GITHUB_STEP_SUMMARY
        echo "| ⭐ **Combined Master Report Package** | [📥 Download all-reports.zip](${{ steps.combined_upload.outputs.artifact-url }}) |" >> $GITHUB_STEP_SUMMARY
        echo "| 📦 **JMeter Performance Data** | [📥 Download jmeter-report ZIP](${{ steps.jmeter_upload.outputs.artifact-url }}) |" >> $GITHUB_STEP_SUMMARY
        echo "| 🤖 **Selenium UI Regression Data** | [📥 Download selenium-report ZIP](${{ steps.selenium_upload.outputs.artifact-url }}) |" >> $GITHUB_STEP_SUMMARY
        echo "| ⚙️ **Core Backend Test Output** | [📥 Download backend-test-report ZIP](${{ steps.backend_upload.outputs.artifact-url }}) |" >> $GITHUB_STEP_SUMMARY
    
    ##################################################
    # Publish Interactive HTML Reports to Summary
    ##################################################

    - name: HTML Preview Deployment
      if: always() && hashFiles('jmeter-report/index.html') != ''
      uses: pavi2410/html-preview-action@v5
      with:
        html_file: index.html
        site_root: jmeter-report
        job_summary: true

    ##################################################
    # Print Docker Logs on Failure
    ##################################################

    - name: Backend Logs
      if: failure()
      run: docker logs backend-test || true

    - name: Frontend Logs
      if: failure()
      run: docker logs frontend-test || true

    ##################################################
    # Cleanup
    ##################################################

    - name: Stop Containers
      if: always()
      run: |
        docker stop backend-test || true
        docker stop frontend-test || true

        docker rm backend-test || true
        docker rm frontend-test || true

    ##################################################
    # Login GHCR
    ##################################################

    - name: Login to GitHub Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    ##################################################
    # Build and Push Backend
    ##################################################
    - name: Build and Push Backend
      uses: docker/build-push-action@v6
      with:
        context: backend
        file: backend/Dockerfile
        push: true
        tags: ghcr.io/slmakomazi/finbudplanner-backend:latest

    ##################################################
    # Build and Push Frontend
    ##################################################
    - name: Build and Push Frontend
      uses: docker/build-push-action@v6
      with:
        context: frontend
        file: frontend/Dockerfile
        push: true
        tags: ghcr.io/slmakomazi/finbudplanner-frontend:latest

    ##################################################
    # 📈 Compile & Publish Allure Dashboard Website
    ##################################################

    - name: Load Allure Report History
      uses: actions/checkout@v4
      if: always()
      continue-on-error: true
      with:
        ref: gh-pages
        path: gh-pages

    - name: Build Allure Test Report GUI Portal
      uses: simple-elf/allure-report-action@master
      if: always()
      with:
        allure_results: backend/allure-results
        allure_report: allure-report
        allure_history: allure-history

    - name: Post-Allure Workspace Chown Fix
      if: always()
      run: sudo chown -R $USER:$USER .

    - name: Deploy Report Portal to GitHub Pages
      uses: peaceiris/actions-gh-pages@v4
      if: always()
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: allure-history