import hashlib
from datetime import datetime, timedelta

class UserManagement:
    def __init__(self, connection):
        self.connection = connection
        self.session_length = timedelta(hours=4) # user must re-login after 4 hours.

    def register_user(self, name, email, username, password):
        hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
        with self.connection.driver.session() as session:
            session.run("""
                MERGE (u:User {username: $username})
                ON CREATE SET u.name = $name, u.email = $email, u.password = $password
            """, name=name, email=email, username=username, password=hashed_pw)
        print(f"User '{username}' registered successfully.")

    def login_user(self, username, password):
        with self.connection.driver.session() as session:
            result = session.run("""
                MATCH (u:User {username: $username})
                RETURN u.password AS hashed_password
            """, username=username)
            record = result.single()

            if record:
                stored_hashed = record["hashed_password"]
                sha256_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
                if sha256_hash == stored_hashed:
                    # update the last-login time for the user.
                    current_time = datetime.now().isoformat()
                    session.run("""
                    MATCH (u:User {username: $username})
                    SET u.last_login = $last_login
                    """, username=username, last_login=current_time)
                    print(f"Login successful! Welcome, {username}!")
                    return True
                else:
                    print("Incorrect password.")
                    return False
            else:
                print("Username not found.")
                return False


    def is_session_valid(self, username) -> bool:
        """Checks if the user's session is still valid, based on last login and session length."""
        with self.connection.driver.session() as session:
            result = session.run("""
                MATCH (u:User {username: $username})
                RETURN u.last_login AS last_login
            """, username=username)
            record = result.single()

            if record and record["last_login"]:
                last_login = datetime.fromisoformat(record["last_login"])
                return datetime.now() - last_login <= self.session_length
            return False