# Student Record Management + Jenkins CI: One-Time Complete Project Brief

> **For the coding agent:** Read this whole file, then build everything in it in a single pass. Do not stop at a plan. When done, run the Section 12 verification and report real results only.
>
> **Student:** Milind Sahu | **Roll No:** 124A1139 | **Experiment:** 3

---

## 1. Official assignment (source of truth)

**Aim:** To configure Jenkins and create CI pipelines for automated build and integration of application code.

**Task:** A development team is facing delays and errors due to manual application builds. To improve efficiency, they need an automated solution for building and integrating code. As a DevOps engineer, set up Jenkins and create a pipeline to streamline the process and ensure consistent builds.

| # | Requirement from the assignment | Where it is satisfied in this brief |
|---|---|---|
| R1 | Student Record Management app (Java console or Spring Boot REST) with JUnit tests | Sections 4, 5 |
| R2 | Install Jenkins on Ubuntu (VM or free-tier cloud) | Section 8 (Windows primary, Ubuntu path included) |
| R3 | Configure JDK, Maven, Git under Manage Jenkins -> Tools | Section 8, Step 4 |
| R4 | Connect Jenkins to a GitHub repo with credentials | Section 7, Section 8 |
| R5 | Declarative Jenkinsfile | Section 6 |
| R6 | Stages: Checkout -> Build (`mvn clean compile`) -> Test (`mvn test`) -> Package (`mvn package`) -> Archive artifact | Section 6 |
| R7 | JUnit results published with the `junit` step | Section 6 |
| R8 | Trigger: GitHub webhook or Poll SCM, every commit starts a build | Section 6, Section 8 |
| R9 | Email notification on failure using `post { failure { ... } }` | Section 6, Section 8 |

The project is **complete only when every row R1-R9 is demonstrably done** (Section 12).

## 2. Ubuntu vs Windows: how this brief handles it

The assignment says Ubuntu. The student prefers not to install Ubuntu or a VM. So:

- **Primary setup: Jenkins on Windows 11** (Windows service installer).
- **The Jenkinsfile is cross-platform**: it uses `sh` on Linux and `bat` on Windows via `isUnix()`. The same file runs unchanged if the student later moves Jenkins to Ubuntu.
- **Section 13 gives the Ubuntu install commands** as a ready fallback if the professor insists on Ubuntu.
- The README and report must state plainly: *"Jenkins was installed on Windows 11; the pipeline is OS-independent and also runs on Ubuntu."* Do not hide this.

Do not install Ubuntu, WSL, Docker, or a VM unless the user asks.

## 3. Agent rules

1. Inspect the workspace first. Keep existing working files; make targeted edits.
2. No secrets in the repo: no passwords, tokens, SMTP passwords. Use placeholders (`YOUR_USERNAME`, `your-email@example.com`).
3. Never claim Jenkins ran, a poll triggered, an email arrived, or a build passed unless it was actually observed. Leave blanks for the student to fill.
4. Run local Maven commands if Java and Maven exist; report real output. If missing, say so and give instructions.
5. Do not force-push, delete user files, or change accounts without asking.
6. Keep it lightweight (the student has about 8 GB RAM). No databases, no Spring Boot.

## 4. Repository structure to create

```text
StudentRecordManagement/
├── pom.xml
├── Jenkinsfile
├── README.md
├── .gitignore
├── src/
│   ├── main/java/com/student/
│   │   ├── Main.java
│   │   ├── Student.java
│   │   └── StudentService.java
│   └── test/java/com/student/
│       └── StudentServiceTest.java
└── docs/
    ├── JENKINS_SETUP.md
    ├── PRACTICAL_REPORT.md
    └── SCREENSHOT_CHECKLIST.md
```

## 5. Application and tests

### Student.java
Fields `int id, String name, int age, String course, String email`. Constructor, getters, setters for name/age/course/email (ID is immutable), readable `toString()`.

### StudentService.java
In-memory `LinkedHashMap<Integer, Student>`.

- `boolean addStudent(Student s)`: false if `s` is null or the ID exists
- `Student getStudent(int id)`: null if missing
- `List<Student> getAllStudents()`: returns a copy
- `boolean updateStudent(int id, String name, int age, String course, String email)`: false if missing
- `boolean deleteStudent(int id)`: false if missing

### Main.java
Menu loop: 1 Add, 2 View All, 3 Search by ID, 4 Update, 5 Delete, 6 Exit. Invalid numeric input must not crash the app (re-prompt). If `Scanner` input ends (EOF), exit cleanly instead of throwing `NoSuchElementException`.

### pom.xml
- `com.student:student-record-management:1.0-SNAPSHOT`
- `maven.compiler.release` = 21, UTF-8 encoding
- `org.junit.jupiter:junit-jupiter` 5.11.4, scope test
- maven-compiler-plugin 3.13.0, maven-surefire-plugin 3.5.2, maven-jar-plugin 3.4.2 with manifest `mainClass` = `com.student.Main`
- Pin versions explicitly

### StudentServiceTest.java (minimum 8 independent tests, `@BeforeEach` creates a fresh service)
1. add student succeeds and size is 1
2. get existing student returns correct name
3. update changes name and age
4. delete existing returns true and the student is gone
5. duplicate ID rejected (second add returns false, original unchanged)
6. get missing ID returns null
7. delete missing ID returns false
8. update missing ID returns false

Optionally add: `getAllStudents` preserves insertion order; `addStudent(null)` returns false.

### .gitignore
```
target/
*.class
*.log
.idea/
.vscode/
.settings/
.classpath
.project
```

## 6. Jenkinsfile (declarative, cross-platform)

Create `Jenkinsfile` (no extension) at the repo root with this content:

```groovy
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
            mail to: 'your-email@example.com',
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
```

Notes the agent must keep:
- `timestamps()` requires the Timestamper plugin, which is part of the suggested plugins. If the student's Jenkins lacks it, delete that line.
- Stage names must stay exactly: **Checkout, Build, Test, Package, Archive Artifact**.
- `pollSCM` is the trigger. A GitHub webhook is not possible on `localhost` unless a tunnel is used, and the assignment accepts either.
- The `mail` step does nothing useful until SMTP is configured in Jenkins (Section 8, Step 9).

## 7. GitHub

Commands (the student runs these; the agent must not push without being told to):

```bash
git init
git branch -M main
git add .
git commit -m "Student Record Management with Jenkins CI"
git remote add origin https://github.com/YOUR_USERNAME/StudentRecordManagement.git
git push -u origin main
```

- **Public repo:** Jenkins can clone anonymously.
- **Private repo (shows the "credentials" requirement R4):** create a GitHub fine-grained personal access token limited to this repo with **Contents: Read-only**. In Jenkins add it as **Username with password**: username = GitHub login, password = token, ID = `github-token`.
- Never put the token in the Jenkinsfile, in the repo, or in a screenshot.

## 8. Jenkins setup (Windows 11, primary path)

Write these steps into `docs/JENKINS_SETUP.md`, in beginner-friendly numbered form.

1. **Prerequisites.** JDK 21 (Eclipse Temurin), Maven 3.9.x (set `MAVEN_HOME`, add `%MAVEN_HOME%\bin` to PATH), Git. Verify with `java -version`, `javac -version`, `mvn -version`, `git --version`.
2. **Install Jenkins LTS** with the official Windows MSI installer. Choose the JDK 21 folder as Java Home, keep port 8080.
3. **Unlock.** Open `http://localhost:8080`, paste the initial admin password from the path shown by the installer, install suggested plugins, create the admin user.
4. **Tools.** Manage Jenkins -> Tools:
   - JDK: name `JDK21`, JAVA_HOME = JDK folder (no `\bin`), auto-install off
   - Maven: name `Maven3`, MAVEN_HOME = Maven root folder (no `\bin`), auto-install off
   - Git: name `Default`, path from `where git` (for example `C:\Program Files\Git\cmd\git.exe`)
   - The Jenkins service account must be able to read these folders.
5. **Plugins check.** Pipeline, Git, GitHub, JUnit, Mailer, Credentials, Timestamper installed.
6. **Credentials.** Add `github-token` (Section 7) if the repo is private.
7. **Create the job.** New Item -> name `StudentRecord-CI` -> Pipeline -> Definition **Pipeline script from SCM** -> SCM Git -> repo URL -> credentials -> branch `*/main` -> Script Path `Jenkinsfile`.
8. **First build.** Click Build Now. Inspect Console Output, Test Result, and the archived JAR. The first run also registers the Poll SCM trigger.
9. **Email.** Manage Jenkins -> System -> E-mail Notification:
   - SMTP server `smtp.gmail.com`, use SMTP authentication, SSL on, port 465 (or TLS on 587)
   - Username = Gmail address, password = Gmail **app password** (needs 2-step verification enabled)
   - Tick "Test configuration by sending test e-mail" and confirm delivery
   - Replace `your-email@example.com` in the Jenkinsfile with the real recipient
10. **Poll SCM demo.** Edit README, commit, push, wait up to about 2 minutes, and confirm a build starts without pressing Build Now. Check **Git Polling Log** if it does not.
11. **Failure demo.** In `testAddStudent` change the expected size from `1` to `5`, commit, push. Confirm: Test stage fails, build is FAILURE, JUnit report shows the failure, failure email arrives.
12. **Restore.** Change it back to `1`, commit, push, confirm SUCCESS. **The final repo state must have all tests passing.**

Troubleshooting table to include: `mvn not recognized`, `No tool named JDK21 found` (name mismatch), `Cannot run program "sh"` (old Jenkinsfile on Windows), checkout auth failures, empty JUnit results, polling not firing, SMTP auth failure, `localhost:8080` not opening (check the Jenkins service in `services.msc`).

## 9. README.md contents

Overview, features, tech stack, project tree, build/test/run commands, sample console session, test case list, CI pipeline stages, polling behavior, email dependency on SMTP, the in-memory (non-persistent) limitation, and the Windows-vs-Ubuntu note from Section 2.

## 10. docs/PRACTICAL_REPORT.md contents

Title, name and roll number (Milind Sahu, 124A1139), Experiment 3, Aim, Problem statement, Objectives, Software required, Theory (CI, Jenkins, Maven, JUnit, Git/GitHub, Jenkinsfile, Poll SCM vs webhook), architecture diagram (text), procedure, pipeline stage explanation, test case table with *expected* results, Observations section with **blank fields** for actual build numbers, durations and screenshots, Conclusion, and 8 viva questions with short answers (for example: What is CI? Declarative vs scripted pipeline? What does `post` do? Poll SCM vs webhook? What does `mvn package` produce? Why archive artifacts? What is a Jenkins credential? Why use `junit`?).

## 11. docs/SCREENSHOT_CHECKLIST.md

The student captures these (never claimed by the agent):

- [ ] App menu and one add/search/update/delete run
- [ ] `mvn test` showing 8 tests, BUILD SUCCESS
- [ ] GitHub repo showing the source and Jenkinsfile
- [ ] Manage Jenkins -> Tools (JDK21, Maven3, Git)
- [ ] Credentials list (token hidden)
- [ ] Job config (Pipeline script from SCM)
- [ ] Green stage view (all 5 stages)
- [ ] Archived JAR on the build page
- [ ] JUnit Test Result page
- [ ] Automatic build triggered by a commit (Polling Log or "Started by an SCM change")
- [ ] Red failed build (Test stage)
- [ ] Received failure email
- [ ] Final green build after the fix

## 12. Final verification: project is complete only if all pass

**Agent runs (if tools exist) and reports real output:**

```cmd
mvn -B clean compile
mvn -B test
mvn -B package
java -jar target/student-record-management-1.0-SNAPSHOT.jar
```

Then self-check:

- [ ] R1: app has 6 working menu options; 8+ JUnit tests pass
- [ ] `target/surefire-reports/*.xml` exists and the JAR exists
- [ ] R5/R6: Jenkinsfile is declarative with the 5 exact stage names in order, using `mvn -B clean compile`, `mvn -B test`, `mvn -B package`
- [ ] R7: `junit` step is in `post { always }`
- [ ] R8: `pollSCM` trigger is present
- [ ] R9: `mail` is inside `post { failure }`
- [ ] No secrets anywhere (search for `password`, `token`, `ghp_`, `github_pat_`)
- [ ] `.gitignore` excludes `target/`
- [ ] README, JENKINS_SETUP, PRACTICAL_REPORT, SCREENSHOT_CHECKLIST all exist
- [ ] Windows-vs-Ubuntu note is present in README and report
- [ ] Tests are green in the final state

**Student does manually (agent cannot):** install Jenkins, create the GitHub repo and token, add Jenkins credentials and tools, configure SMTP, create the job, run builds, capture screenshots.

## 13. Optional: Ubuntu fallback (only if the professor requires it)

On an Ubuntu VM or free-tier cloud instance:

```bash
sudo apt update
sudo apt install -y fontconfig openjdk-21-jdk maven git
# Add the official Jenkins apt repository and key per https://www.jenkins.io/doc/book/installing/linux/
sudo apt install -y jenkins
sudo systemctl enable --now jenkins
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Then use `/usr/lib/jvm/java-21-openjdk-amd64` as JAVA_HOME and `/usr/share/maven` as MAVEN_HOME in Manage Jenkins -> Tools. **No Jenkinsfile change is needed**, because it already switches between `sh` and `bat`. On a public cloud instance, a GitHub webhook (`http://SERVER:8080/github-webhook/`) can replace Poll SCM.

## 14. Final response the agent must give

1. List of every file created or changed (relative paths)
2. Exact commands run and their real results or blockers
3. Which R1-R9 items are verified in code versus which need the student's manual Jenkins/GitHub/SMTP steps
4. Anything unverified

Begin implementation now.
