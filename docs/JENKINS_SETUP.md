# Jenkins CI/CD Setup Guide (Windows 11 Primary)

> **Student:** Milind Sahu | **Roll No:** 124A1139 | **Experiment:** 3  
> **Platform Note:** Jenkins was installed on Windows 11; the pipeline is OS-independent and also runs on Ubuntu.

---

## 1. Prerequisites Installation & Verification

Ensure JDK 21, Apache Maven 3.9+, and Git are installed on Windows.

Open PowerShell or Command Prompt and run:
```cmd
java -version
javac -version
mvn -version
git --version
```

### Environment Variables Setup:
- **JAVA_HOME**: `C:\Program Files\Eclipse Adoptium\jdk-21.x.x` (or your JDK installation path without `\bin`).
- **MAVEN_HOME**: `C:\Program Files\Apache\apache-maven-3.9.x`.
- **Path**: Append `%JAVA_HOME%\bin` and `%MAVEN_HOME%\bin` and `C:\Program Files\Git\cmd`.

---

## 2. Install Jenkins LTS on Windows 11

1. Download the Windows LTS MSI installer from [https://www.jenkins.io/download/](https://www.jenkins.io/download/).
2. Run the installer:
   - Select JDK 21 directory when prompted for Java Home.
   - Keep default service port `8080` (or test port availability).
   - Install as a Windows Service (`jenkins.exe`).

---

## 3. Unlock Jenkins & Install Plugins

1. Open your browser and navigate to: `http://localhost:8080`.
2. Locate the initial admin password from:
   `C:\ProgramData\Jenkins\.jenkins\secrets\initialAdminPassword`
3. Paste password and select **Install suggested plugins**.
4. Create your Admin user (e.g., username `admin`, enter password and name).

---

## 4. Configure Build Tools in Jenkins

Navigate to **Manage Jenkins** -> **Tools**:

1. **JDK**:
   - Click **Add JDK**.
   - Name: `JDK21` *(must match Jenkinsfile exactly)*.
   - Uncheck **Install automatically**.
   - JAVA_HOME: e.g. `C:\Program Files\Eclipse Adoptium\jdk-21.0.x` (no `\bin`).

2. **Maven**:
   - Click **Add Maven**.
   - Name: `Maven3` *(must match Jenkinsfile exactly)*.
   - Uncheck **Install automatically**.
   - MAVEN_HOME: e.g. `C:\Program Files\Apache\apache-maven-3.9.x` (no `\bin`).

3. **Git**:
   - Name: `Default`.
   - Path to Git executable: `C:\Program Files\Git\cmd\git.exe` (run `where git` in cmd to verify).
4. Click **Save**.

---

## 5. Verify Required Plugins

Navigate to **Manage Jenkins** -> **Plugins** -> **Installed Plugins**. Ensure these are present:
- Pipeline
- Git Plugin
- GitHub Plugin
- JUnit Plugin
- Mailer Plugin
- Credentials Plugin
- Timestamper Plugin

---

## 6. GitHub Integration & Credentials (R4)

### Step 1: Initialize Local Git and Push
```cmd
cd c:\Users\Milind\Downloads\StudentRecordManagement
git init
git branch -M main
git add .
git commit -m "Initial Student Record Management project with Jenkins CI"
git remote add origin https://github.com/YOUR_USERNAME/StudentRecordManagement.git
git push -u origin main
```

### Step 2: Add Credentials in Jenkins (for Private Repositories)
1. Go to GitHub -> Settings -> Developer settings -> Personal access tokens -> Fine-grained tokens.
2. Generate token with **Contents: Read-only** permission for `StudentRecordManagement`.
3. In Jenkins: **Manage Jenkins** -> **Credentials** -> **System** -> **Global credentials** -> **Add Credentials**.
   - Kind: `Username with password`
   - Username: Your GitHub username
   - Password: Generated personal access token
   - ID: `github-token`
   - Description: GitHub Read-only PAT
4. Click **Create**. *(For public repos, no credential is required).*

---

## 7. Create Jenkins Declarative Pipeline Job

1. Go to Jenkins Dashboard -> **New Item**.
2. Enter item name: `StudentRecord-CI`.
3. Select **Pipeline** and click **OK**.
4. In Job Configuration:
   - Scroll to **Pipeline** section.
   - Definition: **Pipeline script from SCM**.
   - SCM: **Git**.
   - Repository URL: `https://github.com/YOUR_USERNAME/StudentRecordManagement.git`.
   - Credentials: Select `github-token` (or `none` if repo is public).
   - Branch Specifier: `*/main`.
   - Script Path: `Jenkinsfile`.
5. Click **Save**.

---

## 8. Run First Build & Verify Outputs

1. On the `StudentRecord-CI` job page, click **Build Now**.
2. Click on the build number (e.g. `#1`) -> **Console Output**.
3. Verify that all 5 stages succeed:
   - `Checkout`
   - `Build` (`mvn -B clean compile`)
   - `Test` (`mvn -B test`)
   - `Package` (`mvn -B package`)
   - `Archive Artifact`
4. Confirm `target/student-record-management-1.0-SNAPSHOT.jar` is listed under **Build Artifacts**.
5. Click **Test Result** to view published JUnit test reports.

---

## 9. Configure Email Notifications on Failure (R9)

1. Navigate to **Manage Jenkins** -> **System**.
2. Scroll to **E-mail Notification**:
   - SMTP server: `smtp.gmail.com`
   - Click **Advanced...**
   - Check **Use SMTP Authentication**
   - User Name: Your Gmail address
   - Password: Gmail **App Password** (Generated via Google Account -> Security -> 2-Step Verification -> App Passwords)
   - Check **Use SSL**
   - SMTP Port: `465` (or uncheck SSL, check TLS on port `587`)
   - Check **Test configuration by sending test e-mail**, enter recipient, and click **Test configuration**.
3. Replace placeholder `your-email@example.com` in `Jenkinsfile` with your recipient email address.

---

## 10. Automated Triggers & Failure Demonstration

### A. Poll SCM Demonstration (R8)
1. Edit `README.md` locally, commit, and push:
   ```cmd
   git commit -am "docs: test poll scm trigger"
   git push origin main
   ```
2. Wait up to 2 minutes. Jenkins Poll SCM will detect the commit and trigger build `#2` automatically.
3. Verify the build log shows: `"Started by an SCM change"`.

### B. Intentional Failure Demonstration (R9)
1. Edit `src/test/java/com/student/StudentServiceTest.java`:
   In `testAddStudentSuccess`, change `assertEquals(1, service.getAllStudents().size())` to `assertEquals(5, service.getAllStudents().size())`.
2. Commit and push:
   ```cmd
   git commit -am "test: deliberate assertion failure"
   git push origin main
   ```
3. Jenkins runs build `#3`:
   - Stage `Test` fails.
   - Status marks as **FAILURE**.
   - JUnit shows 1 failure.
   - Failure email is dispatched to your configured inbox.

### C. Restore Passing State
1. Revert `5` back to `1` in `StudentServiceTest.java`.
2. Commit and push:
   ```cmd
   git commit -am "fix: restore green unit test"
   git push origin main
   ```
3. Confirm build `#4` finishes **SUCCESS**.

---

## 11. Troubleshooting Guide

| Issue | Root Cause | Solution |
|---|---|---|
| `'mvn' is not recognized` | Maven bin directory not in system `Path` or Jenkins tool path | Add Maven to system `Path` and configure `Maven3` under Jenkins Tools. |
| `No tool named JDK21 found` | Name mismatch in Manage Jenkins -> Tools | Ensure the name is exactly `JDK21` in tool configuration. |
| `Cannot run program "sh"` | Linux command executed on Windows | Use cross-platform Jenkinsfile with `isUnix()` check. |
| `HTTP 403 / 401 on Checkout` | Invalid GitHub credentials or repo is private | Add GitHub PAT credential in Jenkins with read access. |
| `Empty JUnit results` | Tests did not run or surefire directory missed | Check if Maven Surefire plugin generated `target/surefire-reports/*.xml`. |
| `Polling not firing` | Poll SCM needs initial manual build | Run first build manually to register the polling schedule. |
| `SMTP Authentication Failed` | Standard Gmail password used instead of App Password | Generate a dedicated App Password from Google Account Security. |
| `localhost:8080 does not open` | Jenkins service stopped | Open `services.msc`, locate **Jenkins**, and click **Start**. |

---

## 12. Optional Ubuntu Deployment Fallback

If instructor specifically requires Ubuntu Linux:
```bash
sudo apt update
sudo apt install -y fontconfig openjdk-21-jdk maven git
sudo apt install -y jenkins
sudo systemctl enable --now jenkins
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
Configure `JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64` and `MAVEN_HOME=/usr/share/maven`. The existing `Jenkinsfile` runs without modification on Ubuntu.
