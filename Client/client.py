import mariadb
from datetime import date, timedelta
import platform

def readConfig(system):
    config = ['127.0.0.1', 1433, 'tickets', 'password']  # default values
    if system == "Windows":
        f = open(".\settings.conf", "r")
    elif system == "Linux":
        f = open("./settings.conf", "r")
    lines = f.readlines()
    for line in lines:
        if not line[0] == '#':
            lineSplit = line.split("=")
            if lineSplit[0] == "server_ip":
                config.append(lineSplit[1].strip())
            elif lineSplit[0] == "server_port":
                config.append(int(lineSplit[1].strip()))
            elif lineSplit[0] == "username":
                config.append(lineSplit[1].strip())
            elif lineSplit[0] == "password":
                config.append(lineSplit[1].strip())
    f.close()
    return config

def connectDB():
    try:
        conn = mariadb.connect(
            user=username,
            password=password,
            host=server_ip,
            port=server_port,
            database="ticket-system"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        exit(1)
    return conn

if platform.system() == "Windows":
    system = "Windows"
elif platform.system() == "Linux":
    system = "Linux"
else:
    print("Unknown OS")
    exit(1)

config = readConfig(system) # returns as [server_ip, server_port]
server_ip = config[0]
server_port = config[1]
username = config[2]
password = config[3]

conn = connectDB()
cursor = conn.cursor()

def printHelp():
    print("Commands:")
    print("new - create a new ticket")
    print("exit - exit the program")
    print("help - display this help message")

def createTicket(assignee, dueDate, notes):
    cursor.execute(
        "INSERT INTO Tickets (assignee, dueDate, notes) VALUES (?, ?, ?)",
        (assignee, dueDate, notes)
    )
    conn.commit()

def getTickets(id):
    cursor.execute("SELECT * FROM Tickets WHERE assignee = ?", (id,))
    return cursor.fetchall()

def getEmployees():
    cursor.execute("SELECT * FROM Employees")
    return cursor.fetchall()

def run():
    user = input("Enter your username: ")
    employees = getEmployees()
    employeeList = [[]]
    for emp in employees:
        employeeList.append([emp['id'], emp['name']])
    for emp in employeeList:
        if user == emp[1]:
            print(f"Welcome, {emp[1]}")
            currID = emp[0]
            break
    cont = True
    while cont:
        ticketList = [[]]
        print("Current tickets:")
        tickets = getTickets(currID)
        for ticket in tickets:
            ticketList.append([ticket['id'], ticket['assignee'], ticket['dueDate'], ticket['notes']])
        for ticket in ticketList:
            del ticket[1] # remove assignee for display
        for ticket in ticketList:
            print("Ticket ID:", ticket[0], "Due Date:", ticket[2], "Notes:", ticket[3])
        selection = input("Enter command: ")
        if selection == "new":
            dueDate = input("Enter due date in format (yyyy-mm-dd): ")
            notes = input("Enter ticket notes: ")
            assigned = input("Assign to yourself? (y/n): ")
            if assigned.lower() == 'y':
                createTicket(currID, dueDate, notes)
            else:
                print("Select assignee by ID:")
                for emp in employeeList:
                    print("ID:", emp['id'], "Name:", emp['name'])
                valid = False
                while not valid:
                    assigneeID = int(input("Enter assignee ID: "))
                    for emp in employeeList:
                        if assigneeID == emp['id']:
                            valid = True
                            break
                    if not valid:
                        print("Invalid ID, try again.")
                createTicket(assigneeID, dueDate, notes)
        elif selection == "exit":
            cont = False
        else:
            printHelp()

run()