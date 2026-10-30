# Student Record Management System with Jenkins CI

> **Student:** Milind Sahu  
> **Roll No:** 124A1139  
> **Experiment:** 3 — Continuous Integration with Jenkins  
> **Platform Note:** Jenkins was installed on Windows 11; the declarative pipeline is OS-independent (`isUnix()` switch) and also runs on Ubuntu.

---

## 1. Overview & Features

A lightweight, high-performance console application built with Java 21 and Maven. Demonstrates Continuous Integration (CI) using Jenkins, automated testing with JUnit 5, artifact archiving, and automated build triggering.

### Core Features
- **Add Student**: Enforces unique integer ID, captures name, age, course, and email.
- **View All Students**: Displays all records maintaining insertion order.
- **Search Student by ID**: Instant O(1) lookup.
- **Update Student**: Modifies student details while keeping student ID immutable.
- **Delete Student**: Removes existing student records safely.
- **Non-Persistent In-Memory Storage**: Uses `LinkedHashMap<Integer, Student>` without external database overhead. Memory resets upon application termination.

---

## 2. Technology Stack

- **Language:** Java 21
- **Build & Dependency Management:** Apache Maven 3.9.x
- **Testing Framework:** JUnit Jupiter (JUnit 5.11.4)
- **CI / Automation Engine:** Jenkins LTS (Declarative Pipeline)
- **Version Control:** Git & GitHub

---

## 3. Project Structure

```text
StudentRecordManagement/
├── pom.xml                                     # Maven build definition & dependencies
├── Jenkinsfile                                 # Cross-platform Declarative CI Pipeline
├── README.md                                   # Project documentation
├── .gitignore                                  # Git exclusion list
├── src/
│   ├── main/java/com/student/
│   │   ├── Main.java                           # Console interactive entry point
│   │   ├── Student.java                        # Model entity (immutable ID)
│   │   └── StudentService.java                 # In-memory CRUD business logic
│   └── test/java/com/student/
│       └── StudentServiceTest.java             # 10 JUnit 5 unit tests
└── docs/
    ├── JENKINS_SETUP.md                        # Windows 11 Jenkins step-by-step setup
    ├── PRACTICAL_REPORT.md                     # Experiment report with theory & viva Q&A
    └── SCREENSHOT_CHECKLIST.md                 # Student checklist for screenshots
```

---

## 4. Local Build, Test, and Execution

From the project root directory:

### 1. Compile source code
```cmd
mvn clean compile
```

### 2. Execute JUnit 5 tests
```cmd
mvn test
```
*Surefire reports generated under `target/surefire-reports/`.*

### 3. Package runnable JAR
```cmd
mvn package
```
*Builds `target/student-record-management-1.0-SNAPSHOT.jar`.*

### 4. Run the application
```cmd
java -jar target/student-record-management-1.0-SNAPSHOT.jar
```

---

## 5. Sample Console Session

```text
==================================================
       STUDENT RECORD MANAGEMENT SYSTEM           
==================================================

----------------- MAIN MENU -----------------
1. Add Student
2. View All Students
3. Search Student by ID
4. Update Student
5. Delete Student
6. Exit
---------------------------------------------
Enter choice (1-6): 1

--- Add New Student ---
Enter Student ID: 101
Enter Name: Milind Sahu
Enter Age: 21
Enter Course: Computer Science
Enter Email: milind@example.com
Success: Student added successfully!

Enter choice (1-6): 2

--- All Student Records ---
Student [ID: 101 | Name: Milind Sahu | Age: 21 | Course: Computer Science | Email: milind@example.com]
Total records: 1

Enter choice (1-6): 6
Exiting Student Record Management. Goodbye!
```

---

## 6. Unit Test Suite (`StudentServiceTest.java`)

10 independent unit tests running against a clean `@BeforeEach` instance:
1. `testAddStudentSuccess`: Verifies adding a valid student record.
2. `testGetExistingStudent`: Verifies retrieving matching student details.
3. `testUpdateStudentDetails`: Verifies updating name, age, course, and email.
4. `testDeleteExistingStudent`: Verifies deletion and removal from storage.
5. `testRejectDuplicateStudentId`: Ensures duplicate ID cannot overwrite existing record.
6. `testGetMissingStudentReturnsNull`: Confirms non-existent ID lookup returns `null`.
7. `testDeleteMissingStudentReturnsFalse`: Confirms deleting missing ID returns `false`.
8. `testUpdateMissingStudentReturnsFalse`: Confirms updating missing ID returns `false`.
9. `testGetAllStudentsPreservesInsertionOrder`: Confirms `LinkedHashMap` order guarantee.
10. `testAddNullStudentReturnsFalse`: Confirms graceful rejection of `null` student object.

---

## 7. CI Pipeline Workflow (`Jenkinsfile`)

```
+------------+     +-----------+     +----------+     +-------------+     +--------------------+
|  Checkout  | --> |   Build   | --> |   Test   | --> |   Package   | --> |  Archive Artifact  |
+------------+     +-----------+     +----------+     +-------------+     +--------------------+
                                                             |
                                                             v
                                                  +--------------------+
                                                  | JUnit Test Publish | (always)
                                                  +--------------------+
                                                  | Email Notification | (on failure)
                                                  +--------------------+
```

- **Stages:** Checkout, Build (`mvn -B clean compile`), Test (`mvn -B test`), Package (`mvn -B package`), Archive Artifact (`target/*.jar`).
- **SCM Trigger:** Poll SCM (`H/2 * * * *`) checks repository every ~2 minutes for automatic builds.
- **Reporting:** Publishes `target/surefire-reports/*.xml` after every build.
- **Email:** Dispatches notification via Jenkins Mailer plugin on build failure (requires Jenkins SMTP configuration).

---

## 8. Platform Notice: Windows & Ubuntu Compatibility

- Primary implementation and testing environment: **Windows 11** using native Windows service.
- The pipeline script dynamically selects `bat` on Windows and `sh` on Linux using Groovy `isUnix()`.
- To run on Ubuntu Linux, follow the commands in [JENKINS_SETUP.md](file:///c:/Users/Milind/Downloads/StudentRecordManagement/docs/JENKINS_SETUP.md) (Section 10).


Built By Milind Sahu
