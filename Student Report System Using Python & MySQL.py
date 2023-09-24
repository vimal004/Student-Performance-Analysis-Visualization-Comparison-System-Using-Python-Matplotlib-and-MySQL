import mysql.connector
import matplotlib.pyplot as plt

# Initialize MySQL connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Zaq1@wsx1234",
    database="Student"
)
cursor = db_connection.cursor()

# Initialize empty lists to store student data
students = []

# Function to input student data
def input_students():
    while True:
        name = input("Enter student name (or 'q' to quit): ")
        if name.lower() == 'q':
            break
        try:
            math = [float(input(f"Enter math marks for '{name}' in Test {i + 1}: ")) for i in range(3)]
            physics = [float(input(f"Enter physics marks for '{name}' in Test {i + 1}: ")) for i in range(3)]
            chemistry = [float(input(f"Enter chemistry marks for '{name}' in Test {i + 1}: ")) for i in range(3)]
            att = float(input(f"Enter attendance percentage for '{name}': "))
            students.append({'name': name, 'math': math, 'physics': physics, 'chemistry': chemistry, 'attendance': att})
        except ValueError:
            print("Invalid input. Please enter valid data.")

# Function to display student data
def show_student_data(students):
    if not students:
        print("No student data to display.")
        return

    print("\nStudent Data:")
    for student in students:
        print(f"Name: {student['name']}")
        print(f"Math Marks: {student['math']}")
        print(f"Physics Marks: {student['physics']}")
        print(f"Chemistry Marks: {student['chemistry']}")
        print(f"Attendance: {student['attendance']}%\n")

# Function to insert student data into the database
def insert_student(student):
    sql = "INSERT INTO students (name, math1, math2, math3, physics1, physics2, physics3, chemistry1, chemistry2, chemistry3, attendance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (student['name'], student['math'][0], student['math'][1], student['math'][2], student['physics'][0], student['physics'][1], student['physics'][2], student['chemistry'][0], student['chemistry'][1], student['chemistry'][2], student['attendance'])
    cursor.execute(sql, val)
    db_connection.commit()
    print(f"Student '{student['name']}' has been inserted into the database.")

# Function to fetch student data from the database
def fetch_students():
    cursor.execute("SELECT * FROM students")
    result = cursor.fetchall()
    students = []
    for row in result:
        name = row[1]
        math = [row[2], row[3], row[4]]
        physics = [row[5], row[6], row[7]]
        chemistry = [row[8], row[9], row[10]]
        attendance = row[11]
        students.append({'name': name, 'math': math, 'physics': physics, 'chemistry': chemistry, 'attendance': attendance})
    return students

# Function to delete a student record by name
def delete_student(students):
    name = input("Enter the name of the student to delete: ")
    for student in students:
        if student['name'] == name:
            students.remove(student)
            print(f"Student '{name}' has been deleted.")
            return
    print(f"Student '{name}' not found.")

# Function to update a student record by name
def update_student(students):
    name = input("Enter the name of the student to update: ")
    for student in students:
        if student['name'] == name:
            try:
                student['math'] = [float(input(f"Enter updated math marks for '{name}' in Test {i + 1}: ")) for i in range(3)]
                student['physics'] = [float(input(f"Enter updated physics marks for '{name}' in Test {i + 1}: ")) for i in range(3)]
                student['chemistry'] = [float(input(f"Enter updated chemistry marks for '{name}' in Test {i + 1}: ")) for i in range(3)]
                student['attendance'] = float(input(f"Enter updated attendance percentage for '{name}': "))
                print(f"Student '{name}' has been updated.")
                return
            except ValueError:
                print("Invalid input. Please enter valid data.")
                return
    print(f"Student '{name}' not found.")

# Function to check if students are detained for the semester
def check_detainment(students):
    detainment_criteria = {'attendance': 75, 'marks': 50}
    detained_students = []
    
    for student in students:
        if student['attendance'] < detainment_criteria['attendance'] or min(student['math'] + student['physics'] + student['chemistry']) < detainment_criteria['marks']:
            detained_students.append(student['name'])
    
    if not detained_students:
        print("No students are detained for the semester.")
    else:
        print("Detained Students:")
        for name in detained_students:
            print(name)

# Function to calculate CGPA for students
def calculate_cgpa(students):
    if not students:
        print("No student data to calculate CGPA.")
        return
    
    cgpa_scale = {'A+': 4.0, 'A': 3.7, 'A-': 3.3, 'B+': 3.0, 'B': 2.7, 'B-': 2.3, 'C+': 2.0, 'C': 1.7, 'C-': 1.3, 'D+': 1.0, 'D': 0.7, 'F': 0.0}
    
    for student in students:
        math_cgpa = cgpa_scale['A+'] if max(student['math']) >= 90 else cgpa_scale['A'] if max(student['math']) >= 85 else cgpa_scale['A-'] if max(student['math']) >= 80 else cgpa_scale['B+'] if max(student['math']) >= 75 else cgpa_scale['B'] if max(student['math']) >= 70 else cgpa_scale['B-'] if max(student['math']) >= 65 else cgpa_scale['C+'] if max(student['math']) >= 60 else cgpa_scale['C'] if max(student['math']) >= 55 else cgpa_scale['C-'] if max(student['math']) >= 50 else cgpa_scale['D+'] if max(student['math']) >= 45 else cgpa_scale['D'] if max(student['math']) >= 40 else cgpa_scale['F']
        physics_cgpa = cgpa_scale['A+'] if max(student['physics']) >= 90 else cgpa_scale['A'] if max(student['physics']) >= 85 else cgpa_scale['A-'] if max(student['physics']) >= 80 else cgpa_scale['B+'] if max(student['physics']) >= 75 else cgpa_scale['B'] if max(student['physics']) >= 70 else cgpa_scale['B-'] if max(student['physics']) >= 65 else cgpa_scale['C+'] if max(student['physics']) >= 60 else cgpa_scale['C'] if max(student['physics']) >= 55 else cgpa_scale['C-'] if max(student['physics']) >= 50 else cgpa_scale['D+'] if max(student['physics']) >= 45 else cgpa_scale['D'] if max(student['physics']) >= 40 else cgpa_scale['F']
        chemistry_cgpa = cgpa_scale['A+'] if max(student['chemistry']) >= 90 else cgpa_scale['A'] if max(student['chemistry']) >= 85 else cgpa_scale['A-'] if max(student['chemistry']) >= 80 else cgpa_scale['B+'] if max(student['chemistry']) >= 75 else cgpa_scale['B'] if max(student['chemistry']) >= 70 else cgpa_scale['B-'] if max(student['chemistry']) >= 65 else cgpa_scale['C+'] if max(student['chemistry']) >= 60 else cgpa_scale['C'] if max(student['chemistry']) >= 55 else cgpa_scale['C-'] if max(student['chemistry']) >= 50 else cgpa_scale['D+'] if max(student['chemistry']) >= 45 else cgpa_scale['D'] if max(student['chemistry']) >= 40 else cgpa_scale['F']
        
        total_cgpa = (math_cgpa + physics_cgpa + chemistry_cgpa) / 3.0
        student['cgpa'] = total_cgpa

    print("\nStudent CGPA:")
    for student in students:
        print(f"Name: {student['name']}, CGPA: {student['cgpa']}")

# Function to compare student performance
def compare_performance(students, student_name=None):
    if not students:
        print("No student data to compare.")
        return

    if student_name:
        # Compare a specific student's performance
        for student in students:
            if student['name'] == student_name:
                subjects = ['Math', 'Physics', 'Chemistry', 'Attendance']
                marks = [max(student['math']), max(student['physics']), max(student['chemistry']), student['attendance']]

                plt.figure(figsize=(8, 5))
                plt.bar(subjects, marks, color=['blue', 'green', 'red', 'orange'])
                plt.xlabel('Subjects')
                plt.ylabel('Marks/Attendance')
                plt.title(f'Performance Comparison for {student_name}')
                plt.ylim(0, 100)  # Adjust the y-axis limits if needed
                plt.show()
                return
        print(f"Student '{student_name}' not found.")
    else:
        # Compare all students' performance
        subjects = ['Math', 'Physics', 'Chemistry', 'Attendance']
        marks = []

        for student in students:
            marks.append([student['name'], max(student['math']), max(student['physics']), max(student['chemistry']), student['attendance']])

        marks = list(zip(*marks))  # Transpose the list for plotting

        plt.figure(figsize=(12, 6))
        for i in range(1, len(subjects) + 1):
            plt.subplot(2, 2, i)
            plt.bar(marks[0], marks[i], color='skyblue')
            plt.xlabel('Students')
            plt.ylabel('Marks/Attendance')
            plt.title(f'{subjects[i-1]} Comparison')
            plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()

# Function to analyze and plot an individual student's performance in a subject
def analyze_individual_performance(student, subject):
    if subject not in ['math', 'physics', 'chemistry']:
        print(f"Invalid subject: {subject}. Subject must be 'math', 'physics', or 'chemistry'.")
        return

    subject_scores = student[subject]
    test_numbers = ['Test 1', 'Test 2', 'Test 3']

    plt.figure(figsize=(8, 5))
    plt.bar(test_numbers, subject_scores, color='skyblue')
    plt.xlabel('Tests')
    plt.ylabel('Marks')
    plt.title(f'{subject.capitalize()} Performance for {student["name"]}')
    plt.ylim(0, 100)  # Adjust the y-axis limits if needed
    plt.show()

# Main program loop
while True:
    print("\nStudent Tracker Menu:")
    print("1. Enter Student Data")
    print("2. Show Student Data")
    print("3. Delete Student Record")
    print("4. Update Student Record")
    print("5. Check Detainment")
    print("6. Calculate CGPA")
    print("7. Analyze Student Performance")
    print("8. Compare Student Performance")
    print("9. Quit")

    choice = input("Enter your choice (1/2/3/4/5/6/7/8/9): ")

    if choice == '1':
        student_data = input_students()
        insert_student(student_data)
    elif choice == '2':
        students = fetch_students()
        show_student_data(students)
    elif choice == '3':
        delete_student(students)
    elif choice == '4':
        update_student(students)
    elif choice == '5':
        check_detainment(students)
    elif choice == '6':
        calculate_cgpa(students)
    elif choice == '7':
        student_name = input("Enter student name to analyze performance: ")
        subject = input("Enter subject to analyze (math/physics/chemistry): ")
        analyze_individual_performance(student, subject)
    elif choice == '8':
        student_name = input("Enter student name to compare performance: ")
        compare_performance(students, student_name)
    elif choice == '9':
        break
    else:
        print("Invalid choice. Please select a valid option!")

# Close the database connection when done
db_connection.close()
print("Thank you for using the Student Report System!")
