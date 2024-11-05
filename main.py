# Loading Libraries
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

# Database connection function
def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="saurabh@9006",
        database="OnlineCourseManagement"
    )

# Function to display the group details screen
def display_group_details():
    # Create a black screen
    black_screen = tk.Tk()
    black_screen.title("Group Details")
    black_screen.geometry("600x420")
    black_screen.configure(bg="black")

    # White box with double lines
    white_box = tk.Frame(black_screen, bg="white", highlightbackground="black", highlightthickness=5)
    white_box.place(relx=0.5, rely=0.5, anchor="center", width=550, height=250)

    # Adding details inside the white box
    details = (
        "Group Details:\n\n"
        "Student Name: Saurabh Kumar\nUID: 24MCC20003\n"
        "Student Name: Chota Bheem\nUID: 24MCC20004\n\n"
        "Section/Group: 24MCD1-A\nSubject: PL/SQL Lab\n"
        "Project Title: Online Course Management System"
    )

    label = tk.Label(
        white_box, text=details, font=("Bookman Old Style", 12, "bold"),
        bg="white", fg="black", justify="center"
    )
    label.pack(expand=True)

    # Close the black screen and open the main menu after 4 seconds
    black_screen.after(4000, lambda: (black_screen.destroy(), display_main_menu()))

    # Run the black screen
    black_screen.mainloop()

# Function to display the main menu
def display_main_menu():
    global root
    root = tk.Tk()
    root.title("Online Course Management System")
    root.geometry("600x420")
    root.config(bg="pink")

    # Frame to hold the title in a white box
    title_frame = tk.Frame(root, bg="lightblue", highlightbackground="black", highlightthickness=2)
    title_frame.pack(pady=(20,10), fill="x", padx=20)

    # Title for the application
    title_label = tk.Label(title_frame, text="Online Course Management System", font=("Bookman Old Style", 16, "bold"), bg="lightblue")
    title_label.pack(pady=10)

    # Frame to hold the menu buttons in a white box
    menu_frame = tk.Frame(root, bg="lightblue", highlightbackground="black", highlightthickness=2)
    menu_frame.pack(pady=(10,20), fill="both", expand=True, padx=20)

     # Frame to center the buttons vertically
    button_frame = tk.Frame(menu_frame, bg="lightblue")
    button_frame.pack(expand=True)

    # Function to show available courses
    def show_courses():
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT CourseID, CourseName FROM Courses")
        courses = cursor.fetchall()
        conn.close()

        for widget in course_frame.winfo_children():
            widget.destroy()

        for course in courses:
            tk.Label(course_frame, text=f"Course ID: {course[0]} - {course[1]}", bg="white").pack()

    # Function to enroll a student
    def enroll_student():
        def submit_enrollment():
            conn = db_connection()
            cursor = conn.cursor()

            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            email = email_entry.get()
            course_id = course_id_entry.get()

            cursor.execute("INSERT INTO Students (FirstName, LastName, Email, EnrollmentDate) VALUES (%s, %s, %s, %s)",
                           (first_name, last_name, email, datetime.now().date()))
            student_id = cursor.lastrowid

            cursor.execute("INSERT INTO Enrollments (StudentID, CourseID, EnrollmentDate) VALUES (%s, %s, %s)",
                           (student_id, course_id, datetime.now().date()))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Student {first_name} enrolled in course ID {course_id} successfully!")
            enrollment_window.destroy()

        # Enrollment Form
        enrollment_window = tk.Toplevel(root)
        enrollment_window.title("Enroll Student")

        tk.Label(enrollment_window, text="First Name").pack()
        first_name_entry = tk.Entry(enrollment_window)
        first_name_entry.pack()

        tk.Label(enrollment_window, text="Last Name").pack()
        last_name_entry = tk.Entry(enrollment_window)
        last_name_entry.pack()

        tk.Label(enrollment_window, text="Email").pack()
        email_entry = tk.Entry(enrollment_window)
        email_entry.pack()

        tk.Label(enrollment_window, text="Course ID").pack()
        course_id_entry = tk.Entry(enrollment_window)
        course_id_entry.pack()

        tk.Button(enrollment_window, text="Enroll", command=submit_enrollment).pack()

    # Function to view enrollments
    def view_enrollments():
        enrollments_window = tk.Toplevel(root)
        enrollments_window.title("Enrollments")

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Students.FirstName, Students.LastName, Courses.CourseName, Enrollments.EnrollmentDate "
                       "FROM Enrollments "
                       "JOIN Students ON Enrollments.StudentID = Students.StudentID "
                       "JOIN Courses ON Enrollments.CourseID = Courses.CourseID")
        enrollments = cursor.fetchall()
        conn.close()

        for enrollment in enrollments:
            tk.Label(enrollments_window, text=f"Student: {enrollment[0]} {enrollment[1]}, Course: {enrollment[2]}, "
                                              f"Date: {enrollment[3]}").pack()

    # Buttons in the menu frame
    tk.Button(menu_frame, text="Show Courses", command=show_courses, bg="white", width=20, height=2).pack(pady=5)
    tk.Button(menu_frame, text="Enroll Student", command=enroll_student, bg="white", width=20, height=2).pack(pady=5)
    tk.Button(menu_frame, text="View Enrollments", command=view_enrollments, bg="white", width=20, height=2).pack(pady=5)

    # Frame to display courses
    course_frame = tk.Frame(menu_frame, bg="white")
    course_frame.pack(pady=20)

    # Run the main menu
    root.mainloop()

# Start by displaying the group details
display_group_details()