def post_login_menu(user_mgmt, social_graph, username):
    while True:
        print(f"\nWelcome back, {username}!")
        #we can add all the remaining usecases here, like view profile, edit profile etc.
        print("3. View Profile")
        print("4. Edit Profile")
        print("5. Follow User")
        print("6. Unfollow User")
        print("7. View Followers/Following")
        print("8. Find Mutual Connections")
        print("9. Friend Recommendations")
        print("10. Search Users")
        print("11. Most Popular Users")
        print("12. Logout")

        choice = input("Enter option: ")

        # refactored to use a match case block, as it is more efficient.
        match choice:
            case "3":
                social_graph.get_user_info(username)
            case "4":
                social_graph.set_user_info(username)
            case "5":
                followee = input("Enter the username of the user you want to follow: ")
                social_graph.follow_user(username, followee)
            case "6":
                followee = input("Enter the username of the user you want to unfollow: ")
                social_graph.unfollow_user(username, followee)
            case "7":
                social_graph.get_user_followers(username)
                social_graph.get_user_following(username)
            case "8":
                other_username = input("Enter the username to find mutual connections with: ")
                social_graph.get_mutual_connections(username, other_username)
            case "9":
                social_graph.friend_recommendations(username)
            case "10":
                search_term = input("Enter name or username to search: ")
                social_graph.search_users(search_term)
            case "11":
                social_graph.most_popular_users()
            case "12":
                print("Logging out...")
                break

            case _:
                print("Invalid choice. Please try again.")


            #         if choice == "3":
            #             social_graph.get_user_info(username)
            #
            #
            #         elif choice == "7":
            #             social_graph.get_user_followers(username)
            #             social_graph.get_user_following(username)
            #         elif choice == "8":
            #             other_username = input("Enter the username to find mutual connections with: ")
            #             social_graph.get_mutual_connections(username, other_username)
            #         elif choice == "9":
            #             social_graph.friend_recommendations(username)
            #         elif choice == "10":
            #             search_term = input("Enter name or username to search: ")
            #             social_graph.search_users(search_term)
            #         elif choice == "12":
            #             print("Logging out... 👋")
            #             break
            #         else:
            #             print("Invalid choice. Please try again.")