# Health and Fitness Tracking Database App

## Execution (Python)
These are commands for macOS:
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 models.py
python3 insert.py
python3 query.py
```

```bash
python3 test.py
```

## Overview
The Health and Fitness Tracking App is a comprehensive tool designed to assist individuals in monitoring and enhancing their wellness journey. Its primary objectives are to offer a personalized experience in tracking various health and fitness metrics and to provide actionable insights for users to achieve their fitness goals. The app is suitable for a wide range of users, from fitness enthusiasts to those beginning their health journey, and can be particularly beneficial for individuals seeking a structured approach to monitoring their lifestyle habits.



### Primary Objectives

- **Health Metrics Tracking**:  The app covers a broad spectrum of health and fitness metrics including workouts, nutrition, and sleep patterns. This holistic approach ensures users have a complete view of their health.

- **Personalized Recommendations**:Utilizing data entered by the user, the app provides personalized recommendations and feedback, helping users make informed decisions about their fitness routines and dietary habits.

 

### Target Audience
The app caters to a wide range of users, including:
- Fitness enthusiasts seeking a tool to monitor and optimize their routines.
- Individuals aiming to start or maintain a healthy lifestyle.
- People with specific health conditions who need to track their daily health metrics.

### Health and Fitness Metrics Tracked
- **Workouts**: Types of exercises, duration, intensity, and calories burned.
- **Nutrition**: Daily food intake, calorie count, and nutritional content.
- **Sleep**: Sleep duration, quality.
- **General Health Metrics**: Body weight, Height and Age 



## Files 
The project comprises the following files:
- `models.py`: Defines the database schema with tables for users, workouts, nutrition, and sleep .
- `insert.py`: Populates the database with sample data using the Faker library.
- `query.py`: Contains functions to query the database, providing insights into user data, workouts, nutrition, sleep patterns and gives recommendations based on it. 
- `test.py`: Runs unit tests, showing that all tables are created and the data is populated in the tables.  
- `schema.png`: a visual representation of the database schema. 
- `requirements.txt`: Contains all the required modules version to run the app 


## Database 
The database schema is defined in `models.py` and includes the following tables:

1. **User**: 
- Represents the users of the application.
- Attributes include id (primary key), name, email (unique identifier for each user), age, gender, height, and weight.
- This model is central to most queries. For example, when generating personalized reports or recommendations, the User model provides essential demographic information that might influence the type of workouts, nutritional needs, or sleep patterns.


2. **Workout**: 
- Captures details of users' physical activities.
- Includes id (primary key), user_id (foreign key linking to the User model), date of the workout, type (e.g., Running, Cycling), duration, intensity, and calories_burned.
- Queries involving this model are crucial for tracking physical activity. For instance, get_user_workouts retrieves all workouts for a specific user, helpful for monitoring fitness progress. `get_total_calories_burned` aggregates the calories burned over a time period, useful for weight management goals. `get_workout_recommendations` can analyze workout patterns to suggest changes for optimal fitness results.

3. **Nutrition**: 
- Focuses on dietary intake of users.
- Fields include id (primary key), user_id (foreign key), date, meal_type (Breakfast, Lunch, etc.), food_item, and nutritional details like calories, protein, carbohydrates, and fat.
- Queries using the Nutrition model, such as `get_total_nutrition`, provide insights into a user's daily nutritional intake, essential for diet management. The `get_average_calories` function computes the average calorie consumption, which is vital for understanding eating habits and making necessary dietary adjustments.

4. **Sleep**: 
- Records users' sleep data.
- Contains id (primary key), user_id (foreign key), date, start_time, end_time, and quality of sleep.
- Sleep data queries are integral to understanding rest patterns. `get_average_sleep_duration` calculates the average amount of sleep a user gets, which is crucial for assessing overall health and well-being. `get_sleep_recommendations` utilizes this data to provide advice on improving sleep quality, essential for good health and recovery.



### Normalization
The tables in the database have been reduced to 3NF

1. **1NF**: Each table (User, Workout, Nutrition, Sleep) adheres to the 1NF as each has a primary key (id), and all its attributes contain atomic values. There are no repeating groups or arrays. For instance, each column in the `User` table stores a single data type (integer, string, or float).

2. **2NF**: The design satisfies 2NF, which requires a database to be in 1NF and all attributes to be fully functionally dependent on the primary key. For instance, in the `Workout` table, all non-key attributes like `type`, `duration`, `intensity`, and `calories_burned` are fully dependent on the primary key (`id`). The `user_id` acts as a foreign key creating a link to the `User` table, ensuring no partial dependency of non-key attributes on a part of a primary key.

3. **Third Normal Form (3NF)**: And the design  follows 3NF by ensuring that it is in 2NF and all the attributes are non-transitively dependent on the primary key. For example, in the `Nutrition` table, attributes like `calories`, `protein`, `carbohydrates`, and `fat` are directly related to the `id` and not dependent on any non-prime attribute.

4. **Relationships and Integrity**: The use of foreign keys (like `user_id` in `Workout`, `Nutrition`, and `Sleep` tables) establishes a referential integrity constraint. It ensures relationships between tables are normalized by avoiding duplication of user data in each table. The `backref` property in relationships further enhances the relational aspect, allowing bidirectional access between User and its related data (Workout, Nutrition, Sleep).

5. **Modularity and Scalability**: By separating concerns into distinct tables, your database design is modular and scalable. Should there be a need to add more user attributes or introduce new aspects of workouts or nutrition, it can be done without major alterations to the existing table structure.

And to highlight again, The use of foreign keys, such as user_id in the Workout, Nutrition, and Sleep tables, elegantly ties these tables back to the User table, maintaining referential integrity and making  complex queries simpler to execute. 
You can also check the `schema.png` for better visualization on how everything connects to user id. 


### Indexing 
- **Primary Key Indexing:** Primary keys are indexed. This means each id field in your tables (User, Workout, Nutrition, Sleep) is  indexed. This indexing is crucial for efficient lookup, update, and delete operations based on the primary key.

-**Foreign Key Indexing:** We have index foreign key columns in relational databases for performance reasons. In our model, the user_id fields in the Workout, Nutrition, and Sleep tables are foreign keys referencing the User table. Indexing these  significantly improve the performance of join operations and queries that involve filtering or sorting based on user_id.

- **Additional Index:** When we have an index on a column, the database can use the index to quickly locate the data without having to scan the entire table. Like in our model, The date field in Workout, Nutrition, and Sleep tables are indexed to speed up queries filtering by date, such as in get_total_calories_burned and get_total_nutrition.


- We also avoid unnecessary indexing to reduce the amount of disk space being used.



### Transactions
In the `insert.py` file transactions are used during the insertion of fake data. The code executes each data insertion (creating a user and their corresponding workout, nutrition, and sleep records) within a transaction block (`with session.begin():`). This approach ensures atomicity, meaning all operations within a single transaction are either completely executed or rolled back in case of an error, as handled in the `try-except` block. If an exception occurs, `session.rollback()` is invoked to revert all changes made in that transaction, maintaining the database's consistency. 


