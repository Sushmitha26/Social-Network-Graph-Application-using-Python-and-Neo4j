from getpass import getpass

def register_flow(user_mgmt):
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    
    user_mgmt.register_user(name, email, username, password)

