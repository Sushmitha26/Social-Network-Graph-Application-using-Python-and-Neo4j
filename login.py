from getpass import getpass
from post_login import post_login_menu

def login_flow(user_mgmt, social_graph):
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")
    
    success = user_mgmt.login_user(username, password)
    if success:
        post_login_menu(user_mgmt, social_graph, username)
    else:
        print("Incorrect credentials")