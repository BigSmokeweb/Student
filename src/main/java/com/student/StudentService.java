package com.student;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Service managing in-memory Student records using LinkedHashMap to preserve insertion order.
 */
public class StudentService {
    private final Map<Integer, Student> studentMap;

    public StudentService() {
        this.studentMap = new LinkedHashMap<>();
    }

    /**
     * Adds a new student record.
     * @param s student object
     * @return true if successfully added, false if null or ID already exists
     */
    public boolean addStudent(Student s) {
        if (s == null) {
            return false;
        }
        if (studentMap.containsKey(s.getId())) {
            return false;
        }
        studentMap.put(s.getId(), s);
        return true;
    }

    /**
     * Retrieves student by ID.
     * @param id student ID
     * @return matching Student or null if not found
     */
    public Student getStudent(int id) {
        return studentMap.get(id);
    }

    /**
     * Retrieves all students preserving insertion order.
     * @return defensive copy list of students
     */
    public List<Student> getAllStudents() {
        return new ArrayList<>(studentMap.values());
    }

    /**
     * Updates an existing student record.
     * @param id student ID (immutable)
     * @param name new name
     * @param age new age
     * @param course new course
     * @param email new email
     * @return true if updated, false if student not found
     */
    public boolean updateStudent(int id, String name, int age, String course, String email) {
        Student student = studentMap.get(id);
        if (student == null) {
            return false;
        }
        student.setName(name);
        student.setAge(age);
        student.setCourse(course);
        student.setEmail(email);
        return true;
    }

    /**
     * Deletes a student by ID.
     * @param id student ID
     * @return true if deleted, false if not found
     */
    public boolean deleteStudent(int id) {
        return studentMap.remove(id) != null;
    }
}
