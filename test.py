import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Workout, Nutrition, Sleep  
from insert import create_fake_user, create_fake_data
from query import *
import random
from faker import Faker

# Setup for Faker and random seed for consistent test data generation.
f = Faker(["en_US"])
Faker.seed(0) 
random.seed(0)
engine = create_engine('sqlite:///test_fitness_app.db')
Base.metadata.drop_all(bind=engine) # Drop any existing data.
Base.metadata.create_all(bind=engine) # Create new tables.

class TestFitness(unittest.TestCase):
    #Setting up database
    def setUp(self):
        self.engine = engine
        self.metadata = Base.metadata
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    # Teardown method called after each test.
    def tearDown(self):
        self.session.close()
        self.metadata.drop_all(self.engine)
        
    # Testing Table Creation 
    def test_user_table_created(self):
        self.assertTrue('users' in self.metadata.tables)

    def test_workout_table_created(self):
        self.assertTrue('workouts' in self.metadata.tables)

    def test_nutrition_table_created(self):
        self.assertTrue('nutrition' in self.metadata.tables)

    def test_sleep_table_created(self):
        self.assertTrue('sleep' in self.metadata.tables)


    #Insert test data into the database
    def insert_data(self):
        for _ in range(5):
            fake_user = create_fake_user(f)
            create_fake_data(fake_user)
    
    # Testing Data Insertion 
    def test_insert_user(self):
        result = session.query(User).filter_by(id=1).first()
        self.assertIsNotNone(result)

    def test_insert_nutrition(self):
        result = session.query(Nutrition).filter_by(id=1).first()
        self.assertIsNotNone(result)
    
    def test_insert_workout(self):
        result = session.query(Workout).filter_by(id=1).first()
        self.assertIsNotNone(result)

    def test_insert_sleep(self):
        result = session.query(Sleep).filter_by(id=1).first()
        self.assertIsNotNone(result)
   
            
if __name__ =="__main__":
    unittest.main()