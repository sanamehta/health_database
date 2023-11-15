from faker import Faker
from models import *
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
import random
from datetime import datetime
from sqlalchemy import text


# Instantiate a Faker object for generating fake data
fake = Faker(["en_US"])
# Set a seed for Faker to generate repeatable pseudorandom data.
Faker.seed(0) 
random.seed(0)

# Drop all existing tables 
Base.metadata.drop_all(bind=engine)

# Create all tables based on model definitions
Base.metadata.create_all(bind=engine)

# Create a sessionmaker bound to the engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Function to create a fake user
def create_fake_user(fake):
    user = User(
        name=fake.name(),
        email=fake.email(),
        age=random.randint(18, 80),
        gender=random.choice(['Male', 'Female', 'Other']),
        height=random.uniform(1.5, 2.0),
        weight=random.uniform(50, 100)
    )
    session.add(user)
    return user

# Function to create fake data for other models
def create_fake_data(user,fake):
    # Create a fake workout
    workout = Workout(
        user=user,
        date=fake.date_between(start_date='-1y', end_date='today'),
        type=random.choice(['Running', 'Cycling', 'Yoga', 'Weightlifting']),
        duration=random.uniform(0.5, 2),
        intensity=random.choice(['Low', 'Medium', 'High']),
        calories_burned=random.randint(100, 800)
    )
    session.add(workout)

    # Create fake nutrition data
    nutrition = Nutrition(
        user=user,
        date=fake.date_between(start_date='-1y', end_date='today'),
        meal_type=random.choice(['Breakfast', 'Lunch', 'Dinner', 'Snack']),
        calories=random.randint(100, 500),
        protein=random.uniform(0, 30),
        carbohydrates=random.uniform(0, 50),
        fat=random.uniform(0, 20)
    )
    session.add(nutrition)

    # Create fake sleep data
    sleep = Sleep(
        user=user,
        date=fake.date_between(start_date='-1y', end_date='today'),
        start_time=datetime.now().time(),
        end_time=datetime.now().time(),
        quality=random.choice(['Poor', 'Average', 'Good', 'Excellent'])
    )
    session.add(sleep)

# Generate and insert fake data
for _ in range(10):
    try:
        # Begin a transaction
        with session.begin():
            fake_user = create_fake_user(fake)
            session.add(fake_user)
            create_fake_data(fake_user, fake)
    except Exception as e:
        # Rollback the transaction in case of an error
        session.rollback()
        print(f"An error occurred: {e}")

# Commit the session
session.commit()


# Creating an inspector object to inspect the database.
inspector = inspect(engine)
# Get list of table names
table_names = inspector.get_table_names()

# Iterating over each table and printing its contents.
for table_name in table_names:
    print(f"Contents of table {table_name}:")
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT * FROM {table_name}"))
        for row in result:
            print(row)
    print("\n") 