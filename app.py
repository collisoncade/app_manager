import os
import random
import json
from datetime import datetime, time
from dateutil.relativedelta import relativedelta

'''
>>> Cool lines
'''

# ================== Global Variable ==================
line = '='
space = ' '
new_file_write = {"users": 
    [
        {
            "username": "admin",
            "password": "kronos",
            "user_name": "",
            "date_created ": f"{datetime.now().strftime('%m-%d-%Y')}"
            
        }
    ]
}

# ================== Global Paths ==================
script_directory = os.path.dirname(os.path.abspath(__file__))
user_file_path = os.path.join(script_directory, "users.json")

# ================== Functions ================== 
def ensure_userjson_existence():
    try:
        if not os.path.isfile("users.json"):
            print(f"<|   Error   |>: \"users.json is a mandatory file that stores the users\' credentials\"")
            print(f"<|  Solution |>: Ensure \"users.json\" is in the correct directory or create a new one from scratch.")
            while True:
                prompt_new_json_file = input("Would you like to create a new .json file from scratch?\n~ ")
                if prompt_new_json_file != 'yes': exit()
                else:
                    with open(user_file_path, "w") as new_file:
                        name = input("Enter the name of the admin\n~ ")
                        if len(name) != 0:
                            new_file_write["users"][0]["user_name"]=name
                        new_file.write(json.dumps(new_file_write))
                        task_manager()
    except FileNotFoundError as FNFE:
        print(FNFE)

def clear_screen():
    '''
    Tool function to clear the user's screen
    '''
    os.system('cls' if os.name == 'nt' else 'clear')


class credentials:
    current_username = None

    def load_users():
        users = {}
        with open(user_file_path, 'r') as user_file:
            user_data = json.load(user_file)
            for i, user in enumerate(user_data["users"]):
                username = user_data["users"][i]["username"]
                password = user_data["users"][i]["password"]
                users[username] = password
        return users
            
    def verify_password(users, username, password):
        stored_password = users.get(username)
        return password == stored_password
    
# ================== Page Functions ==================

class Page:
    
    def __init__(self):
        clear_screen()
        
    def page_choice(choice, username=None):
        if credentials.current_username is None :
            if choice == 'l':
                Page.login()
            elif choice == 'ca':
                Page.page_name_header('Create Account')
                Page.create_account()
            elif choice == 'ab':
                Page.page_name_header('About NFL Predictions')
            elif choice == 'ra':
                Page.page_name_header('Recover account')
            else:
                clear_screen()
                Page.welcome_header()
                print("Invalid option, please select an option below.\n")
                Page.unlogged_menu_page()
        elif len(username) != 0:
            if choice == 'mp':
                Page.page_name_header(f'Make Picks for {credentials.current_username}')
            elif choice == 'ep':
                Page.page_name_header(f'Edit {credentials.current_username}\'s Picks')
            elif choice == 'vp':
                Page.page_name_header(f'View {credentials.current_username}\'s Picks')
            elif choice == 'vr':
                Page.page_name_header(f'{credentials.current_username}\'s Record')
            elif choice == 'du':
                Page.page_name_header(f'Delete {credentials.current_username}')
            elif choice == 'lo':
                # credentials.current_username = None
                Page.logout()
        elif username == 'admin':
            pass
        
    def welcome_header():
        clear_screen()
        print(line * 27)
        print(f"Welcome to NFL Predictions!")
        print(line * 27)
        print()
        
    def page_name_header(page_title):
        clear_screen()
        print(line * (18 + len(page_title)))
        print(f"NFL Predictions > " + page_title.title())
        print(line * (18 + len(page_title)))
        print()
        
    def unlogged_menu_page():
        unlogged_user_options = {
            '[l]': 'Login to your account.',
            '[ca]': 'Create an account!',
            '[ab]': 'What is "NFL Predictions"?',
            '[ra]': 'Recover your account.'
        }

        for option, description in list(unlogged_user_options.items()):
            print(f"{option.ljust(6)} {description}")
                
        while True:
            choice = input('\nSelect option ~> ').strip('[]')
            if len(choice) == 0:
                print("Invalid option, try again.")
                continue
            Page.page_choice(choice)
            break
        
    def logged_menu_page(username):  
        user_options = {
            '[mp]': 'Make this week\'s picks.',
            '[ep]': 'Edit your picks for this week.',
            '[vp]': 'View your picks for this week.',
            '[vr]': 'View your record for the season.',
            '[lo]': 'Logout',
            '[du]': 'Delete user',
            '[au]': 'Add user'
        }
        
        clear_screen()
        
        Page.page_name_header(credentials.current_username)
        
        if credentials.current_username != 'admin':
            print("\n".join(f"{option.ljust(6)} {description}" for option, description in list(user_options.items())[:6]))
            
        else:
            print("\n".join(f"{option.ljust(6)} {description}" for option, description in list(user_options.items())))
            
        while True:
            choice = input('\nSelect option ~> ').strip('[]')
            if len(choice) == 0:
                print("Invalid option, try again.")
                continue
            Page.page_choice(choice, credentials.current_username)
            break
                  
    def login(username=None):
        Page.page_name_header('Login')
        
        users = credentials.load_users()
        
        while credentials.current_username is None:
            username = input("Username: ")
            if username == 'x':
                exit()
            elif username == '<-':
                return task_manager()
                
            elif len(username) == 0:
                print("Invalid response, try again.")
                continue
            elif username not in users:
                print(f"We couldn\'t find \'{username}\', please try again.")
                continue
            
            while credentials.current_username is None:
                password = input('Password: ')
            
                if password == 'x':
                    confirm_esc = input("\nAre you sure you want to exit?\n\t~> ")
                    if confirm_esc != 'no':
                        continue
                    else: Page.welcome_header()
                elif not credentials.verify_password(users, username, password):
                    print('\t### Wrong password ###')
                    break
                else:
                    print(f'Welcome {username}!\n')
                    credentials.current_username = username
                    break
        
        Page.logged_menu_page(credentials.current_username)
        return credentials.current_username
       
    def logout():
        credentials.current_username = None
        task_manager()

    def create_account():
        curr_new_user_data = {
            "username": "",
            "password": "",
            "role": "",  
            "email": "",
            "date_created": ""
        }
        
        curr_new_user_name = input('Enter new user:\n\t~ ')
        credentials.load_users()
        with open(user_file_path, 'w') as user_file:
            json.dumps(curr_new_user_data)
            
        while True:
            if curr_new_user_name in user_file:
                print(f"It looks like {curr_new_user_name} is already taken. Try something similar.\n ~> ")
            else:
                curr_new_user_pass = input(f'Enter password for {curr_new_user_name}:\n\t~ ')
                curr_new_user_data["password"] = curr_new_user_pass
                curr_new_user_email = input(f'Enter email for {curr_new_user_name}:\n\t~ ')
                curr_new_user_data["email"] = curr_new_user_email
                curr_new_user_data["date_created"] = datetime.now().strftime('%m-%d-%Y')
                
        
def task_manager():
    clear_screen()
    
    Page.welcome_header()
    
    ensure_userjson_existence()
    
    if credentials.current_username is None:
        Page.unlogged_menu_page()
    else:
        Page.logged_menu_page(credentials.current_username)



# =============================================== Run task_manager =============================================== 
if __name__ == "__main__":
    task_manager()
# =============================================== Run task_manager =============================================== 