# Agent Implementation Brief — Student Record Management + Jenkins CI

> **Role:** You are a coding agent working in the user's VS Code project workspace. Build a complete, runnable Java console Student Record Management application with Maven and JUnit 5, plus a Windows-compatible Jenkins declarative CI pipeline. Treat this document as the implementation specification and checklist. Do the work rather than merely describing it.
>
> **Important platform constraint:** The original college assignment specifies Jenkins on **Ubuntu**, but the user explicitly does **not** want to install or download Ubuntu. Implement the app and Jenkins pipeline for **Windows 11**, using `bat` rather than Unix `sh`. Clearly disclose in documentation that the Windows deployment is a deviation from the original Ubuntu-specific requirement and needs instructor approval if Ubuntu is mandatory. Do not install Ubuntu, Docker, WSL, or a virtual machine.

## 1. Project goal and scenario

**Experiment:** Configure Jenkins and create a continuous integration (CI) pipeline for automated application build and integration.

**Scenario:** A development team experiences errors and delays due to manual builds. The solution must automatically retrieve source from GitHub, compile it, run JUnit tests, package a runnable JAR, archive the artifact, report test results, rebuild on new commits, and email on failure.

**Application:** Student Record Management System, implemented as a **Java 21 console application**, managed with Maven. Spring Boot and databases are not necessary. In-memory data is acceptable, and should be identified as nonpersistent in README.

## 2. Working guidelines for the coding agent

1. Inspect the existing workspace first. Preserve functional code; make targeted edits if files already exist. If the workspace is empty, initialize the project structure below.
2. Implement actual runnable source code, tests, configuration, and instructions. Avoid mockups, pseudocode, unrelated features, unnecessary frameworks, and paid services.
3. Use **Java 21**, **Maven 3.x**, **JUnit Jupiter (JUnit 5)**, and Jenkins **Declarative Pipeline**. Target Windows commands wherever OS-dependent.
4. Do **not** put passwords, personal access tokens, SMTP passwords, private emails, or other credentials in committed source files. Use placeholders and Jenkins credentials/configuration.
5. Do **not** claim that Jenkins was installed, that a GitHub webhook or polling trigger ran, that emails were sent, or that builds passed without observing the corresponding result.
6. If Java/Maven/Git are available, execute tests and report outputs. If unavailable, leave precise instructions rather than fabricating results.
7. The user has limited RAM (~8 GB), so keep the app lightweight and avoid unnecessary background services.
8. Never overwrite unrelated user files or force-push existing repositories. Ask before destructive or account-changing operations.

## 3. Required repository structure

```text
StudentRecordManagement/
├── pom.xml
├── Jenkinsfile
├── README.md
├── .gitignore
├── src/
│   ├── main/
│   │   └── java/com/student/
│   │       ├── Main.java
│   │       ├── Student.java
│   │       └── StudentService.java
│   └── test/
│       └── java/com/student/
│           └── StudentServiceTest.java
└── docs/
    ├── WINDOWS_JENKINS_SETUP.md
    └── PRACTICAL_REPORT.md
```

Do not commit `target/`, `.class` files, local IDE metadata, credentials, or build outputs.

## 4. Java application requirements

### Student model — `com.student.Student`

- Fields: `int id`, `String name`, `int age`, `String course`, `String email`.
- Constructor; getters; setters for editable fields; readable `toString()`.
- Student IDs must remain stable on updates.

### Business logic — `com.student.StudentService`

- `boolean addStudent(Student student)` — add student if the ID is not already present.
- `Student getStudent(int id)` — return matching student or `null` if missing.
- `List<Student> getAllStudents()` — return a list of all students.
- `boolean updateStudent(int id, String name, int age, String course, String email)` — update if present; `false` if absent.
- `boolean deleteStudent(int id)` — remove if present; `false` if absent.
- Use an in-memory `LinkedHashMap<Integer, Student>` or equivalent. Do not add a database.
- Handle duplicate IDs and missing records without crashes. Basic validation of ID, age and required text fields is desirable; document rules and test them if implemented.

### Console interface — `com.student.Main`

Provide an interactive menu with these options:

1. Add Student
2. View All Students
3. Search Student by ID
4. Update Student
5. Delete Student
6. Exit

Handle malformed numeric input gracefully. Display success/failure messages and print student details in readable format. The application must be runnable with `java -jar ...` after packaging.

## 5. Maven and unit testing

Implement `pom.xml` with:

- Coordinates: `com.student:student-record-management:1.0-SNAPSHOT`.
- Java 21 compilation (`maven.compiler.release=21`).
- JUnit 5 (`org.junit.jupiter:junit-jupiter`) as `test` dependency.
- Maven Compiler and Surefire plugins configured for JUnit 5.
- Maven JAR plugin with `Main-Class: com.student.Main` so the JAR runs directly.
- Stable explicit plugin and dependency versions; avoid version ranges and snapshots except the local project version.

Write **at least eight independent JUnit tests** in `StudentServiceTest.java`:

1. Successfully add a student.
2. Retrieve an existing student.
3. Update student details.
4. Delete an existing student.
5. Reject duplicate student IDs.
6. Searching a missing ID returns `null`.
7. Deleting a missing ID returns `false`.
8. Updating a missing ID returns `false`.

Use `@BeforeEach` to create a fresh service instance. Assert actual behavior, not just that methods execute. Optionally test viewing records and validation.

**Commands that must work on Windows (from project root):**

```cmd
mvn clean compile
mvn test
mvn package
java -jar target/student-record-management-1.0-SNAPSHOT.jar
```

Expect Maven Surefire to write XML reports to `target/surefire-reports/` and the runnable JAR to `target/student-record-management-1.0-SNAPSHOT.jar`.

## 6. Declarative Jenkins pipeline — exact required stages

Create a root-level file named **`Jenkinsfile`** (no extension). It must be a syntactically valid declarative Jenkins Pipeline, designed for a **Windows Jenkins agent**.

Required stage names and behavior, in order:

1. **Checkout** — `checkout scm`; pipeline job must be configured as "Pipeline script from SCM" against GitHub.
2. **Build** — use Windows `bat` step to run `mvn -B clean compile`.
3. **Test** — `bat 'mvn -B test'`.
4. **Package** — `bat 'mvn -B package'`.
5. **Archive Artifact** — `archiveArtifacts artifacts: 'target/*.jar', fingerprint: true`.

Also include:

- `agent any` (on a Windows Jenkins installation, or otherwise explicitly restrict execution to Windows-labeled agents).
- `tools { jdk 'JDK21'; maven 'Maven3' }`. The Jenkins administrator must configure these exact tool names under **Manage Jenkins → Tools**.
- `options { skipDefaultCheckout(true) }` if using an explicit Checkout stage, to avoid duplicate checkouts.
- `triggers { pollSCM('H/2 * * * *') }` to check for new commits approximately every two minutes (a GitHub webhook is optional, not required for localhost). This trigger must automatically cause a build when SCM changes are detected.
- In `post { always { ... } }`, publish JUnit results with Jenkins' `junit` step against `target/surefire-reports/*.xml`. Handle missing reports gracefully when an earlier stage failed (for example `allowEmptyResults: true`), while still reporting real test failures.
- In `post { failure { ... } }`, send a failure email using Jenkins' `mail` step. Use `your-email@example.com` as an obvious replaceable recipient placeholder. Include job name, build number, and build URL in the notification.
- An optional `post { success { echo '...' } }` is fine.
- **Do not** use `sh`, Bash paths, hardcoded credentials, or Linux-specific commands in the Windows pipeline.

**Suggested implementation template** (may be improved, but required behavior must remain):

```groovy
pipeline {
    agent any
    tools {
        jdk 'JDK21'
        maven 'Maven3'
    }
    options { skipDefaultCheckout(true) }
    triggers { pollSCM('H/2 * * * *') }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build') {
            steps { bat 'mvn -B clean compile' }
        }
        stage('Test') {
            steps { bat 'mvn -B test' }
        }
        stage('Package') {
            steps { bat 'mvn -B package' }
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
            mail to: 'your-email@example.com',
                 subject: "Jenkins Build Failed: ${env.JOB_NAME}",
                 body: "Build ${env.BUILD_NUMBER} failed. ${env.BUILD_URL}"
        }
    }
}
```

Note: The Jenkins `mail` step requires working SMTP settings and an appropriate plugin. A successful failure-notification test cannot be assumed simply because this step appears in the Jenkinsfile.

## 7. GitHub integration requirements

- Provide exact commands for initializing and pushing the project to a GitHub repo named `StudentRecordManagement` without running them on the user's account unless authorized:

```bash
git init
git branch -M main
git add .
git commit -m "Initial Student Record Management project with Jenkins CI"
git remote add origin https://github.com/YOUR_USERNAME/StudentRecordManagement.git
git push -u origin main
```

- Document two modes: public repository (can check out anonymously) and private repository (configure a GitHub token as Jenkins **Username with password** credential, username = GitHub login, password = token, ID `github-token`). Use least-privilege Contents: Read-only permission for checkout.
- In Jenkins job config, choose **New Item → Pipeline → Pipeline script from SCM**, SCM Git, repository URL, appropriate credentials, branch `*/main`, script path `Jenkinsfile`.
- Do not write a token into Git URLs or checked-in files.

## 8. Windows Jenkins setup guide — `docs/WINDOWS_JENKINS_SETUP.md`

Write beginner-friendly numbered steps covering all of the following:

1. Verify/install Java JDK 21, Maven 3.x and Git. Include `java -version`, `javac -version`, `mvn -version`, and `git --version`.
2. Install the **Jenkins LTS Windows installer** from the official Jenkins website and run Jenkins as a Windows service with a suitable service account. Open `http://localhost:8080`; use the installer-provided initial admin password path; install suggested plugins; create admin user.
3. Ensure Pipeline, Git, GitHub, JUnit, Mailer, and Credentials plugins are present.
4. Under **Manage Jenkins → Tools**, set JDK name `JDK21`, Maven name `Maven3`, and configure Git executable. Explain how to find paths and that the Jenkins Windows service account must be able to access them.
5. Under **Manage Jenkins → Credentials**, create GitHub repository credentials if necessary; never expose tokens in screenshots.
6. Create a Jenkins Pipeline job configured with SCM Git, branch `*/main`, script path `Jenkinsfile`.
7. Run the first build manually and inspect **Console Output**, Test Result, and archived `.jar` artifact.
8. Explain Poll SCM vs webhooks: because `localhost` is not publicly reachable from GitHub, use Poll SCM for the local setup; after the first execution Jenkins should schedule polling and a changed Git commit should trigger a new build.
9. Configure **Manage Jenkins → System → E-mail Notification** with verified SMTP, sender, TLS/SSL settings and app password/credential. Provide Gmail SMTP (`smtp.gmail.com`, SSL port 465 or STARTTLS 587) as an example only. Do not embed any actual email password in the repository.
10. Demonstrate a deliberate JUnit assertion failure, commit and push, verify the failed pipeline and failure email, then restore the assertion and push a fixed commit. The final codebase must have passing tests.
11. Include troubleshooting for `mvn not recognized`, Java version/path, `Cannot run program sh`, credential failures, absent JUnit results, SCM polling not running, SMTP auth failures and localhost connectivity.
12. Clearly note: **Windows is used instead of Ubuntu per user constraint; verify grading acceptance with the professor.**

## 9. README and report

### `README.md`

Include: short project overview, features, requirements, project tree, setup, commands, sample console usage, design summary, test cases, CI stages, GitHub polling behavior, email setup dependency and limitation that records are in-memory.

### `docs/PRACTICAL_REPORT.md`

Create a concise Software Engineering lab-ready practical report containing:

- Title, Aim, Problem Statement.
- Objectives and required software.
- Theory: CI, Jenkins, Maven, JUnit, Git/GitHub, Jenkinsfile.
- Brief system architecture diagram (Markdown code/text is fine).
- Implementation procedure.
- Pipeline stages explained.
- Test cases table with **expected** outcomes (do not mark tests passed unless verified).
- Observation/Result section with spaces to fill in **actual** Jenkins run details and screenshots.
- Conclusion and 6–10 relevant viva questions with short answers.
- Note about Windows replacing the specified Ubuntu setup.

## 10. Acceptance checklist (do not claim completion without verifying)

- [ ] Correct project folder structure and `com.student` Java packages.
- [ ] Six-option working Java console application.
- [ ] CRUD operations and duplicate/missing student handling.
- [ ] Maven Java 21 configuration and runnable JAR manifest.
- [ ] Eight or more meaningful JUnit 5 tests.
- [ ] `mvn clean compile` succeeds locally (if tooling available).
- [ ] `mvn test` succeeds and emits Surefire XML (if tooling available).
- [ ] `mvn package` produces runnable JAR (if tooling available).
- [ ] Root `Jenkinsfile` with five exact stages in order.
- [ ] Windows `bat` commands, JDK/Maven tool definitions.
- [ ] `post { always { junit ... } }` and `post { failure { mail ... } }`.
- [ ] Automatic Poll SCM trigger configured.
- [ ] Documentation for GitHub credentials, SMTP and Jenkins Tools.
- [ ] No secrets in repository; `.gitignore` excludes build outputs.
- [ ] Jenkins successful and failing runs captured **only if actually executed**.
- [ ] Final code restored to green tests after intentional failure demo.

## 11. Expected final response from coding agent

Once files are written, report:

1. Every created/modified file with relative path.
2. A short summary of implemented features and pipeline behavior.
3. Exact local commands run, plus their real results or blockers.
4. Any environment/deployment steps requiring user action (Jenkins installation, GitHub repo/credentials, SMTP, first pipeline run).
5. Any remaining requirements not yet verified.

Proceed to implement the project in the workspace now. Do not stop after generating a plan.
