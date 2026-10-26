package com.student;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for StudentService.
 * Contains 10 independent unit tests covering CRUD operations, edge cases, and ordering.
 */
public class StudentServiceTest {

    private StudentService service;

    @BeforeEach
    void setUp() {
        service = new StudentService();
    }

    @Test
    void testAddStudentSuccess() {
        Student s = new Student(101, "Alice Smith", 20, "Computer Science", "alice@example.com");
        boolean result = service.addStudent(s);

        assertTrue(result, "Adding valid student should return true");
        assertEquals(1, service.getAllStudents().size(), "Student count should be 1");
    }

    @Test
    void testGetExistingStudent() {
        Student s = new Student(102, "Bob Jones", 22, "Information Technology", "bob@example.com");
        service.addStudent(s);

        Student fetched = service.getStudent(102);
        assertNotNull(fetched, "Fetched student must not be null");
        assertEquals("Bob Jones", fetched.getName(), "Name should match added student");
        assertEquals(22, fetched.getAge(), "Age should match added student");
        assertEquals("Information Technology", fetched.getCourse(), "Course should match added student");
        assertEquals("bob@example.com", fetched.getEmail(), "Email should match added student");
    }

    @Test
    void testUpdateStudentDetails() {
        Student s = new Student(103, "Charlie Brown", 19, "Mechanical", "charlie@example.com");
        service.addStudent(s);

        boolean updated = service.updateStudent(103, "Charles Brown", 20, "Mechatronics", "charles.b@example.com");
        assertTrue(updated, "Updating existing student should return true");

        Student afterUpdate = service.getStudent(103);
        assertNotNull(afterUpdate);
        assertEquals("Charles Brown", afterUpdate.getName(), "Name should be updated");
        assertEquals(20, afterUpdate.getAge(), "Age should be updated");
        assertEquals("Mechatronics", afterUpdate.getCourse(), "Course should be updated");
        assertEquals("charles.b@example.com", afterUpdate.getEmail(), "Email should be updated");
    }

    @Test
    void testDeleteExistingStudent() {
        Student s = new Student(104, "Diana Prince", 21, "Civil", "diana@example.com");
        service.addStudent(s);

        boolean deleted = service.deleteStudent(104);
        assertTrue(deleted, "Deleting existing student should return true");
        assertNull(service.getStudent(104), "Deleted student lookup should return null");
        assertEquals(0, service.getAllStudents().size(), "Student list should be empty after deletion");
    }

    @Test
    void testRejectDuplicateStudentId() {
        Student s1 = new Student(105, "Evan Wright", 21, "Electronics", "evan@example.com");
        Student s2 = new Student(105, "Evan Clone", 25, "Physics", "clone@example.com");

        boolean firstAdd = service.addStudent(s1);
        boolean duplicateAdd = service.addStudent(s2);

        assertTrue(firstAdd, "First add should succeed");
        assertFalse(duplicateAdd, "Duplicate ID must be rejected");
        assertEquals(1, service.getAllStudents().size(), "Only one record should exist");
        assertEquals("Evan Wright", service.getStudent(105).getName(), "Original record must remain intact");
    }

    @Test
    void testGetMissingStudentReturnsNull() {
        Student s = service.getStudent(999);
        assertNull(s, "Searching non-existent ID should return null");
    }

    @Test
    void testDeleteMissingStudentReturnsFalse() {
        boolean deleted = service.deleteStudent(999);
        assertFalse(deleted, "Deleting non-existent ID should return false");
    }

    @Test
    void testUpdateMissingStudentReturnsFalse() {
        boolean updated = service.updateStudent(999, "Nobody", 30, "None", "nobody@example.com");
        assertFalse(updated, "Updating non-existent ID should return false");
    }

    @Test
    void testGetAllStudentsPreservesInsertionOrder() {
        Student s1 = new Student(201, "First", 20, "CS", "first@example.com");
        Student s2 = new Student(202, "Second", 21, "CS", "second@example.com");
        Student s3 = new Student(203, "Third", 22, "CS", "third@example.com");

        service.addStudent(s1);
        service.addStudent(s2);
        service.addStudent(s3);

        List<Student> list = service.getAllStudents();
        assertEquals(3, list.size());
        assertEquals(201, list.get(0).getId());
        assertEquals(202, list.get(1).getId());
        assertEquals(203, list.get(2).getId());
    }

    @Test
    void testAddNullStudentReturnsFalse() {
        boolean result = service.addStudent(null);
        assertFalse(result, "Adding null student should return false");
        assertEquals(0, service.getAllStudents().size(), "List must remain empty");
    }
}
