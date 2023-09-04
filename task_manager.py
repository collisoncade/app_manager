'''
>>> Welcome to Task Manager

This is a program designed for a small business to help to manage tasks assigned to each member of a team.

All output that this program provides to the user is easy to read and understand.
With this program you can:
  - register new users,
  - view tasks assigned to loged in user,
  - view all tasks,
  - mark tasks as complete or edit them,
  - with admin rights it lets you display statistics, delete existing users and generate reports
All usernames, passwords and tasks are stored in txt files, as well as user overview and task overview reports if they have been generated.

Use the following username and password to access the ADMIN rights:
... Username:   admin
... Password:   password
'''

#==================== Imports ====================
import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

#==================== Global variables ====================
date_format = "%d/%m/%Y" # Input: 01/12/2023
date_format_output = "%d %b %Y" # Output: 1st Jan 2023
line = "-"
line_width = 65
line_width_menu = 32
press_enter_message = "Press 'Enter' to return to the main menu..."
current_user = None

#==================== Global File Paths ====================
script_directory = os.path.dirname(os.path.abspath(__file__))
user_file_path = os.path.join(script_directory, "user.txt")
tasks_file_path = os.path.join(script_directory, "tasks.txt")
task_overview_file_path = os.path.join(script_directory, "task_overview.txt")
user_overview_file_path = os.path.join(script_directory, "task_overview.txt")


# Displays the current option/screen user currently is in
def print_screen_name(screen_name):
    """
    Clears the screen and prints the current option/screen user currently is in at the top of the screen.

    Arguments:
        screen_name (str): The current screen name stored in each function that represents a specific feature/option of the program.
    """

    clear_screen()
    # Display menu option user currently is in
    print(line * (15 + len(screen_name)))
    print(f"Task Manager > {screen_name}")
    print(line * (15 + len(screen_name)))
    print()

# Prints welcome message
def print_welcome_message():
    """
    Prints a welcome message to the console.
    """
    
    clear_screen()
    print(line * line_width_menu)
    print(">>>       Task Manager       <<<")
    print(line * line_width_menu)

# Clears the console screen
def clear_screen():
    """
    Clears the console screen.
    """

    os.system("cls" if os.name == "nt" else "clear")

# Prompts the user to log in
def login():
    """
    Prompts the user to enter their username and password.

    Returns:
        current_user (str): The current username logged in as a string.
    """
    
    # Declare current_user as a global variable
    global current_user 

    users = load_users()
    
    clear_screen()

    print_welcome_message()
    
    print("\nEnter username and password to log in.")
    while current_user is None:
        current_user = input("Username: ").lower()

        # Check if input is empty after stripping whitespace
        if len(current_user.strip()) == 0: 
            print("You didn't enter anything. Try again.")
            current_user = None  # Reset the current_user back to None
            continue
        # Check if entered user exists in register
        elif current_user not in users:
            print(f"Username '{current_user}' does not exist. Try again.")
            current_user = None  # Reset the current_user variable
            continue

        current_password = input("Password: ")

        # Check if password is correct
        if not verify_password(users, current_user.lower(), current_password):
            print("Wrong password.")
            current_user = None
        else:
            input(f"\nWelcome {current_user.upper()}, press 'Enter' to continue...")
            return current_user

# Logs out the current user
def logout():
    """
    Logs out the current user and returns to the login screen.
    """
    
    global current_user
    
    # Set current user to 'None' and return to the login screen
    current_user = None
    login()

# Create 'user.txt' file if it doesn't exist
def create_user_file():
    """
    Creates a 'user.txt' file if it doesn't exist.

    This function checks if the 'user.txt' file exists in the current directory.
    If the file does not exist, it informs the user and provides an option to continue with a blank file or exit.
    If the user chooses to continue, a new 'user.txt' file is created with a default admin user only.
    """
    
    print_welcome_message()

    if not os.path.isfile(user_file_path):
        print("\nError: 'user.txt' file was not found.")
        print("\nTo access register with existing users, make sure 'user.txt' file is located in same directory as task_manager.py.")
        
        # Promt user to continue with creating new file or exit
        user_file_choice = input("\nPress 'Enter' to continue and create new 'user.txt' file with ADMIN as only user or enter 'e' to exit: ")
        
        if user_file_choice.lower() == 'e':
            print("Good Bye!")
            exit()
        else:
            with open(user_file_path, "w") as default_file:
                default_file.write("admin;password")
                clear_screen()

                print_welcome_message()
                print("\nNew users will now be stored in created new `user.txt` file.")
                print("Be aware that Task Manager has now no records of previous users that were stored in file.")
                print("Contact ADMIN to register you as new user or login as ADMIN.")
                input("Press 'Enter' to continue...")
                clear_screen()

# Creates a 'tasks.txt' file if it doesn't exist                
def create_tasks_file():
    """
    Creates a 'tasks.txt' file if it doesn't exist.

    This function checks if the 'tasks.txt' file exists in the current directory.
    If the file does not exist, it informs the user and provides an option to continue with a new blank file or exit.
    """

    print_welcome_message()

    if not os.path.isfile(tasks_file_path):
        print("\nError: 'tasks.txt' file was not found.")
        print("\nTo access existing tasks, make sure 'tasks.txt' file is located in same directory as 'task_manager.py'.")
        
        # Promt user to continue with creating new file or exit
        tasks_file_choice = input("\nPress 'Enter' to continue and create new 'tasks.txt' file or enter 'e' to exit: ")
        
        if tasks_file_choice.lower() == 'e':
            print("Good Bye!")
            exit()
        else:
            with open(tasks_file_path, "w") as default_file:
                clear_screen()

                print_welcome_message()
                print("\nNew tasks added will now be stored in created new 'tasks.txt' file.")
                print("Be aware that Task Manager has now no records of previous tasks that were stored in file.")
                input("Press 'Enter' to continue...")
                clear_screen()

# Returns a dictionary of all users
def load_users():
    """
    Loads all users from the 'user.txt' file into a dictionary.

    Returns:
        users (dict): A dictionary containing the usernames and passwords of all registered users.
    """

    users = {}
    with open(user_file_path, "r") as user_file:
        for line in user_file:
            username, password = line.strip().split(";")
            users[username.lower()] = password
    return users

# Presents main menu to and prompts to choose from provided options
def main_menu():
    """
    Presents the main menu to the user and prompts them to choose from the provided options.

    Returns:
        menu_choice (str): The user's choice from the menu options as a string.
    """
    
    regular_menu = {
        'r': 'Register User',
        'a': 'Add Task',
        'va': 'View All Tasks',
        'vm': 'View My Tasks',
        'cp': 'Change Password',
        'l': 'Log Out',
        'e': 'Exit'
    }
    
    admin_menu = {
        'gr': 'Generate Reports',
        'ds': 'Display Statistics',
        'du': 'Delete User'
    }
    
    # Clear the console whenever main_menu() function is called
    clear_screen()

    print_welcome_message()
    print(f"Login: {current_user.upper()}")
    print(line * line_width_menu)
    print("Main menu:")

    for option, description in regular_menu.items():
        print(f"{option.ljust(2)} - {description}")

    # Display options for the ADMIN user
    if current_user == 'admin':
        print("\nAdmin options:")
        for option, description in admin_menu.items():
            print(f"{option.ljust(2)} - {description}")
    
    print(line * line_width_menu)
    menu_choice = input("Select an option: ").lower()
    return menu_choice

# Register a new user
def register_user():
    """
    Allows an existing user to register a new user by providing a username and password.
    
    Writes the username and password to the 'user.txt' file.
    """
    
    users = load_users()
    current_password = None

    # Clear the screen and display menu option user currently is in
    print_screen_name("Register User")

    # Display username requirements, promt the user to enter the username for new user and perform checks
    new_username = verify_new_username(users)

    # Display password requirements, prompt the user to enter the new password, and perform checks
    new_password = verify_new_password(current_password)

    # Add the new user to the users list
    users[new_username.lower()] = new_password

    # Write the new user information to the 'user.txt' file
    write_users(users)

    # Print a confirmation message
    print(f"\nNew user '{new_username.upper()}' has been registered.")
    input(f"\n{press_enter_message}")

# Deletes the user
def delete_user():
    """
    Prompts the user to enter a username and confirm deletion of the user.
    If confirmed, deletes the user from the users dictionary and writes the updated users to the 'user.txt' file.

    This function allows the user to delete a user from the user register. The user is prompted to enter a username,
    and if the username exists, they are asked to confirm the deletion. If confirmed, the user is deleted from the
    register and the changes are saved to the 'user.txt' file.
    """

    users = load_users()

    # Clear the screen and display menu option user currently is in
    print_screen_name("Delete User")

    # Prompt user to enter username to delete
    username = input("Enter the username to delete: ").lower()

    if username == 'admin':
        print("\nYou cannot delete the ADMIN user. Only regular users can be deleted.")
        input(f"\n{press_enter_message}")
        return

    if username not in users:
        input(f"\nUser '{username}' does not exist. {press_enter_message}")
        return

    # Prompt user for confirmation
    confirm = input("\nAre you sure you want to delete this user? (Y/N): ")
    if confirm.lower() == 'y':
        del users[username]
        write_users(users)
        input(f"\nUser '{username}' has been deleted. {press_enter_message}")
    else:
        input(f"\nDeletion aborted. {press_enter_message}")

# Adds a new task and writes it to the 'tasks.txt' file
def add_task():
    """
    Allows the user to add a new task and write it to the 'tasks.txt' file.
    
    Prompts the user for the following information:
        - Username of the person to whom the task is assigned
        - Title of the task (between 5 and 30 characters)
        - Description of the task (between 5 and 1000 characters)
        - Due date of the task (same as today or up to 18 months in the future)
    """
    
    task_list = load_tasks()
    users = load_users()

    # Clear the screen and display menu option user currently is in
    print_screen_name("Add Task")

    while True:
        # Prompt user to enter username of person the task is assigned to
        task_username = input("Enter username of assignee or enter '-1' to return to the main menu: ")

        if task_username == '-1':
            return
        
        if len(task_username) == 0 or task_username.isspace():
            print("\nYou didn't enter anything. Try again.")
            continue

        if task_username.lower() not in users:
            print(f"\nUsername '{task_username}' does not exist. Please enter a valid username.")
            continue

        # Prompt user to enter task title and perform checks
        while True:
            task_title = input("Enter title for the task: ")

            if len(task_title) == 0 or task_title.isspace():
                print("\nTitle cannot be empty.")
                continue

            if len(task_title) < 5 or len(task_title) > 30:
                print("\nTitle must be 5 to 30 characters.")
                continue
            
            break
        
        while True:
            # Prompt user to enter task description and perform checks
            task_description = input("Enter description of the task: ")

            if len(task_description) < 5 or task_description.isspace():
                print("\nInput too short. Description should be at least 5 characters long.")
                continue
            elif len(task_description) > 1000:
                print("\nInput too long. Description cannot exceed 1000 characters.")
                continue
            
            break

        # Prompt user to enter task due date and perform checks
        while True:
            try:
                task_due_date = input("Due date of the task (DD/MM/YYYY): ")
                due_date_time = datetime.strptime(task_due_date, date_format)
                # Convert due_date_time and compare with date range  
                if due_date_time < datetime.combine(date.today(), datetime.min.time()) or due_date_time > datetime.combine(date.today() + relativedelta(months=18), datetime.max.time()):
                    print("\nInvalid due date. Due date must be same as today or up to 18 months in the future.")
                    continue

                break
            except ValueError:
                print("\nInvalid date format. Please use the specified format (e.g., 01/12/2023 for 1st December 2023).")

        # Get today's date
        current_date = date.today()

        # Add the data to the tasks list
        new_task = {
            'assigned_to': task_username,
            'assigned_by': current_user,
            'task_title': task_title,
            'task_description': task_description,
            'due_date': due_date_time,
            'date_assigned': current_date,
            'task_status': False
        }

        # Add the created task to the task list
        task_list.append(new_task)

        # Update the tasks in the 'tasks.txt' file
        update_tasks_file(task_list)

        print(f"\nTask '{task_title}' successfully assigned to user '{task_username.upper()}'.")
        choice = input("\nPress 'Enter' to add another task or enter '-1' to return to the main menu...")

        if choice == '-1':
            return

# Allows user to edit task assigned to them or mark it as complete
def edit_task(filter_choice):
    """
    Allows the user to select a task assigned to them to edit or mark as complete.

    This function loads the user information, task list, and current user tasks.
    It prompts the user to choose a task by entering its number, and then presents options to mark the task as complete or edit its details.
    The function performs the chosen action and updates the task list accordingly.
    """

    users = load_users()
    task_list = load_tasks()
    # Load filtered tasks without selected filter name
    filtered_tasks, _ = load_filtered_tasks(filter_choice)

    while True:
        # Check if there are any tasks in filtered task list
        if len(filtered_tasks) == 0:
            user_choice = input("\nThere are no tasks assigned to you with the selected filter.\nEnter '-1' to return to the main menu or press 'Enter' to return to filter options: ")
            if user_choice == '-1':
                return  # Return to main menu
            else:
                clear_screen()
                break # Return to filter options
        
        # Promt user to select task from displayed tasks
        task_choice = input("\nEnter the number of the task you want to edit or mark as complete\n(enter '-1' to return to the main menu or press 'Enter' to filter tasks): ")

        # Return to main menu
        if task_choice == '-1':
            return

        # Perform checks on task choice input
        if task_choice.isdigit() and int(task_choice) > 0 and int(task_choice) <= len(filtered_tasks):
            task_index = int(task_choice) - 1
            selected_task = filtered_tasks[task_index]
            
            # Print the relevant message if task is already completed and promt user to select another task
            if selected_task['task_status']:
                print("\nSelected task has already been completed and cannot be edited. Select another task.")
                continue 
            
            while True:
                # Prompt user to mark task as complete or edit the task
                action_choice = input(f"\nEnter '1' to mark the task {task_choice} as complete or '2' to edit the task: ")

                # Mark selected task as complete and return to filter options
                if action_choice == '1':
                    # Mark selected task as complete
                    selected_task['task_status'] = True
                    # Update the task in the 'task_list' by finding its index
                    for i, task in enumerate(task_list):
                        if task['task_title'] == selected_task['task_title'] and task['assigned_by'] == selected_task['assigned_by']:
                            task_list[i] = selected_task
                            break
                    # Write the updated 'task_list' to 'tasks.txt' file
                    update_tasks_file(task_list)

                    print(f"\nTask marked as complete!")
                    input(press_enter_message)
                    return
                # Edit selected task
                elif action_choice == '2':
                    while True:
                        # Prompt user to assign task to someone else or leave it unchanged
                        new_assignee = input(f"\nEnter username of the assignee for task {task_choice} or press 'Enter' to leave it unchanged: ").lower()
                        # If 'Enter' leave assignee unchanged and continue to next promt
                        if new_assignee == '':
                            break
                        # Check if entered new asignee is an existing user
                        elif new_assignee not in users:
                            print(f"\nUsername '{new_assignee}' does not exist. Please enter a valid username.")
                        else:
                            # Update the new assignee for the task and continue to next promt
                            selected_task['assigned_to'] = new_assignee
                            selected_task['assigned_by'] = current_user
                            break

                    while True:
                        # Prompt user to change due date or leave it unchanged
                        new_due_date = input("\nEnter the new due date for the task (DD/MM/YYYY) or press 'Enter' to leave it unchanged: ")
                        # If 'Enter' leave due date unchanged
                        if len(new_due_date) == 0:
                            break
                        try:
                            # Perform check on date format
                            new_due_date_time = datetime.strptime(new_due_date, date_format)
                            # Perform check on due date range
                            if new_due_date_time < datetime.combine(date.today(), datetime.min.time()) or new_due_date_time > datetime.combine(date.today() + relativedelta(months=18), datetime.max.time()):
                                print("\nInvalid due date. Due date must be the same as today or up to 18 months in the future.")
                                continue
                            selected_task['due_date'] = new_due_date_time
                            break
                        except ValueError:
                            print("\nInvalid date format. Please use the format specified (for example: 01/12/2023 for 1st December 2023).")
                            continue

                    # Update the task in the 'task_list' by finding its index
                    for i, task in enumerate(task_list):
                        if task['task_title'] == selected_task['task_title'] and task['assigned_by'] == selected_task['assigned_by']:
                            task_list[i] = selected_task
                            break

                    # Write the updated 'task_list' to 'tasks.txt' file
                    update_tasks_file(task_list)
                    
                    print("\nTask updated.")
                    input(f"{press_enter_message}")
                    clear_screen()
                    return  # Return to main menu
                
                # Return to task selection
                else:
                    print("\nInvalid input. Try again.")
        
        # Return to filter options if selected task is not a valid input
        else:
            clear_screen()
            break

    view_mine()

# Displays the tasks assigned to the current user
def view_mine():
    """
    Displays the tasks assigned to the current user and allows them to edit or mark tasks as complete.
    Only tasks assigned to the current user are shown.

    The function first prompts the user to choose filtering option for the tasks. The available options are:
        1 - Incomplete tasks
        2 - Completed tasks
        3 - Overdue tasks
        4 - Tasks assigned by users that no longer exist

    If any other input is provided, all tasks assigned to the current user are displayed.

    Information displayed for each task:
        - Task title
        - Assigned by user
        - [deleted user] label next to assigned by if assigned by user is not in register
        - Date assigned
        - Due date
        - [due in days] if task is not completed and not overdue
        - [-days overdue] if task in not completed and overdue
        - Task completion status (Yes or No)
        - Task description

    The function also allows the user to select a task to edit or mark as complete using the edit_task() function.
    """
    
    # Load a list of all tasks
    task_list = load_tasks()
    # List with current user tasks only
    current_user_tasks = [task for task in task_list if task["assigned_to"] == current_user]

    # Clear the screen and display menu option user currently is in
    print_screen_name("View My Tasks")
    
    # Print relevant message if there are currently no tasks assigned to the current user
    if len(current_user_tasks) == 0:
        input(f"There are currently no tasks assigned to you. {press_enter_message}")
        return

    # Present user with filter options
    print("Choose an option to filter tasks or press 'Enter' to view all my tasks:")
    print("1 - Incomplete tasks")
    print("2 - Completed tasks")
    print("3 - Overdue tasks")
    print("4 - Assigned by users that no longer exist")
    # Prompt user to choose filter option
    filter_choice = input("Select an option: ")

    # Clear the screen and display menu option user currently is in
    print_screen_name("View My Tasks")

    filtered_tasks, current_filter_name = load_filtered_tasks(filter_choice)

    print(f"Selected filter: {current_filter_name} [ {len(filtered_tasks)} total ]")
    # Loop through each task and display the details
    for number, task in enumerate(filtered_tasks, start = 1):
        task_title = task['task_title']
        assigned_by = task['assigned_by']
        assigned_by_label = " [deleted user]" if assigned_by not in load_users() else ""
        date_assigned = task['date_assigned'].strftime(date_format_output)
        due_date = task['due_date'].strftime(date_format_output)
        task_status = 'Yes' if task['task_status'] else 'No'
        task_description = task['task_description']

        # Calculate the remaining days until the due date
        remaining_days = (task['due_date'].date() - date.today()).days

        # Display days overdue if the task is overdue and NOT completed
        if task['due_date'].date() < date.today() and not task['task_status']:
            due_date += f"\t[{remaining_days} days overdue]"
        # Display days until the due date if the task is NOT overdue and NOT completed
        elif task['due_date'].date() > date.today() and not task['task_status']:
            due_date += f"\t[due in {remaining_days} days]"

        print(line * line_width)
        print(f"{str(number) + ('.'): <3} {'Task:': <15} {task_title}")
        print(f"{'': <3} {'Assigned by:': <15} {assigned_by + assigned_by_label}")
        print(f"{'': <3} {'Date assigned:': <15} {date_assigned}")
        print(f"{'': <3} {'Due date:': <15} {due_date}")
        print(f"{'': <3} {'Task complete?': <15} {task_status}")
        print(f"{'': <3} Task description: {task_description}")
    print(line * line_width)

    # Allow the user to select a task assigned to them to edit or mark as complete
    edit_task(filter_choice)

# Displays tasks assigned to all users
def view_all():
    """
    Displays tasks assigned to all users.

    The function first prompts the user to choose a filtering option for the tasks. The available options are:
        1 - Incomplete tasks
        2 - Completed tasks
        3 - Overdue tasks
        4 - Tasks assigned by users that no longer exist

    If any other input is provided, all tasks are displayed.

    Information displayed for each task:
        - Task title
        - Assigned to user
        - Assigned by user
        - [deleted user] label next to assigned by if assigned by user is not in register
        - Date assigned
        - Due date
        - [due in days] if task is not completed and not overdue
        - [days overdue] if task is not completed and overdue
        - Task completion status (Yes or No)
        - Task description
    """
    
    # Load a list of all tasks
    task_list = load_tasks()

    # Clear the screen and display the menu option the user is currently in
    print_screen_name("View All Tasks")

    # Print relevant message if there are currently no tasks
    if len(task_list) == 0:
        input(f"There are currently no tasks in the register. {press_enter_message}")
        return

    # Present the user with filtering options
    print("Choose an option to filter tasks or press 'Enter' to view all tasks:")
    print("1 - Incomplete tasks")
    print("2 - Completed tasks")
    print("3 - Overdue tasks")
    print("4 - Assigned by users that no longer exist")

    # Prompt the user to choose a filter option
    filter_choice = input("Select an option: ")

    # Clear the screen and display the menu option the user is currently in
    print_screen_name("View All Tasks")

    if filter_choice.strip() == "":
        current_filter_name = "All tasks"
        filtered_tasks = task_list
    else:
        filtered_tasks, current_filter_name = load_filtered_tasks(filter_choice)

    print(f"Selected filter: {current_filter_name} [ {len(filtered_tasks)} total ]")
    # Loop through each task and display the details
    for number, task in enumerate(filtered_tasks, start=1):
        task_title = task['task_title']
        assigned_to = task['assigned_to']
        assigned_to_label = " [deleted user]" if assigned_to not in load_users() else ""
        assigned_by = task['assigned_by']
        assigned_by_label = " [deleted user]" if assigned_by not in load_users() else ""
        date_assigned = task['date_assigned'].strftime(date_format_output)
        due_date = task['due_date'].strftime(date_format_output)
        task_status = 'Yes' if task['task_status'] else 'No'
        task_description = task['task_description']

        # Calculate the remaining days until the due date
        remaining_days = (task['due_date'].date() - date.today()).days

        # Display days overdue if the task is overdue and not completed
        if task['due_date'].date() < date.today() and not task['task_status']:
            due_date += f"\t[{remaining_days} days overdue]"
        # Display days until the due date if the task is not overdue and not completed
        elif task['due_date'].date() > date.today() and not task['task_status']:
            due_date += f"\t[due in {remaining_days} days]"

        print(line * line_width)
        print(f"{str(number) + ('.'): <3} {'Task:': <15} {task_title}")
        print(f"{'': <3} {'Assigned to:': <15} {assigned_to + assigned_to_label}")
        print(f"{'': <3} {'Assigned by:': <15} {assigned_by + assigned_by_label}")
        print(f"{'': <3} {'Date assigned:': <15} {date_assigned}")
        print(f"{'': <3} {'Due date:': <15} {due_date}")
        print(f"{'': <3} {'Task complete?': <15} {task_status}")
        print(f"{'': <3} Task description: {task_description}")
    print(line * line_width)
    
    user_choice = input("Enter '-1' to return to main menu or press 'Enter' to return to filter options: ")
    if user_choice == '-1':
        return
    else:
        view_all()

# Generates 'Task Overview' and 'User Overview' reports
def generate_reports():
    """
    Generates two text files:
        'task_overview.txt' - provides an overview of all tasks
        'user_overview.txt' - provides an overview of user statistics

    The task overview report includes the following:
    - Total number of tasks
    - Number of completed tasks
    - Number of incomplete tasks
    - Number of overdue tasks
    - Incomplete tasks (%)
    - Overdue tasks (%)

    The user overview report includes the following for each user:
    - Username
    - Number of Tasks Assigned
    - Percentage of Total Tasks (%)
    - Tasks Completed (%)
    - Tasks Incomplete (%)
    - Tasks Overdue (%)
    """

    line_width = 45
    task_list = load_tasks()
    users = load_users()

    # Clear the screen and display menu option user currently is in
    print_screen_name("Generate Reports")

    # Print relevant message if there are currently no tasks
    if len(task_list) == 0:
        input(f"\nThere are currently no tasks to generate reports. {press_enter_message}")
        return

    # Get counts for task overview
    total_tasks = len(task_list)
    completed_tasks = sum(task['task_status'] for task in task_list)
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(task['due_date'].date() < date.today() and not task['task_status'] for task in task_list)

    # Calculate percentages for task overview
    incomplete_percentage = (incomplete_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    # Get counts for user overview
    total_users = len(users)

    # Generate task overview report
    with open(task_overview_file_path, "w") as task_file:
        task_file.write("           Task Overview Report\n")
        task_file.write(f"{'=' * line_width}\n")
        task_file.write("Date Report Generated: {}\n\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        task_file.write(f"{'Total Tasks:': <20}{total_tasks}\n")
        task_file.write(f"{'Completed Tasks:': <20}{completed_tasks}\n")
        task_file.write(f"{'Incomplete Tasks:': <20}{incomplete_tasks}\n")
        task_file.write(f"{'Overdue Tasks:': <20}{overdue_tasks}\n")
        task_file.write(f"{'% Incomplete Tasks:': <20}{incomplete_percentage:.2f} %\n")
        task_file.write(f"{'% Overdue Tasks:': <20}{overdue_percentage:.2f} %\n\n\n")
    
    print("\nTask Overview report generated successfully!")

    # Generate user overview report
    with open(user_overview_file_path, "w") as user_file:
        user_file.write("           User Overview Report\n")
        user_file.write(f"{'=' * line_width}\n")
        user_file.write("Date Report Generated: {}\n\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        user_file.write(f"{'Total Users:': <15}{total_users}\n")
        user_file.write(f"{'Total Tasks:': <15}{total_tasks}\n\n")

        # Write user statistics
        for username, _ in users.items():
            user_tasks = [task for task in task_list if task['assigned_to'] == username]
            user_total_tasks = len(user_tasks)
            user_incomplete_tasks = sum(not task['task_status'] for task in user_tasks)
            user_completed_tasks = user_total_tasks - user_incomplete_tasks
            user_overdue_tasks = sum(task['due_date'].date() < date.today() and not task['task_status'] for task in user_tasks)

            # Calculate percentages for user statistics
            user_task_percentage = (user_total_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            user_completed_percentage = (user_completed_tasks / user_total_tasks) * 100 if user_total_tasks > 0 else 0
            user_incomplete_percentage = (user_incomplete_tasks / user_total_tasks) * 100 if user_total_tasks > 0 else 0
            user_overdue_percentage = (user_overdue_tasks / user_total_tasks) * 100 if user_total_tasks > 0 else 0

            user_file.write(f"{'Username:': <18}{username}\n")
            user_file.write(f"{'Tasks Assigned:': <18}{user_total_tasks} ({user_task_percentage:.2f} % of total)\n")
            user_file.write(f"{'% Completed:': <18}{user_completed_percentage:.2f} %\n")
            user_file.write(f"{'% Incomplete:': <18}{user_incomplete_percentage:.2f} %\n")
            user_file.write(f"{'% Overdue:': <18}{user_overdue_percentage:.2f} %\n")
            user_file.write(f"{line * line_width}\n")

    print("User Overview report generated successfully!")

    input(f"\n{press_enter_message}")

# Displays statistics based on the generated reports
def display_statistics():
    """
    Displays statistics based on the generated reports.
    If the reports are not generated, first generate them.
    """
    # Check if the reports exist, and generate them if not
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports()

    clear_screen()

    # Read and display the task overview report
    with open(task_overview_file_path, "r") as task_file:
        task_overview = task_file.read()
        print(task_overview)

    # Read and display the user overview report
    with open(user_overview_file_path, "r") as user_file:
        user_overview = user_file.read()
        print(user_overview)

    input(f"\n{press_enter_message}")

# Allows the user to change their password
def change_password():
    """
    Allows the user to change their password.
    
    Writes the new password to the 'user.txt' file.
    """
    
    users = load_users()

    # Clear the screen and display menu option user currently is in
    print_screen_name("Change Password")

    # Prompt user to enter current password
    print("Enter your current password to proceed.")
    current_password = input("Password: ")

    # Check if current password matches the stored password for the current user
    if current_password != users[current_user]:
        print("\nIncorrect password.")
        input(f"\n{press_enter_message}")
        return

    print("\nPassword verified!")
    input("Press 'Enter' to continue...")

    # Display password requirements, prompt user to enter the new password and perform checks
    new_password = verify_new_password(current_password)

    # Update password in the 'user.txt' file
    users[current_user] = new_password
    update_users(users, current_user, new_password)
    write_users(users)

    print(f"\nYour new password is '{new_password}'.")
    input(f"\n{press_enter_message}")

# Verifies if password entered matches stored password
def verify_password(users, current_user, current_password):
    """
    Verifies if the password entered by the user matches the stored password for the current user.

    Arguments:
        users (dict): A dictionary containing the usernames and passwords.
        current_user (str): The username of the current user.
        current_password (str): The password entered by the user.

    Returns:
        boolean: True if the password is verified, False otherwise.

    This function checks if the password entered by the user matches the stored password for the current user in the users dictionary.
    It returns True if the passwords match, and False otherwise.
    """
    
    stored_password = users.get(current_user)
    return current_password == stored_password

# Displays new username requirements and performs checks
def verify_new_username(users):
    """
    Prompts the user to enter a new username and performs checks on it.

    Arguments:
        users (dict): Dictionary containing existing usernames and passwords.

    Returns:
        new_username (str): The verified new username entered by the user.
    """
    
    # Prompt the user to enter the username and perform checks
    print("\nNew username requirements:")
    print("* 5 - 15 characters long")
    print("* must not contain any whitespace characters")
    print("* is not an existing username")
    while True:
        new_username = input("\nEnter new username: ")

        # Check if the username is 5 - 15 characters long
        if len(new_username) < 5 or len(new_username) > 15:
            print("\nInvalid username. Username must be 5 to 15 characters long.")
            continue

        # Check if the username contains any whitespace characters
        if any(char.isspace() for char in new_username):
            print("\nInvalid username. Username cannot contain any whitespace characters.")
            continue

        # Check if the username already exists in 'user.txt' to avoid duplicate usernames
        if new_username.lower() in users:
            print(f"\nUsername '{new_username}' already exists. Please enter a different username.")
            continue

        input(f"\nUsername '{new_username}' is available. Press 'Enter' to continue...")
        break

    return new_username

# Displays new password requirements and performs checks
def verify_new_password(current_password):
    """
    Prompts the user to enter a new password and performs checks on it.

    Arguments:
        current_password (str): The current user's password.

    Returns:
        new_password (str): The verified new password entered by the user.
    """

    # Display password requirements
    print("\nNew password requirements:")
    print("* 5 - 15 characters long")
    print("* contain at least 1 uppercase letter")
    print("* contain at least 1 lowercase letter")
    print("* contain at least 1 digit")
    print("* must not contain any whitespace characters")
    
    while True:
        # Prompt user for a new password
        new_password = input("\nEnter your new password: ")

        # Check if new password is the same as the current password
        if new_password == current_password:
            print("\nPassword cannot be the same as the current password. Try again.")
            continue

        # Check if the password is empty
        if len(new_password) == 0:
            print("\nPassword cannot be empty. Try again.")
            continue

        # Check for whitespace characters in the password
        if any(char.isspace() for char in new_password):
            print("\nPassword cannot contain whitespace characters. Try again.")
            continue

        # Check password length
        if len(new_password) < 5 or len(new_password) > 15:
            print("\nPassword must be 5 to 15 characters long. Try again.")
            continue

        # Check for at least one digit, uppercase letter, and lowercase letter in the password
        if not any(char.isdigit() for char in new_password) or not any(char.isupper() for char in new_password) or not any(char.islower() for char in new_password):
            print("\nPassword must contain at least one digit, uppercase letter, and lowercase letter. Try again.")
            continue

        # Prompt user to confirm the password
        confirm_password = input("Confirm your new password: ")

        # Check if password and confirmation match
        if new_password != confirm_password:
            print("\nPasswords do not match. Try again.")
            continue
    
        # Return the verified new password
        return new_password

# Updates user information for current user
def update_users(users, current_user, new_password):
    """
    Updates the password for the current user in the users dictionary.

    Arguments:
        users (dict): A dictionary containing the usernames and passwords.
        current_user (str): The username of the current user.
        new_password (str): The new password to be updated.

    Returns:
        users (dict): An updated dictionary with the new password.

    This function takes a dictionary of user information, the current username, and the new password.
    It updates the password for the current user in the dictionary and returns the updated dictionary.
    """

    if current_user in users:
        users[current_user] = new_password
    return users

# Writes user information to the 'user.txt' file
def write_users(users):
    """
    Writes the user information (usernames and passwords) to the 'user.txt' file.

    Arguments:
        users (dict): A dictionary containing the usernames and passwords.

    This function takes a dictionary of user information and writes it to the 'user.txt' file.
    Each user's information is formatted as 'username;password' and written on a new line in the file.
    """

    with open(user_file_path, "w") as user_file:
        for username, password in users.items():
            user_file.write(f"{username};{password}\n")

# Returns current user tasks with chosen filter
def load_filtered_tasks(filter_choice):
    """
    Retrieve the filtered tasks assigned to the current user based on the user's filter choice.

    Arguments:
        filter_choice (str): The user's choice for filtering the tasks. Default is an empty string.

    Returns:
        filtered_tasks (list): The list of filtered tasks assigned to the current user.
        current_filter_name (str): The string for name of the selected filter.

    This function loads the task list and filters it based on the user's choice to return the filtered tasks.
    The available filter choices are:
        1 - Incompleted tasks
        2 - Completed tasks
        3 - Overdue tasks
        4 - Tasks assigned by users that no longer exist

    If an invalid filter choice is provided or if no filter choice is given, it returns all tasks assigned to the current user.
    """
    
    # List of all tasks
    task_list = load_tasks()
    # List of current user tasks only
    current_user_tasks = [task for task in task_list if task['assigned_to'] == current_user]
    
    # Create list with filtered tasks based on user's choice
    if filter_choice == '1':
        current_filter_name = "Incompleted tasks"
        filtered_tasks = [task for task in current_user_tasks if not task['task_status']]
    elif filter_choice == '2':
        current_filter_name = "Completed tasks"
        filtered_tasks = [task for task in current_user_tasks if task['task_status']]
    elif filter_choice == '3':
        current_filter_name = "Overdue tasks"
        filtered_tasks = [task for task in current_user_tasks if task['due_date'].date() < date.today() and not task['task_status']]
    elif filter_choice == '4':
        current_filter_name = "Tasks assigned by users that no longer exist"
        filtered_tasks = [task for task in current_user_tasks if task['assigned_by'] not in load_users()]
    else:
        current_filter_name = "All tasks"
        # Show all tasks if no filter option selected or invalid input is entered
        filtered_tasks = current_user_tasks 

    # Return filtered task list and name of chosen filter
    return filtered_tasks, current_filter_name

# Returns all tasks from 'tasks.txt' file in sorted list
def load_tasks():
    """
    Load tasks from the 'tasks.txt' file into a list of dictionaries, sorted by due date.

    Returns:
        task_list (list): A list of dictionaries containing the task details, sorted by due date.

    This function reads the task information from the 'tasks.txt' file, sorts the tasks by due date,
    and returns a list of dictionaries. Each dictionary represents a task with the following keys:
    - 'assigned_to': The username of the user to whom the task is assigned.
    - 'assigned_by': The username of the user who assigned the task.
    - 'task_title': The title or name of the task.
    - 'task_description': The description or details of the task.
    - 'due_date': The due date of the task (as a datetime object).
    - 'date_assigned': The date when the task was assigned (as a datetime object).
    - 'task_status': The status of the task (True for completed, False for incompleted).
    """
    
    task_list = []

    try:
        with open(tasks_file_path, "r") as tasks_file:
            lines = tasks_file.readlines()
            for line in lines:
                task_components = line.strip().split(';')
                task = {
                    'assigned_to': task_components[0],
                    'assigned_by': task_components[1],
                    'task_title': task_components[2],
                    'task_description': task_components[3],
                    'due_date': datetime.strptime(task_components[4], date_format),
                    'date_assigned': datetime.strptime(task_components[5], date_format),
                    'task_status': True if task_components[6] == 'Yes' else False
                }
                task_list.append(task)
        # Sort tasks by due date
        task_list.sort(key=lambda task: task['due_date'])
    except FileNotFoundError:
        print("Error: 'tasks.txt' file not found.")

    return task_list

# Writes updated task list back to file
def update_tasks_file(task_list):
    """
    Update the tasks file with the given task list.

    Arguments:
        task_list (list): The list of tasks to be written to the file.
    """
    
    with open(tasks_file_path, "w") as tasks_file:
        for task in task_list:
            due_date_str = task['due_date'].strftime(date_format)
            date_assigned_str = task['date_assigned'].strftime(date_format)
            task_status_str = "Yes" if task['task_status'] else "No"
            task_line = f"{task['assigned_to']};{task['assigned_by']};{task['task_title']};{task['task_description']};{due_date_str};{date_assigned_str};{task_status_str}\n"
            tasks_file.write(task_line)

# Entry point of the Task Manager program
def task_manager():
    """
    Entry point of program.

    This function displays the welcome message, enters the main menu loop, and performs the following steps:
    1. Checks if the 'user.txt' file exists and creates it if it doesn't.
    2. Checks if the 'tasks.txt' file exists and creates it if it doesn't.
    3. Prompts the user to login.
    4. Displays the main menu and performs the corresponding menu actions based on user input.
    
    Takes action based on the user's choice from the main menu.

    Options that are only accessible to the ADMIN:
    - Generate Reports
    - Display Statistics
    - Delete Users
    """
    
    # Main menu loop
    while True:
        # Create 'user.txt' file if it doesn't exist
        create_user_file()
        # Create 'tasks.txt' file if it doesn't exist
        create_tasks_file()
        
        login()

        menu_choice = main_menu()
        
        if menu_choice == 'r':
            register_user()
        elif menu_choice == 'a':
            add_task()
        elif menu_choice == 'va':
            view_all()
        elif menu_choice == 'vm':
            view_mine()
        elif menu_choice == 'gr' and current_user == 'admin':
            generate_reports()
        elif menu_choice == 'cp':
            change_password()
        elif menu_choice == 'l':
            logout()
        elif menu_choice == 'e':
            exit()
        elif menu_choice == 'ds' and current_user == 'admin':
            display_statistics()
        elif menu_choice == 'du' and current_user == 'admin':
            delete_user()
        else:
            input("\nYou have made a wrong choice, press 'Enter' to try again...")
            clear_screen()


# Start the Program
task_manager()