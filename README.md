# CS157C-Final

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


