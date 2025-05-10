import pandas as pd
import os
from neo4j import GraphDatabase
from faker import Faker
import hashlib
import random
from datetime import datetime 

# Initialize Faker to generate realistic data
fake = Faker()

# Neo4j connection configuration
NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = ""

# Path to the SNAP ego-Facebook dataset
dataset_path = "./data"

class Neo4jImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
        
    def run_query(self, query, params=None):
        with self.driver.session() as session:
            result = session.run(query, params)
            return list(result)
    
    def setup_schema(self):
        # Create constraints for faster lookups
        constraints = [
            "CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.userId IS UNIQUE",
            "CREATE CONSTRAINT username IF NOT EXISTS FOR (u:User) REQUIRE u.username IS UNIQUE",
            "CREATE CONSTRAINT email IF NOT EXISTS FOR (u:User) REQUIRE u.email IS UNIQUE"
        ]
        
        for constraint in constraints:
            self.run_query(constraint)
        
        print("Schema setup complete")
    
    def import_users(self, user_ids):
        print(f"Importing {len(user_ids)} users...")
        
        # Create batches of users for more efficient import
        batch_size = 500
        user_batches = [list(user_ids)[i:i+batch_size] for i in range(0, len(user_ids), batch_size)]
        
        user_count = 0
        for batch in user_batches:
            # Batch insert users
            query = """
            UNWIND $users AS userData
            CREATE (u:User)
            SET u = userData
            """
            
            users_data = []
            for user_id in batch:
                user_data = generate_user_data(user_id)
                users_data.append(user_data)
                user_count += 1
            
            self.run_query(query, {"users": users_data})
            print(f"Created {user_count} users so far")
        
        print(f"Total users created: {user_count}")
    
    def import_relationships(self, edges_df):
        print("Importing relationships...")
        
        # Create batches of relationships for more efficient import
        batch_size = 1000
        edge_batches = [edges_df[i:i+batch_size] for i in range(0, len(edges_df), batch_size)]
        
        rel_count = 0
        for batch in edge_batches:
            edges = []
            for _, edge in batch.iterrows():
                edges.append({
                    "source_id": int(edge['source']),
                    "target_id": int(edge['target']),
                    "created_at": datetime.now().isoformat()
                })
            
            # Batch create relationships
            query = """
            UNWIND $edges AS edge
            MATCH (source:User {userId: toString(edge.source_id)})
            MATCH (target:User {userId: toString(edge.target_id)})
            CREATE (source)-[r:FOLLOWS {createdAt: edge.created_at}]->(target)
            """
            
            self.run_query(query, {"edges": edges})
            rel_count += len(edges)
            print(f"Created {rel_count} relationships so far")
        
        print(f"Total relationships created: {rel_count}")

def generate_user_data(user_id):
    """Generate comprehensive user data with Faker"""
    # Make the random generation deterministic based on user_id
    # This ensures consistent data across runs
    random.seed(int(user_id))
    fake.seed_instance(int(user_id))
    
    # Basic user info
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = f"{first_name.lower()}{last_name.lower()}{user_id}"[:20]
    
    # Extended profile data
    return {
        "userId": str(user_id),
        "firstName": first_name,
        "lastName": last_name,
        "username": username,
        "email": f"{username}@{fake.free_email_domain()}",
        "password": hashlib.sha256(f"password{user_id}".encode()).hexdigest(),
        "bio": fake.paragraph(nb_sentences=3),
        "location": fake.city(),
        "country": fake.country(),
    }

def main():
    # Load the edge list - this contains the friendship connections
    edges_file = os.path.join(dataset_path, "facebook_combined.txt")
    edges_df = pd.read_csv(edges_file, sep=' ', header=None, names=['source', 'target'])

    # Get unique user IDs from the edge list
    user_ids = set(edges_df['source'].tolist() + edges_df['target'].tolist())
    print(f"Total unique users: {len(user_ids)}")
    
    # Initialize Neo4j importer
    importer = Neo4jImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    try:
        # Setup schema
        importer.setup_schema()
        
        # Import users
        importer.import_users(user_ids)
        
        # Import relationships
        importer.import_relationships(edges_df)
        
        print("Import complete!")
    finally:
        importer.close()

if __name__ == "__main__":
    main()
