# Q2

# P1: Graph Data Structure (adjacency list implementation)
class DirectedGraph:
    """Unweighted directed graph, can be reused for any kind of data"""

    def __init__(self):
        self.vertices = {} # data object stored in that vertex
        self.adjacency = {} #list of vertices it points TO (connections)

    #methods
    #key = course code
    #data = course object containing all its information
    def addVertex(self, key, data=None):
        """Add a new vertex. Returns False if the key already exists."""

        #checks if the course code exists in the graph already
        if key in self.vertices:
            return False
        #adds the course code and course info into vertices dictionary.
        self.vertices[key] = data
        #creates an empty list for the new course's connections.
        self.adjacency[key] = []
        #tells program that the course is successfully added.
        return True


    # source = course where the arrow starts
    # target = course where the arrow ends
    def addEdge(self, source, target):
        """Add a directed edge source -> target returns false if either vertex is missing."""

        #check if either course is missing from the graph
        if source not in self.vertices or target not in self.vertices:
            return False
        #check if the course is being connected to itself / connection already exists
        if source == target or target in self.adjacency[source]:
            return False
        #line that adds the connection (self.adjacency["CS101"].append("CS201"))
        self.adjacency[source].append(target)
        return True


    #finds all the prerequisite courses of a selected course.
    def listIncomingAdjacentVertex(self, key):
        """Return every vertex that has an edge pointing into key
            Only outgoing edges are stored, so every vertex's outgoing list for key is checked"""

        #creates empty list to store prerequisite courses
        incoming = []

        #goes through every course, list of connections
        # (source - course code / targets - courses that it points to)
        for source, targets in self.adjacency.items():
            if key in targets:
                incoming.append(source)
        return incoming


    # finds all the courses that a selected course unlocks
    def listOutgoingAdjacentVertex(self, key):
        """Return every vertex that 'key' points to"""

        #self.adjacency key finds the selected course's list of outgoing connections
        #list() makes a copy of the list, returns it
        return list(self.adjacency[key])


# Course Entity Class
class Course:
    """Represents a single course"""

    def __init__(self, code, name, credit_hours, level, description):
        self.code = code
        self.name = name
        self.credit_hours = credit_hours
        self.level = level #core or elective course
        self.description = description

    def full_details(self):
        """All information, regardless of level."""
        #f string allows Python to insert actual value of a variable into a sentence
        return(f"Course Code : {self.code}\n"
               f"Course Name : {self.name}\n"
               f"Credit Hours : {self.credit_hours}\n"
               f"Level        : {self.level.capitalize()}\n" #first letter is capitalized
               f"Description  : {self.description}")

#sample data
def build_sample_system():
    """Create the Course objects and connect them as prerequisites."""
    # creates new graph object using DirectedGraph class
    graph = DirectedGraph()

    courses = [
        Course("CS101", "Programming Fundamentals", 4, "core",
               "Introduction to programming using Python."),
        Course("CS102", "Discrete Mathematics", 3, "core",
               "Logic, sets, relations and graph theory basics."),
        Course("CS201", "Data Structures", 4, "core",
               "Arrays, linked lists, stacks, queues, trees and graphs."),
        Course("CS202", "Database Systems", 3, "core",
               "Relational model, SQL and database design."),
        Course("CS301", "Advanced Algorithms", 4, "core",
               "Algorithm design and complexity analysis."),
        Course("CS302", "Software Engineering", 3, "core",
               "Software development lifecycle and teamwork."),
        Course("CS303", "Artificial Intelligence", 3, "elective",
               "Search, reasoning and intelligent agents."),
        Course("CS304", "Machine Learning", 3, "elective",
               "Supervised and unsupervised learning."),
    ]

    #adds all eight course objects into the graph
    #goes through the courses list one course at a time
    for course in courses:
        #calls the addVertex() method to add course into graph
        #course.code = course code (dictionary key)
        #course = entire course object (dictionary value)
        graph.addVertex(course.code, course)

    # (prerequisite, course that requires it)
    #creates a list containing all the prerequisite relationships
    #e.g. ("CS101", "CS201") means CS101 is needed before CS201
    prerequisites = [
        ("CS101", "CS201"), ("CS101", "CS202"),
        ("CS201", "CS301"), ("CS102", "CS301"),
        ("CS201", "CS302"), ("CS202", "CS302"),
        ("CS301", "CS303"), ("CS301", "CS304"), ("CS102", "CS304"),
    ]


    #adds all the prerequisite relationships into the graph
    #goes through every pair into the prerequisites list, separates each pair into two variables
    for prereq, course in prerequisites:
        graph.addEdge(prereq, course)
    return graph

#interface

#asks user for a course code - checks if course exists
def ask_for_course(graph, prompt="Enter course code: "):
    """Ask for a course code, Returns the code, or none if it does not exist."""

    # .strip() removes unnecessary spaces at the beginning and end.
    # .upper() changes the letters to uppercase.
    code = input(prompt).strip().upper()

    #check if the entered course code exists in the graph
    if code not in graph.vertices:
        print(f" Course '{code}' not found.")
        return None
    return code

#displays a list of courses with their codes and names
#graph = gives access to the course information
#codes = The course codes to display
#empty_message = The message shown when there are no courses
def print_course_list(graph, codes, empty_message):
    """Print a list of course codes with names, or a message if empty."""
    if not codes:
        print(f" {empty_message}")
        return
    for code in codes:
        #{code:<8} makes course code left-aligned in a space of eight character
        print(f" {code:<8}{graph.vertices[code].name}")

#display every course in the graph
def display_all_courses(graph):
    print("\n--- All Courses ---")
    print_course_list(graph, graph.vertices.keys(), "No courses available.")

#displays all details of a course selected by the user
def view_course_details(graph):
    code = ask_for_course(graph)
    if code:
        print("\n--- Course Details ---")
        print(graph.vertices[code].full_details())

#display all prerequisites of a selected course
def view_prerequisites(graph):
    code = ask_for_course(graph)
    #only continues if the course code is valid
    if code:
        print(f"\n--- Prerequisites of {code} ({graph.vertices[code].name}) ---")

        ## Calls the method that finds all incoming adjacent vertices (prerequisite courses).
        print_course_list(graph, graph.listIncomingAdjacentVertex(code),
                          "No prerequisites required.")

#displays the courses that a selected course unlocked
def view_unlocked_courses(graph):
    #asks user to enter course code, check existence
    code = ask_for_course(graph)
    if code:
        print(f"\n--- Courses unlocked by {code} ({graph.vertices[code].name}) ---")
        #calls the method that finds all outgoing edges
        print_course_list(graph, graph.listOutgoingAdjacentVertex(code),
                          "This course does not unlock any course.")


# ADVANCED FEATURE

#creates a new course and adds it to the graph as a new vertex
def add_course(graph):
    """Advanced (a): add a new course (vertex) on demand."""
    #asks for the code first, so the user is not asked for details that will be rejected
    code = input("New course code: ").strip().upper()
    if code == "" or code in graph.vertices:
        print(" Course code is empty or already exists.")
        return

    name = input("Course name: ").strip()
    description = input("Description: ").strip()
    level = input("Level (core/elective): ").strip().lower()
    if name == "" or level not in ("core", "elective"):
        print(" Name cannot be empty and level must be 'core' or 'elective'.")
        return

    #int() raises ValueError if the input is not a whole number
    try:
        credit_hours = int(input("Credit hours: "))
    except ValueError:
        print(" Credit hours must be a whole number.")
        return
    if credit_hours < 1:
        print(" Credit hours must be at least 1.")
        return

    #only reached when every check has passed
    graph.addVertex(code, Course(code, name, credit_hours, level, description))
    print(f" Course {code} added.")


#MAIN MENU

#stores the menu that the user sees when running the program
MENU = """
==== University Course Prerequisite System ====
 1. Display all courses
 2. View course details (full)
 3. View prerequisites of a course
 4. View courses unlocked by a course
 --- Advanced ---
 5. Add a new course
 0. Exit"""


def main():
    graph = build_sample_system()

    #creates dictionary called actions
    #connects menu number to the function that should run when user selects it
    actions = {
        "1": display_all_courses,
        "2": view_course_details,
        "3": view_prerequisites,
        "4": view_unlocked_courses,
        "5": add_course,
    }

    #while True loop keeps menu running until user chooses to exit
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        elif choice in actions:
            #actions[choice]
            actions[choice](graph)
        else:
            print("  Invalid option. Please enter 0-5.")


if __name__ == "__main__":
    main()
