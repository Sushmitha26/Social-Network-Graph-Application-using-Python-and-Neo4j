from db.connection import Neo4jConnection
from db.user_management import UserManagement
from db.social_graph import SocialGraph
from register import register_flow
from login import login_flow

# Set your credentials
uri = "bolt://localhost:7687"
user = "neo4j"
password = ""

connection = Neo4jConnection(uri, user, password)
connection.test_connection()

# Initialize modules
user_mgmt = UserManagement(connection)
social_graph = SocialGraph(connection)

while True:
    print("\nWelcome! Choose one from the following options:")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter option: ")

    if choice == "1":
        register_flow(user_mgmt)
    elif choice == "2":
        login_flow(user_mgmt, social_graph)
    elif choice == "3":
        print("Thank You!")
        break
    else:
        print("Invalid choice. Please try again.")

connection.close()

