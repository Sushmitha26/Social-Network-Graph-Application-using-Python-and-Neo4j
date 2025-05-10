from unittest import case

profile_edit_menu = """
Profile Edit Options:
1. Edit First Name
2. Edit Last Name
3. Edit Email
4. Edit Bio
5. Edit Location
6. Edit Country
7. Exit Edit Mode 

Please select an option (1-7): """

class SocialGraph:
    def __init__(self, connection):
        self.connection = connection

    #we can add the database logic part for remaining usecases here, like view profile, edit profile etc.
    def get_user_info(self, username):
        with self.connection.driver.session() as session:
            result = session.run("""
            MATCH (u:User {username: $username})
            RETURN u.userId AS userId, u.firstName AS firstName, u.lastName AS lastName, 
                   u.username AS username, u.email AS email, u.bio AS bio,
                   u.location AS location, u.country AS country
            """, username=username)
            record = result.single()

            if record:
                print(f"User Info:")
                print(f"User ID: {record['userId']}")
                print(f"Name: {record['firstName']} {record['lastName']}")
                print(f"Username: {record['username']}")
                print(f"Email: {record['email']}")
                print(f"Bio: {record['bio']}")
                print(f"Location: {record['location']}")
                print(f"Country: {record['country']}")
                return record
            else:
                print("User not found.")
                return None

    def set_user_info(self, username):
        with self.connection.driver.session() as session:
            result = session.run("""
            MATCH (u:User {username: $username})
            RETURN u.userId AS userId, u.firstName AS firstName, u.lastName AS lastName, 
                   u.username AS username, u.email AS email, u.bio AS bio,
                   u.location AS location, u.country AS country
            """, username=username)
            record = result.single()

            if not record:
                print("User not found.")
                return None

            user_continue = True

            while user_continue:

                user_choice = int(input(profile_edit_menu))

                match user_choice:
                    case 1:
                        new_first_name = input("Enter new first name: ")
                        session.run("""
                            MATCH (u:User {username: $username})
                            SET u.firstName = $new_first_name
                        """, username=username, new_first_name=new_first_name)
                        print(f"First name updated to {new_first_name}.")
                    case 2:
                        new_last_name = input("Enter new last name: ")
                        session.run("""
                            MATCH (u:User {username: $username})
                            SET u.lastName = $new_last_name
                        """, username=username, new_last_name=new_last_name)
                        print(f"Last name updated to {new_last_name}.")
                    case 3:
                        new_email = input("Enter new email: ")
                        session.run("""
                            MATCH (u:User {username: $username})
                            SET u.email = $new_email
                        """, username=username, new_email=new_email)
                        print(f"Email updated to {new_email}.")
                    case 4:
                        new_bio = input("Enter new bio: ")
                        session.run("""
                            MATCH (u:User {username: $username})
                            SET u.bio = $new_bio
                        """, username=username, new_bio=new_bio)
                        print(f"Bio updated.")
                    case 5:
                        new_location = input("Enter new location: ")
                        session.run("""
                            MATCH (u:User {username: $username})
                            SET u.location = $new_location
                        """, username=username, new_location=new_location)
                        print(f"Location updated to {new_location}.")
                    case 6:
                        new_country = input("Enter new country: ")
                        session.run("""
                            MATCH (u:User {username: $username})
                            SET u.country = $new_country
                        """, username=username, new_country=new_country)
                        print(f"Country updated to {new_country}.")
                    case 7:
                        print("Exiting Edit Mode.")
                        user_continue = False

                    case _:
                        print("Invalid option. Please try again.")

            return None


    def follow_user(self, username, followee_username):
        with self.connection.driver.session() as session:
            result = session.run("""
            MATCH (u:User {username: $username})
            MATCH (f:User {username: $followee_username})
            MERGE (u)-[:FOLLOWS]->(f)
            RETURN u.username AS username, f.username AS followee_username
            """, username=username, followee_username=followee_username)
            record = result.single()

            if record:
                print(f"{username} followed {followee_username}.")
                return record
            else:
                print(f"Failed to follow {followee_username}.")
                return None


    def unfollow_user(self, username, followee_username):
        with self.connection.driver.session() as session:
            result = session.run("""
            MATCH (u:User {username: $username})
            MATCH (f:User {username: $followee_username})
            OPTIONAL MATCH (u)-[r:FOLLOWS]->(f)
            WITH u, f, r
            WHERE r IS NOT NULL
            DELETE r
            RETURN count(r) as deletedCount
            """, username=username, followee_username=followee_username)
            record = result.single()

            if record and record['deletedCount'] > 0:
                print(f"{username} unfollowed {followee_username}.")
                return True
            else:
                print(f"Failed to unfollow {followee_username}. Relationship may not exist.")
                return False

    def get_user_followers(self, username):
        with self.connection.driver.session() as session:
            result = session.run("""
            MATCH (u:User {username: $username})<-[:FOLLOWS]-(f:User)
            RETURN f.username AS follower_username
            """, username=username)
            followers = [record["follower_username"] for record in result]
            
            if followers:
                print(f"Followers of {username}:")
                for follower in followers:
                    print(f"- {follower}")
                return followers
            else:
                print(f"{username} has no followers.")
                return []
    
    def get_user_following(self, username):
        with self.connection.driver.session() as session:
            result = session.run("""
            MATCH (u:User {username: $username})-[:FOLLOWS]->(f:User)
            RETURN f.username AS following_username
            """, username=username)
            following = [record["following_username"] for record in result]
            
            if following:
                print(f"{username} is following:")
                for user in following:
                    print(f"- {user}")
                return following
            else:
                print(f"{username} is not following anyone.")
                return []

    #UC 9:
    def friend_recommendations(self, username):
        with self.connection.driver.session() as session:
            result = session.run("""
                MATCH (me:User {username: $username})-[:FOLLOWS]->(friend:User)-[:FOLLOWS]->(rec:User)
                WHERE NOT (me)-[:FOLLOWS]->(rec) AND me <> rec
                RETURN DISTINCT rec.username AS recommended_user
                LIMIT 10
            """, username=username)

            print("\n--- Friend Recommendations ---")
            recommendations = result.values()
            if recommendations:
                for rec in recommendations:
                    print(f"- {rec[0]}")
            else:
                print("No recommendations available.")

    def get_mutual_connections(self, username1, username2):
        """
        Find mutual connections between two users.
        Returns users who are followed by both username1 and username2.
        """
        with self.connection.driver.session() as session:
            result = session.run("""
                MATCH (user1:User {username: $username1})-[:FOLLOWS]->(mutual:User)
                MATCH (user2:User {username: $username2})-[:FOLLOWS]->(mutual)
                RETURN mutual.username AS mutual_friend
            """, username1=username1, username2=username2)
            
            mutual_connections = result.values()
            
            print(f"\n--- Mutual Connections between {username1} and {username2} ---")
            if mutual_connections:
                for connection in mutual_connections:
                    print(f"- {connection[0]}")
                print(f"Total mutual connections: {len(mutual_connections)}")
            else:
                print("No mutual connections found.")

    def search_users(self, search_term):
        """
        Search for users by username or name (firstName/lastName).
        Returns and prints users that match the search criteria.
        """
        with self.connection.driver.session() as session:
            result = session.run("""
                MATCH (u:User)
                WHERE u.username CONTAINS $search_term 
                   OR toLower(u.firstName) CONTAINS toLower($search_term)
                   OR toLower(u.lastName) CONTAINS toLower($search_term)
                RETURN u.userId AS userId, u.firstName AS firstName, u.lastName AS lastName, 
                       u.username AS username, u.location AS location
                LIMIT 10
            """, search_term=search_term)
            
            users = list(result)
            
            print(f"\n--- Search Results for '{search_term}' ---")
            if users:
                for i, user in enumerate(users, 1):
                    print(f"{i}. {user['firstName']} {user['lastName']} (@{user['username']})")
                    if user['location']:
                        print(f"   Location: {user['location']}")
                print(f"\nFound {len(users)} matching users.")
                return users
            else:
                print("No users found matching your search criteria.")
                return []
            
    
    def most_popular_users(self):
        """
        Returns the list of top 10 users with the most followers.
        Displays each user's name, username, and follower count.
        """
        with self.connection.driver.session() as session:
            result = session.run("""
                MATCH (follower:User)-[:FOLLOWS]->(user:User)
                WITH user, count(follower) as followerCount
                ORDER BY followerCount DESC
                LIMIT 10
                RETURN user.name AS name,
                       user.username AS username,
                       followerCount
            """)

            users = list(result)

            print("\n--- Top 10 Most Popular Users ---")
            if users:
                for i, user in enumerate(users, 1):
                    print(f"{i}. {user['name']} (@{user['username']})")
                    print(f"   Followers: {user['followerCount']}")
                return users
            else:
                print("No users found.")
                return []

