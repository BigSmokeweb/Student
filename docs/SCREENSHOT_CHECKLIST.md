# Student Screenshot Checklist

> **Student:** Milind Sahu | **Roll No:** 124A1139 | **Experiment:** 3  
> **Instructions:** Capture these screenshots during your live demonstration for your practical submission. The coding agent cannot fabricate these images.

---

## Required Submission Screenshots

- [ ] **1. Java Application Running:**  
  Console window showing the Main Menu and successful execution of Option 1 (Add Student) and Option 2 (View All Students).

- [ ] **2. Local Maven Test Run:**  
  Terminal window running `mvn test` showing 10 tests passed with `BUILD SUCCESS`.

- [ ] **3. GitHub Repository:**  
  Browser screenshot of the GitHub repository page (`StudentRecordManagement`) showing files, recent commit, and `Jenkinsfile`.

- [ ] **4. Jenkins Tools Configuration:**  
  **Manage Jenkins** -> **Tools** page displaying configured `JDK21` and `Maven3` tool names and paths.

- [ ] **5. Jenkins Credentials (if private repo):**  
  **Manage Jenkins** -> **Credentials** listing `github-token` (ensure token value remains masked).

- [ ] **6. Jenkins Job Configuration:**  
  `StudentRecord-CI` job settings showing Pipeline definition set to **Pipeline script from SCM**, Git repository URL, and script path `Jenkinsfile`.

- [ ] **7. Green Pipeline Stage View:**  
  Jenkins job dashboard displaying all 5 stages in green: `Checkout`, `Build`, `Test`, `Package`, `Archive Artifact`.

- [ ] **8. Archived Artifact:**  
  Jenkins build summary page showing `student-record-management-1.0-SNAPSHOT.jar` under **Build Artifacts**.

- [ ] **9. Published JUnit Test Results:**  
  Jenkins **Test Result** page showing 10 passing tests with test duration details.

- [ ] **10. SCM Polling Automatic Build:**  
  Build summary or **Git Polling Log** showing build triggered automatically with: *"Started by an SCM change"*.

- [ ] **11. Intentional Build Failure:**  
  Jenkins stage view showing failed `Test` stage in RED after deliberate test failure commit.

- [ ] **12. Email Failure Notification:**  
  Email client inbox showing email alert received with subject *"Jenkins Build Failed: StudentRecord-CI #..."*.

- [ ] **13. Restored Passing Build:**  
  Final build showing status restored to green **SUCCESS** after reverting test assertion.
