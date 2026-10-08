import json
import os


# =========================
# FILE HANDLING
# =========================

STUDENTS_FILE = "students.json"
TEACHERS_FILE = "teachers.json"
COURSES_FILE = "courses.json"


def load_data(filename):
    try:
        if not os.path.exists(filename):
            with open(filename, "w") as file:
                json.dump([], file)

        with open(filename, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError) as error:
        print(f"Error loading {filename}: {error}")
        return []


def save_data(filename, data):
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    except OSError as error:
        print(f"Error saving {filename}: {error}")


# =========================
# CLASSES
# =========================

class Student:
    def __init__(self, student_id, fullname, age, email, department):
        self.student_id = student_id
        self.fullname = fullname
        self.age = age
        self.email = email
        self.department = department
        self.courses = []

    def enroll(self, course_code):
        if course_code not in self.courses:
            self.courses.append(course_code)

    def display(self):
        print("\n--- Student ---")
        print(f"ID: {self.student_id}")
        print(f"Name: {self.fullname}")
        print(f"Age: {self.age}")
        print(f"Email: {self.email}")
        print(f"Department: {self.department}")
        print(f"Courses: {', '.join(self.courses) if self.courses else 'None'}")


class Teacher:
    def __init__(self, teacher_id, fullname, email):
        self.teacher_id = teacher_id
        self.fullname = fullname
        self.email = email
        self.courses = []

    def assign_course(self, course_code):
        if course_code not in self.courses:
            self.courses.append(course_code)

    def display(self):
        print("\n--- Teacher ---")
        print(f"ID: {self.teacher_id}")
        print(f"Name: {self.fullname}")
        print(f"Email: {self.email}")
        print(f"Courses: {', '.join(self.courses) if self.courses else 'None'}")


class Course:
    def __init__(self, course_code, title, unit, teacher_id=None):
        self.course_code = course_code
        self.title = title
        self.unit = unit
        self.teacher_id = teacher_id
        self.students = []

    def add_student(self, student_id):
        if student_id not in self.students:
            self.students.append(student_id)

    def display(self):
        print("\n--- Course ---")
        print(f"Code: {self.course_code}")
        print(f"Title: {self.title}")
        print(f"Unit: {self.unit}")
        print(f"Teacher ID: {self.teacher_id or 'Not assigned'}")
        print(f"Students: {', '.join(map(str, self.students)) if self.students else 'None'}")


# =========================
# LOAD DATA
# =========================

students = load_data(STUDENTS_FILE)
teachers = load_data(TEACHERS_FILE)
courses = load_data(COURSES_FILE)


# =========================
# ID GENERATORS
# =========================

def generate_student_id():
    if not students:
        return 1

    return max(student["student_id"] for student in students) + 1


def generate_teacher_id():
    if not teachers:
        return 1

    return max(teacher["teacher_id"] for teacher in teachers) + 1


# =========================
# REGISTER STUDENT
# =========================

def register_student():
    print("\n=== Register Student ===")

    fullname = input("Full name: ").strip()

    if not fullname:
        print("Error: Name cannot be empty.")
        return

    email = input("Email: ").strip().lower()

    if not email or "@" not in email:
        print("Error: Invalid email.")
        return

    # Prevent duplicate emails
    for student in students:
        if student["email"] == email:
            print("Error: This email is already registered.")
            return

    try:
        age = int(input("Age: "))

        if age <= 0 or age > 100:
            print("Error: Invalid age.")
            return

    except ValueError:
        print("Error: Age must be a number.")
        return

    department = input("Department: ").strip()

    if not department:
        print("Error: Department cannot be empty.")
        return

    student = {
        "student_id": generate_student_id(),
        "fullname": fullname,
        "age": age,
        "email": email,
        "department": department,
        "courses": []
    }

    students.append(student)
    save_data(STUDENTS_FILE, students)

    print(f"Student registered successfully!")
    print(f"Student ID: {student['student_id']}")


# =========================
# ADD TEACHER
# =========================

def add_teacher():
    print("\n=== Add Teacher ===")

    fullname = input("Full name: ").strip()

    if not fullname:
        print("Error: Name cannot be empty.")
        return

    email = input("Email: ").strip().lower()

    if not email or "@" not in email:
        print("Error: Invalid email.")
        return

    for teacher in teachers:
        if teacher["email"] == email:
            print("Error: Email already exists.")
            return

    teacher = {
        "teacher_id": generate_teacher_id(),
        "fullname": fullname,
        "email": email,
        "courses": []
    }

    teachers.append(teacher)
    save_data(TEACHERS_FILE, teachers)

    print(f"Teacher added successfully!")
    print(f"Teacher ID: {teacher['teacher_id']}")


# =========================
# CREATE COURSE
# =========================

def create_course():
    print("\n=== Create Course ===")

    course_code = input("Course code: ").strip().upper()

    if not course_code:
        print("Error: Course code cannot be empty.")
        return

    # Prevent duplicate course codes
    for course in courses:
        if course["course_code"] == course_code:
            print("Error: Course already exists.")
            return

    title = input("Course title: ").strip()

    if not title:
        print("Error: Course title cannot be empty.")
        return

    try:
        unit = int(input("Course unit: "))

        if unit <= 0:
            print("Error: Unit must be greater than 0.")
            return

    except ValueError:
        print("Error: Unit must be a number.")
        return

    course = {
        "course_code": course_code,
        "title": title,
        "unit": unit,
        "teacher_id": None,
        "students": []
    }

    courses.append(course)
    save_data(COURSES_FILE, courses)

    print("Course created successfully!")


# =========================
# ASSIGN COURSE TO TEACHER
# =========================

def assign_course():
    print("\n=== Assign Course ===")

    try:
        teacher_id = int(input("Teacher ID: "))
    except ValueError:
        print("Invalid teacher ID.")
        return

    course_code = input("Course code: ").strip().upper()

    teacher = next(
        (teacher for teacher in teachers
         if teacher["teacher_id"] == teacher_id),
        None
    )

    course = next(
        (course for course in courses
         if course["course_code"] == course_code),
        None
    )

    if teacher is None:
        print("Teacher not found.")
        return

    if course is None:
        print("Course not found.")
        return

    course["teacher_id"] = teacher_id

    if course_code not in teacher["courses"]:
        teacher["courses"].append(course_code)

    save_data(COURSES_FILE, courses)
    save_data(TEACHERS_FILE, teachers)

    print("Course assigned successfully!")


# =========================
# ENROLL STUDENT
# =========================

def enroll_student():
    print("\n=== Enroll Student ===")

    try:
        student_id = int(input("Student ID: "))
    except ValueError:
        print("Invalid student ID.")
        return

    course_code = input("Course code: ").strip().upper()

    student = next(
        (student for student in students
         if student["student_id"] == student_id),
        None
    )

    course = next(
        (course for course in courses
         if course["course_code"] == course_code),
        None
    )

    if student is None:
        print("Student not found.")
        return

    if course is None:
        print("Course not found.")
        return

    # Prevent duplicate enrollment
    if course_code in student["courses"]:
        print("Student is already enrolled in this course.")
        return

    student["courses"].append(course_code)
    course["students"].append(student_id)

    save_data(STUDENTS_FILE, students)
    save_data(COURSES_FILE, courses)

    print("Student enrolled successfully!")


# =========================
# SEARCH STUDENT BY ID
# =========================

def search_student_by_id():
    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    for student in students:
        if student["student_id"] == student_id:
            print("\nStudent found:")
            print(student)
            return

    print("Student not found.")


# =========================
# SEARCH STUDENT BY NAME
# =========================

def search_student_by_name():
    name = input("Enter student name: ").strip().lower()

    found = False

    for student in students:
        if name in student["fullname"].lower():
            print(student)
            found = True

    if not found:
        print("No student found.")


# =========================
# SEARCH COURSE
# =========================

def search_course():
    course_code = input("Enter course code: ").strip().upper()

    for course in courses:
        if course["course_code"] == course_code:
            print("\nCourse found:")
            print(course)
            return

    print("Course not found.")


# =========================
# DISPLAY ALL STUDENTS
# =========================

def display_students():
    if not students:
        print("No students registered.")
        return

    for student in students:
        print(student)


# =========================
# DISPLAY ALL TEACHERS
# =========================

def display_teachers():
    if not teachers:
        print("No teachers registered.")
        return

    for teacher in teachers:
        print(teacher)


# =========================
# DISPLAY ALL COURSES
# =========================

def display_courses():
    if not courses:
        print("No courses created.")
        return

    for course in courses:
        print(course)


# =========================
# MAIN MENU
# =========================

def main():
    while True:

        print("\n==============================")
        print(" SCHOOL MANAGEMENT SYSTEM")
        print("==============================")

        print("1. Register Student")
        print("2. Add Teacher")
        print("3. Create Course")
        print("4. Assign Course to Teacher")
        print("5. Enroll Student")
        print("6. Search Student by ID")
        print("7. Search Student by Name")
        print("8. Search Course")
        print("9. Display Students")
        print("10. Display Teachers")
        print("11. Display Courses")
        print("0. Exit")

        choice = input("\nChoose an option: ")

        try:

            if choice == "1":
                register_student()

            elif choice == "2":
                add_teacher()

            elif choice == "3":
                create_course()

            elif choice == "4":
                assign_course()

            elif choice == "5":
                enroll_student()

            elif choice == "6":
                search_student_by_id()

            elif choice == "7":
                search_student_by_name()

            elif choice == "8":
                search_course()

            elif choice == "9":
                display_students()

            elif choice == "10":
                display_teachers()

            elif choice == "11":
                display_courses()

            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Invalid option.")

        except IndexError:
            print("Error: Index does not exist.")

        except Exception as error:
            print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()