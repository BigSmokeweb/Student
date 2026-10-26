package com.student;

import java.util.List;
import java.util.Scanner;

/**
 * Interactive console interface for Student Record Management.
 */
public class Main {
    private static final StudentService service = new StudentService();

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("==================================================");
        System.out.println("       STUDENT RECORD MANAGEMENT SYSTEM           ");
        System.out.println("==================================================");

        boolean running = true;
        while (running) {
            printMenu();
            System.out.print("Enter choice (1-6): ");
            int choice = readInt(scanner);
            if (choice == -1) {
                // End of input stream reached
                System.out.println("\nInput stream ended. Exiting application.");
                break;
            }

            switch (choice) {
                case 1 -> handleAddStudent(scanner);
                case 2 -> handleViewAll();
                case 3 -> handleSearch(scanner);
                case 4 -> handleUpdate(scanner);
                case 5 -> handleDelete(scanner);
                case 6 -> {
                    System.out.println("Exiting Student Record Management. Goodbye!");
                    running = false;
                }
                default -> System.out.println("Invalid selection. Please choose an option between 1 and 6.");
            }
        }
    }

    private static void printMenu() {
        System.out.println("\n----------------- MAIN MENU -----------------");
        System.out.println("1. Add Student");
        System.out.println("2. View All Students");
        System.out.println("3. Search Student by ID");
        System.out.println("4. Update Student");
        System.out.println("5. Delete Student");
        System.out.println("6. Exit");
        System.out.println("---------------------------------------------");
    }

    private static void handleAddStudent(Scanner scanner) {
        System.out.println("\n--- Add New Student ---");
        System.out.print("Enter Student ID: ");
        int id = readInt(scanner);
        if (id == -1) return;

        if (service.getStudent(id) != null) {
            System.out.println("Error: Student with ID " + id + " already exists!");
            return;
        }

        System.out.print("Enter Name: ");
        String name = readLine(scanner);
        if (name == null) return;

        System.out.print("Enter Age: ");
        int age = readInt(scanner);
        if (age == -1) return;

        System.out.print("Enter Course: ");
        String course = readLine(scanner);
        if (course == null) return;

        System.out.print("Enter Email: ");
        String email = readLine(scanner);
        if (email == null) return;

        boolean added = service.addStudent(new Student(id, name, age, course, email));
        if (added) {
            System.out.println("Success: Student added successfully!");
        } else {
            System.out.println("Error: Failed to add student.");
        }
    }

    private static void handleViewAll() {
        System.out.println("\n--- All Student Records ---");
        List<Student> students = service.getAllStudents();
        if (students.isEmpty()) {
            System.out.println("No student records found.");
        } else {
            for (Student s : students) {
                System.out.println(s);
            }
            System.out.println("Total records: " + students.size());
        }
    }

    private static void handleSearch(Scanner scanner) {
        System.out.println("\n--- Search Student by ID ---");
        System.out.print("Enter Student ID: ");
        int id = readInt(scanner);
        if (id == -1) return;

        Student s = service.getStudent(id);
        if (s != null) {
            System.out.println("Found record: " + s);
        } else {
            System.out.println("No student found with ID: " + id);
        }
    }

    private static void handleUpdate(Scanner scanner) {
        System.out.println("\n--- Update Student ---");
        System.out.print("Enter Student ID to update: ");
        int id = readInt(scanner);
        if (id == -1) return;

        Student existing = service.getStudent(id);
        if (existing == null) {
            System.out.println("Error: No student found with ID: " + id);
            return;
        }

        System.out.println("Current details: " + existing);
        System.out.print("Enter New Name: ");
        String name = readLine(scanner);
        if (name == null) return;

        System.out.print("Enter New Age: ");
        int age = readInt(scanner);
        if (age == -1) return;

        System.out.print("Enter New Course: ");
        String course = readLine(scanner);
        if (course == null) return;

        System.out.print("Enter New Email: ");
        String email = readLine(scanner);
        if (email == null) return;

        boolean updated = service.updateStudent(id, name, age, course, email);
        if (updated) {
            System.out.println("Success: Student record updated successfully!");
        } else {
            System.out.println("Error: Failed to update student record.");
        }
    }

    private static void handleDelete(Scanner scanner) {
        System.out.println("\n--- Delete Student ---");
        System.out.print("Enter Student ID to delete: ");
        int id = readInt(scanner);
        if (id == -1) return;

        boolean deleted = service.deleteStudent(id);
        if (deleted) {
            System.out.println("Success: Student with ID " + id + " was deleted.");
        } else {
            System.out.println("Error: No student found with ID: " + id);
        }
    }

    private static int readInt(Scanner scanner) {
        while (true) {
            if (!scanner.hasNextLine()) {
                return -1;
            }
            String line = scanner.nextLine().trim();
            try {
                return Integer.parseInt(line);
            } catch (NumberFormatException e) {
                System.out.print("Invalid integer. Please enter a valid number: ");
            }
        }
    }

    private static String readLine(Scanner scanner) {
        if (!scanner.hasNextLine()) {
            return null;
        }
        return scanner.nextLine().trim();
    }
}
