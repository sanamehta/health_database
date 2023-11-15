#importing necessary modules and libraries 
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Creating a SQLite database engine for the health and fitness app.
engine = create_engine('sqlite:///health_fitness_app.db')

# Base class for declarative class definitions.
Base = declarative_base()

#User table.
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    age = Column(Integer)
    gender = Column(String)
    height = Column(Float)
    weight = Column(Float)

    #foreign key relationship backref 
    workouts = relationship('Workout', backref='user')
    nutritions = relationship('Nutrition', backref='user')
    sleeps = relationship('Sleep', backref='user')
    
# Workout table.
class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, index=True)
    type = Column(String)
    duration = Column(Float)
    intensity = Column(String)
    calories_burned = Column(Float)

# Nutrition Table 
class Nutrition(Base):
    __tablename__ = 'nutrition'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, index=True)
    meal_type = Column(String)
    food_item = Column(String)
    calories = Column(Float)
    protein = Column(Float)
    carbohydrates = Column(Float)
    fat = Column(Float)


#Sleep Table 
class Sleep(Base):
    __tablename__ = 'sleep'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, index=True)
    start_time = Column(Time)
    end_time = Column(Time)
    quality = Column(String)

# Creating all tables in the database.
Base.metadata.create_all(engine)
