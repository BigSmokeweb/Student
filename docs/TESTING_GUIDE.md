# Step-by-Step Testing & Verification Guide

> **Student:** Milind Sahu | **Roll No:** 124A1139 | **Experiment:** 3  
> **Target:** Student Record Management + Jenkins CI Pipeline

---

## Part 1: Install Required Tools on Windows 11

### Step 1.1: Install Java 21 (JDK)
1. Download **Eclipse Temurin JDK 21 (MSI)** from [Adoptium](https://adoptium.net/temurin/releases/?version=21).
2. Run installer and ensure **"Set JAVA_HOME variable"** and **"Add to PATH"** are checked.
3. Verify in a new Command Prompt or PowerShell:
   ```cmd
   java -version
   javac -version
   ```
   *Expected:* Shows `openjdk version "21.x.x"`.

### Step 1.2: Install Apache Maven
1. Download Maven binary zip (`apache-maven-3.9.x-bin.zip`) from [Maven Official Site](https://maven.apache.org/download.cgi).
2. Extract to `C:\Program Files\Apache\apache-maven-3.9.x`.
3. Add `C:\Program Files\Apache\apache-maven-3.9.x\bin` to your system environment variable `Path`.
4. Verify:
   ```cmd
   mvn -version
   ```
   *Expected:* Shows `Apache Maven 3.9.x` and `Java version: 21.x.x`.

---

## Part 2: Test the Java Application Locally

Navigate to the project folder:
```cmd
cd c:\Users\Milind\Downloads\StudentRecordManagement
```

### Step 2.1: Compile Code
```cmd
mvn clean compile
```
- **What to look for:** `BUILD SUCCESS`.
- **Files created:** Compiled `.class` files generated under `target/classes/com/student/`.

### Step 2.2: Execute Unit Tests
```cmd
mvn test
```
- **What to look for:** 
  ```text
  [INFO] Tests run: 10, Failures: 0, Errors: 0, Skipped: 0
  [INFO] BUILD SUCCESS
  ```
- **Reports generated:** Surefire XML test reports created in `target/surefire-reports/`.

### Step 2.3: Package Executable JAR
```cmd
mvn package
```
- **What to look for:** `BUILD SUCCESS` and creation of:
  `target/student-record-management-1.0-SNAPSHOT.jar`

### Step 2.4: Run & Test Console Menu
```cmd
java -jar target/student-record-management-1.0-SNAPSHOT.jar
```
Test each menu action in order:
1. **Option 1 (Add Student):**
   - Enter ID: `101`
   - Enter Name: `Milind Sahu`
   - Enter Age: `21`
   - Enter Course: `Computer Science`
   - Enter Email: `milind@example.com`
   - *Expected:* `"Success: Student added successfully!"`
2. **Option 1 (Duplicate ID test):**
   - Enter same ID: `101`
   - *Expected:* `"Error: Student with ID 101 already exists!"`
3. **Option 2 (View All):**
   - *Expected:* Prints details of student `101`. Total records: `1`.
4. **Option 3 (Search by ID):**
   - Enter `101` -> Displays student.
   - Enter `999` -> `"No student found with ID: 999"`.
5. **Option 4 (Update Student):**
   - Enter ID: `101`
   - Update Age to `22`
   - *Expected:* `"Success: Student record updated successfully!"`. View all to verify age changed.
6. **Option 5 (Delete Student):**
   - Enter `101` -> `"Success: Student with ID 101 was deleted."`.
   - View all again -> `"No student records found."`.
7. **Option 6 (Exit):**
   - *Expected:* Prints `"Exiting Student Record Management. Goodbye!"` and terminates cleanly.

---

## Part 3: Push to GitHub

```cmd
git init
git branch -M main
git add .
git commit -m "feat: complete student record management with jenkins ci"
git remote add origin https://github.com/YOUR_USERNAME/StudentRecordManagement.git
git push -u origin main
```
*(Replace `YOUR_USERNAME` with your actual GitHub username).*

---

## Part 4: Test Jenkins CI Pipeline on Windows

### Step 4.1: Start Jenkins & Configure Tools
1. Open browser: `http://localhost:8080`.
2. Go to **Manage Jenkins** -> **Tools**:
   - **JDK:** Name = `JDK21`, JAVA_HOME = `C:\Program Files\Eclipse Adoptium\jdk-21.x.x` (auto-install unchecked).
   - **Maven:** Name = `Maven3`, MAVEN_HOME = `C:\Program Files\Apache\apache-maven-3.9.x` (auto-install unchecked).
   - **Git:** Name = `Default`, path to Git = `C:\Program Files\Git\cmd\git.exe`.
   - Click **Save**.

### Step 4.2: Create & Run the Pipeline Job
1. Click **New Item** -> Name: `StudentRecord-CI` -> Select **Pipeline** -> Click **OK**.
2. Under **Pipeline**:
   - Definition: `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: `https://github.com/YOUR_USERNAME/StudentRecordManagement.git`
   - Branch Specifier: `*/main`
   - Script Path: `Jenkinsfile`
   - Click **Save**.
3. Click **Build Now**.

### Step 4.3: Verify Build #1 (Green Pipeline)
1. Click on `#1` -> **Console Output**.
2. Verify all 5 stages succeed:
   - `Checkout`
   - `Build` (`mvn -B clean compile`)
   - `Test` (`mvn -B test`)
   - `Package` (`mvn -B package`)
   - `Archive Artifact`
3. Check **Test Result** tab: 10/10 JUnit tests passed.
4. Check **Build Artifacts**: `target/student-record-management-1.0-SNAPSHOT.jar` is preserved.

---

## Part 5: Test Automated Trigger & Failure Alert

### Step 5.1: Test Poll SCM (Auto Build on Push)
1. Open [`README.md`](file:///c:/Users/Milind/Downloads/StudentRecordManagement/README.md) in your editor.
2. Make a minor edit (e.g. add a space or comment at the end) and save.
3. Commit and push:
   ```cmd
   git commit -am "test: trigger automated poll scm build"
   git push origin main
   ```
4. Do not click "Build Now". Wait ~2 minutes.
5. In Jenkins, verify **Build #2** triggers automatically.
6. Open Build #2 log and confirm: `"Started by an SCM change"`.

### Step 5.2: Test Deliberate Pipeline Failure & Email Alert
1. Open [`src/test/java/com/student/StudentServiceTest.java`](file:///c:/Users/Milind/Downloads/StudentRecordManagement/src/test/java/com/student/StudentServiceTest.java).
2. In `testAddStudentSuccess`, change:
   ```java
   assertEquals(1, service.getAllStudents().size(), "Student count should be 1");
   ```
   to:
   ```java
   assertEquals(5, service.getAllStudents().size(), "Student count should be 1");
   ```
3. Commit and push:
   ```cmd
   git commit -am "test: deliberate assertion failure to test failure alert"
   git push origin main
   ```
4. Observe **Build #3** in Jenkins:
   - Stage `Test` fails in RED.
   - Overall build status: **FAILURE**.
   - JUnit report highlights `testAddStudentSuccess` failed: `expected: <5> but was: <1>`.
   - Failure email is sent via configured SMTP (see [JENKINS_SETUP.md](file:///c:/Users/Milind/Downloads/StudentRecordManagement/docs/JENKINS_SETUP.md) Step 9).

### Step 5.3: Restore Green Pipeline
1. In `StudentServiceTest.java`, change `5` back to `1`.
2. Commit and push:
   ```cmd
   git commit -am "fix: restore passing unit test assertion"
   git push origin main
   ```
3. Confirm **Build #4** triggers and finishes with **SUCCESS** across all 5 stages.
