# Student Result Processing Portal


# Student class
class Student:
    def __init__(self, student_id, name, password):
        self.student_id = student_id
        self.name = name
        self.password = password
        self.courses = []

    # Register for a course
    def register_course(self, course):
        if course.course_code in self.courses:
            print("You have already registered for this course.")
            return False

        self.courses.append(course.course_code)
        print("Course registered successfully.")
        return True


# Lecturer class
class Lecturer:
    def __init__(self, lecturer_id, name):
        self.lecturer_id = lecturer_id
        self.name = name


# Course class
class Course:
    def __init__(self, course_code, course_name, units, lecturer):
        self.course_code = course_code
        self.course_name = course_name
        self.units = units
        self.lecturer = lecturer


# Result class
class Result:
    def __init__(self, student_id, course_code, score):
        self.student_id = student_id
        self.course_code = course_code
        self.score = score

    # Get grade point
    def get_grade_point(self):
        if self.score >= 70:
            return 5
        elif self.score >= 60:
            return 4
        elif self.score >= 50:
            return 3
        elif self.score >= 45:
            return 2
        elif self.score >= 40:
            return 1
        else:
            return 0

    # Get grade
    def get_grade(self):
        if self.score >= 70:
            return "A"
        elif self.score >= 60:
            return "B"
        elif self.score >= 50:
            return "C"
        elif self.score >= 45:
            return "D"
        elif self.score >= 40:
            return "E"
        else:
            return "F"


# Student Result Portal
class ResultPortal:

    def __init__(self):
        self.students = {}
        self.lecturers = {}
        self.courses = {}
        self.results = []

    # Add student
    def add_student(self, student):
        self.students[student.student_id] = student

    # Add lecturer
    def add_lecturer(self, lecturer):
        self.lecturers[lecturer.lecturer_id] = lecturer

    # Add course
    def add_course(self, course):
        self.courses[course.course_code] = course

    # Student login
    def student_login(self):
        student_id = input("Enter student ID: ")
        password = input("Enter password: ")

        if student_id not in self.students:
            print("Student not found.")
            return None

        student = self.students[student_id]

        if student.password == password:
            print("Login successful.")
            print("Session created.")
            return student

        print("Invalid password.")
        return None

    # Register student for course
    def register_course(self, student):
        course_code = input("Enter course code: ")

        if course_code not in self.courses:
            print("Course not found.")
            return

        course = self.courses[course_code]

        student.register_course(course)

    # Add result
    def add_result(self):
        student_id = input("Enter student ID: ")
        course_code = input("Enter course code: ")

        if student_id not in self.students:
            print("Student not found.")
            return

        if course_code not in self.courses:
            print("Course not found.")
            return

        try:
            score = float(input("Enter score: "))
        except ValueError:
            print("Invalid score.")
            return

        # Validate score
        if score < 0 or score > 100:
            print("Score must be between 0 and 100.")
            return

        # Check if result already exists
        for result in self.results:
            if result.student_id == student_id and result.course_code == course_code:
                print("Result already exists.")
                return

        result = Result(
            student_id,
            course_code,
            score
        )

        self.results.append(result)

        print("Result added successfully.")

    # Edit result
    def edit_result(self):
        student_id = input("Enter student ID: ")
        course_code = input("Enter course code: ")

        for result in self.results:

            if result.student_id == student_id and result.course_code == course_code:

                try:
                    new_score = float(input("Enter new score: "))
                except ValueError:
                    print("Invalid score.")
                    return

                if new_score < 0 or new_score > 100:
                    print("Score must be between 0 and 100.")
                    return

                result.score = new_score

                print("Result updated successfully.")
                return

        print("Result not found.")

    # Delete result
    def delete_result(self):
        student_id = input("Enter student ID: ")
        course_code = input("Enter course code: ")

        for result in self.results:

            if result.student_id == student_id and result.course_code == course_code:

                self.results.remove(result)

                print("Result deleted successfully.")
                return

        print("Result not found.")

    # View student results
    def view_results(self, student):

        total_points = 0
        total_units = 0

        print("\n===== STUDENT RESULT =====")
        print("Student:", student.name)
        print("Student ID:", student.student_id)

        found = False

        for result in self.results:

            if result.student_id == student.student_id:

                found = True

                course = self.courses[result.course_code]

                grade_point = result.get_grade_point()
                grade = result.get_grade()

                quality_point = grade_point * course.units

                total_points += quality_point
                total_units += course.units

                print("\nCourse:", course.course_name)
                print("Course Code:", course.course_code)
                print("Units:", course.units)
                print("Score:", result.score)
                print("Grade:", grade)
                print("Grade Point:", grade_point)

        if not found:
            print("No result found.")
            return

        # Calculate GPA
        gpa = total_points / total_units

        print("\nTotal Units:", total_units)
        print("GPA:", round(gpa, 2))


# Create portal
portal = ResultPortal()


# Create lecturers
lecturer1 = Lecturer(
    "L001",
    "Mr. Ade"
)

lecturer2 = Lecturer(
    "L002",
    "Mrs. Grace"
)

portal.add_lecturer(lecturer1)
portal.add_lecturer(lecturer2)


# Create students
student1 = Student(
    "S001",
    "John",
    "1234"
)

student2 = Student(
    "S002",
    "Mary",
    "5678"
)

portal.add_student(student1)
portal.add_student(student2)


# Create courses
course1 = Course(
    "CSC101",
    "Introduction to Computing",
    3,
    lecturer1
)

course2 = Course(
    "STA101",
    "Statistics",
    3,
    lecturer2
)

course3 = Course(
    "MTH101",
    "Mathematics",
    2,
    lecturer1
)

portal.add_course(course1)
portal.add_course(course2)
portal.add_course(course3)


# Main program
while True:

    print("\n===== STUDENT RESULT PORTAL =====")
    print("1. Student Login")
    print("2. Register Course")
    print("3. Add Result")
    print("4. Edit Result")
    print("5. Delete Result")
    print("6. View Student Result")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        student = portal.student_login()

        if student is not None:
            print("Welcome", student.name)

    elif choice == "2":

        student = portal.student_login()

        if student is not None:
            portal.register_course(student)

    elif choice == "3":

        portal.add_result()

    elif choice == "4":

        portal.edit_result()

    elif choice == "5":

        portal.delete_result()

    elif choice == "6":

        student = portal.student_login()

        if student is not None:
            portal.view_results(student)

    elif choice == "7":

        print("Thank you for using the Student Result Portal.")
        break

    else:

        print("Invalid choice.")