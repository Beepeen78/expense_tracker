"""Script to update database schema - DROPS ALL TABLES AND RECREATES THEM"""
from database import engine
import models

# WARNING: This will drop all existing tables and data!
print("WARNING: This will drop all tables and recreate them. All data will be lost!")
response = input("Type 'yes' to continue: ")

if response.lower() == 'yes':
    # Drop all tables
    models.Base.metadata.drop_all(bind=engine)
    print("Dropped all tables.")
    
    # Create all tables
    models.Base.metadata.create_all(bind=engine)
    print("Created all tables successfully!")
else:
    print("Cancelled.")

