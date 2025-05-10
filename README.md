# Project overview
A basic social networking application using Python and Neo4j as the database. The system will model relationships between users, enabling social interactions such as following others, recommending connections, and efficiently querying networks using graph-based techniques.

## Dataset
The application uses SNAP ego-Facebook dataset with around 4,000 nodes and 80,000 edges, enriching profiles with Faker and loading them using Cypher batch queries.

## Usecases implemented:
1. User Management
UC-1: User Registration: A new user can sign up by providing basic details (name, email, username, password). The system stores user data in Neo4j as nodes.
UC-2: User Login: A registered user can log in using their username and password. The system authenticates the credentials and grants access.
UC-3: View Profile: A user can view their own profile and update basic information.
UC-4: Edit Profile: A user can update their name, bio, and other details.

2. Social Graph Features
UC-5: Follow Another User - A user can follow another user, creating a "FOLLOWS" relationship in Neo4j. The relationship is stored as an edge in the graph database.
UC-6: Unfollow a User - A user can unfollow another user, removing the "FOLLOWS" relationship.
UC-7: View Friends/Connections - A user can see a list of people they are following and who follow them.
UC-8: Mutual Connections - A user can see mutual friends (users followed by both parties).
UC-9: Friend Recommendations - The system suggests new people to follow based on common connections using second degree graph traversal queries.

4. Search & Exploration
UC-10: Search Users - A user can search for other users by name or username. The system returns a list of matching users.
UC-11: Explore Popular Users - The system displays the most-followed users.

## Database connection setup

1. In local neo4j desktop, create new database called SocialGraph and set a password to it.
2. Create python virtual environment in local:
   `python -m venv venv`
   `source venv/bin/activate` (On Windows: `venv\Scripts\activate`)
3. Install dependencies in requirements.txt
4. Run main.py file : `python main.py`
5. You should be able to see 'Neo4j Connected' message.


## Folder Structure
```
SocialNetwork/
├── db/
│   ├── __init__.py             # Makes 'db' a Python package
│   ├── connection.py           # Handles Neo4j database connection
│   ├── user_management.py      # User operations: Register, Login, View Profile, Edit Profile
│   └── social_graph.py         # Social features: Follow, Unfollow, Friend Recommendations, Mutual Connections
├── main.py                     # Main entry point: User chooses to Register or Login
├── register.py                  # Handles the user registration flow
├── login.py                     # Handles the user login flow
├── post_login.py                # Post-login menu: View Profile, Friend Recommendations, Logout
```


