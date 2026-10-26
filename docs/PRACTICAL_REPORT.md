# Practical Report — Experiment 3: Continuous Integration with Jenkins

**Course:** DevOps Laboratory  
**Experiment No:** 3  
**Title:** Configure Jenkins and Create Continuous Integration (CI) Pipeline  
**Student Name:** Milind Sahu  
**Roll Number:** 124A1139  
**Date of Submission:** 26-10-2026  
**Environment:** Windows 11 (OS-independent pipeline; compatible with Ubuntu Linux)

---

## 1. Aim
To configure Jenkins and create a continuous integration (CI) pipeline for automated building, testing, packaging, and integration of application source code.

---

## 2. Problem Statement
A development team experiences frequent integration errors, build failures, and delivery delays due to manual build and test procedures. An automated CI pipeline is required to pull source code from version control upon new commits, compile code, execute JUnit tests, package runnable binaries, publish test metrics, and notify developers of build failures.

---

## 3. Objectives
1. Implement a modular console-based Java application (Student Record Management System).
2. Automate dependency resolution and build packaging using Apache Maven.
3. Establish a comprehensive unit test suite using JUnit 5 Jupiter.
4. Install and configure Jenkins LTS as a CI automation server on Windows 11.
5. Create a cross-platform Declarative Jenkins Pipeline (`Jenkinsfile`).
6. Configure automated SCM triggers (Poll SCM) and test result reporting (`junit`).
7. Implement automated failure alerts using Jenkins Mailer.

---

## 4. Software & Tools Required
- **Operating System:** Windows 11 (Ubuntu Linux compatible)
- **Programming Language:** Java Development Kit (JDK 21)
- **Build Automation Tool:** Apache Maven 3.9.x
- **Testing Framework:** JUnit 5.11.4
- **Version Control:** Git 2.52+ & GitHub
- **CI Server:** Jenkins LTS 2.479+
- **Browser:** Google Chrome / Edge

---

## 5. Theory & Core Concepts

### 5.1 Continuous Integration (CI)
Continuous Integration is a DevOps software development practice where developers merge code changes frequently into a central repository. Each integration is verified by an automated build and test pipeline, enabling teams to detect problems early, locate bugs easily, and reduce integration conflicts.

### 5.2 Jenkins & Declarative Pipelines
Jenkins is an open-source automation server. A Declarative Pipeline provides a structured and readable Groovy-based syntax to define CI/CD workflows as code (`Jenkinsfile`). It enforces strict structure (`pipeline`, `stages`, `steps`, `post`) for maintainability.

### 5.3 Apache Maven & JUnit 5
Maven uses a Project Object Model (`pom.xml`) to manage dependencies, execution plugins, and standardized build lifecycles (`compile`, `test`, `package`). JUnit 5 Jupiter provides assertions and annotations (`@Test`, `@BeforeEach`) to validate code logic. Surefire generates XML test reports compatible with CI reporting tools.

### 5.4 Poll SCM vs Webhooks
- **Webhooks:** Instant push notifications sent by GitHub to a public Jenkins endpoint when commits occur. Ideal for cloud/server deployments.
- **Poll SCM:** A periodic polling mechanism where Jenkins queries GitHub on a schedule (e.g., `H/2 * * * *`). Essential for private localhost environments where Jenkins cannot receive external incoming HTTP requests without tunneling.

---

## 6. Architecture & Workflow Diagram

```
+-------------------------------------------------------------------------------------------------+
|                                    CI PIPELINE WORKFLOW                                         |
+-------------------------------------------------------------------------------------------------+
|                                                                                                 |
|   Developer                GitHub                     Jenkins Automation Server                 |
|  +---------+           +------------+              +-----------------------------+              |
|  | git     |  push     | Remote     |  poll SCM    |  Stage 1: Checkout          |              |
|  | commit  | --------> | Repository | <..........> |  Stage 2: Build (compile)   |              |
|  +---------+           +------------+  every 2 min |  Stage 3: Test (JUnit 5)    |              |
|                                                    |  Stage 4: Package (.jar)    |              |
|                                                    |  Stage 5: Archive Artifact  |              |
|                                                    +-----------------------------+              |
|                                                                   |                             |
|                                                    +--------------+--------------+              |
|                                                    |                             |              |
|                                                    v                             v              |
|                                            (Always Post-Action)       (On Failure Post-Action)  |
|                                            Publish JUnit XML          Send SMTP Email Alert     |
|                                                                                                 |
+-------------------------------------------------------------------------------------------------+
```

---

## 7. Implementation Procedure

1. **Application Logic:** Created `com.student.Student` model with immutable ID and `StudentService` using `LinkedHashMap` for in-memory CRUD operations. Created `Main` with a menu loop handling input errors and EOF.
2. **Build Configuration:** Configured `pom.xml` with Java 21 release flag, JUnit 5.11.4 dependency, Maven Surefire plugin, and Maven Jar plugin with `Main-Class` manifest.
3. **Unit Tests:** Implemented 10 unit test cases in `StudentServiceTest.java`.
4. **CI Pipeline Definition:** Authored cross-platform `Jenkinsfile` specifying 5 sequential stages (`Checkout`, `Build`, `Test`, `Package`, `Archive Artifact`), `pollSCM` trigger, `junit` test reporting, and `mail` notification on failure.
5. **Jenkins Windows Configuration:** Installed Jenkins LTS as a Windows Service, configured `JDK21` and `Maven3` under Tools, created `StudentRecord-CI` pipeline job connected to GitHub.

---

## 8. Test Cases & Expected Results

| Test Case ID | Test Name | Description | Expected Result | Status |
|---|---|---|---|---|
| TC-01 | `testAddStudentSuccess` | Add a valid student object | Returns `true`, size becomes 1 | Passed |
| TC-02 | `testGetExistingStudent` | Fetch student by existing ID | Returns matching student object | Passed |
| TC-03 | `testUpdateStudentDetails` | Update name, age, course, email | Returns `true`, fields updated | Passed |
| TC-04 | `testDeleteExistingStudent` | Delete existing student ID | Returns `true`, record removed | Passed |
| TC-05 | `testRejectDuplicateStudentId` | Attempt adding duplicate ID | Returns `false`, initial record safe | Passed |
| TC-06 | `testGetMissingStudentReturnsNull` | Search non-existent ID | Returns `null` without error | Passed |
| TC-07 | `testDeleteMissingStudentReturnsFalse`| Delete non-existent ID | Returns `false` | Passed |
| TC-08 | `testUpdateMissingStudentReturnsFalse`| Update non-existent ID | Returns `false` | Passed |
| TC-09 | `testGetAllStudentsPreservesInsertionOrder`| Insert 3 students, fetch all | Returned in exact insertion order | Passed |
| TC-10 | `testAddNullStudentReturnsFalse` | Add `null` student reference | Returns `false`, storage empty | Passed |

---

## 9. Observations & Results

*(To be filled during laboratory demonstration)*

| Metric / Event | Expected Observation | Actual Observation |
|---|---|---|
| First Build Execution | Build #1 succeeds across all 5 stages | Build #: `_____` \| Duration: `_____` |
| JUnit Test Publishing | 10 tests reported in Jenkins UI | Total Tests: `_____` \| Passed: `_____` |
| Archived Artifact | `student-record-management-1.0-SNAPSHOT.jar` | Artifact Size: `_____` |
| SCM Polling Trigger | Automatic build triggered on push within 2 mins | Build #: `_____` \| Cause: SCM change |
| Failure Demonstration | Build marks FAILURE on bad assertion | Failed Stage: `_____` |
| Email Alert Received | Notification delivered to inbox | Email Received: [ ] Yes [ ] No |
| Restored Green Build | All tests green and build SUCCESS | Build #: `_____` \| Status: SUCCESS |

---

## 10. Conclusion
The Continuous Integration pipeline was successfully designed, implemented, and configured using Jenkins and Maven on Windows 11 with full Ubuntu Linux portability. The automated workflow eliminates manual compilation and packaging overhead, verifies code integrity on every commit, archives deployable JAR binaries, and notifies engineers immediately upon test failures.

---

## 11. Viva Questions & Short Answers

1. **Q: What is Continuous Integration (CI)?**  
   *A:* A software development practice where code changes are automatically compiled, tested, and integrated into a shared repository frequently.

2. **Q: What is the difference between Declarative and Scripted Pipeline?**  
   *A:* Declarative pipeline uses structured, opinionated syntax (`pipeline { stages { ... } }`) with built-in validation, whereas Scripted pipeline uses free-form Groovy syntax with less structural enforcement.

3. **Q: What is the role of the `post` block in a Jenkinsfile?**  
   *A:* It defines conditions (`always`, `success`, `failure`, `unstable`) executed after pipeline stages complete, commonly used for notifications and reporting.

4. **Q: Why was Poll SCM used instead of a GitHub Webhook in this local setup?**  
   *A:* Webhooks require Jenkins to have a publicly accessible URL, which is unavailable on `localhost` without third-party tunneling. Poll SCM allows Jenkins to poll GitHub outbound.

5. **Q: What is the purpose of archiving artifacts in Jenkins?**  
   *A:* Archiving preserves build outputs (such as executable `.jar` binaries) on the Jenkins controller so they can be downloaded, tested, or deployed without rebuilding.

6. **Q: What does `mvn clean compile` versus `mvn package` do?**  
   *A:* `mvn clean compile` deletes older build files and compiles source code into `.class` files; `mvn package` compiles, runs tests, and packages classes into a distributable JAR file.

7. **Q: Why must `allowEmptyResults: true` be set in `junit` step?**  
   *A:* If an earlier stage fails before tests run, no XML reports exist; without this flag, Jenkins would fail the build solely because no report files were found.

8. **Q: What is the significance of a Jenkins Credential ID?**  
   *A:* It provides an abstraction to access sensitive secrets (passwords, API tokens) securely without hardcoding credentials in source code.
