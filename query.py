from models import *
from insert import  *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func,text
from datetime import datetime, date, timedelta

# Create engine and session
Session = sessionmaker(bind=engine)
session = Session()




# --- Workouts Training  ---

# Query 1
# Retrive all workout records for a user 
def get_user_workouts(user_id):
    return session.query(Workout).filter(Workout.user_id == user_id).all()

#Query 2
# Calculate the total calories burned by a user in a given month.
def get_total_calories_burned(user_id, year_month):
    return session.query(func.sum(Workout.calories_burned)).filter(Workout.user_id == user_id, func.strftime('%Y-%m', Workout.date) == year_month).scalar()

#Query 3
#Workout Recommendation 
def get_workout_recommendations(user_id):
    one_week_ago = datetime.now() - timedelta(days=7)
    # number of workouts in the last week
    workout_count = session.query(func.count(Workout.id)).filter(
        Workout.user_id == user_id,
        Workout.date >= one_week_ago).scalar()
    # Recommendations based on workout frequency
    if workout_count < 3:  # Assuming 3 is the threshold for low activity
        print("We recommend increasing your workout frequency. Aim for at least 3 workouts per week.")

    # Query for workout type distribution
    workout_types = session.query(Workout.type,func.count(Workout.id).label('count')).filter(Workout.user_id == user_id).group_by(Workout.type).all()
    # Recommendations based on workout variety
    if len(workout_types) == 1:
        print(f"You've been focusing a lot on {workout_types[0][0]} lately. How about trying different types of workouts for a balanced fitness routine?")




#--Nutrition Analysis --

#Query 4
# Get total nutritional intake for a specific date
def get_total_nutrition(user_id, specific_date):
    return session.query(func.sum(Nutrition.calories), func.sum(Nutrition.protein), func.sum(Nutrition.carbohydrates), func.sum(Nutrition.fat)).filter(Nutrition.user_id == user_id, Nutrition.date == specific_date).group_by(Nutrition.date).first()

#Query 5
#calculate the average daily calorie intake for a user
def get_average_calories(user_id):
    avg_calories = session.query(
        func.avg(Nutrition.calories).label('average_calories')
    ).filter(
        Nutrition.user_id == user_id
    ).scalar()
    return avg_calories

#Query 6
#Nutrition recommendations based on average calories intake
def get_nutrition_recommendations(user_id):
    avg_calories = get_average_calories(user_id)

    if avg_calories is not None:
        if avg_calories < 1800:  # Assuming 1800 is the minimum for this example
            print("Your average caloric intake is lower than usual. Consider increasing your calorie intake with nutrient-dense foods.")

    avg_protein, avg_carbs, avg_fats = session.query(
        func.avg(Nutrition.protein).label('average_protein'),
        func.avg(Nutrition.carbohydrates).label('average_carbs'),
        func.avg(Nutrition.fat).label('average_fats')
    ).filter(Nutrition.user_id == user_id).one()

    if avg_protein is not None and avg_protein < 50:  # Example threshold for protein
        print("You might need to increase your protein intake for better muscle recovery and growth.")

    if avg_carbs is not None and avg_carbs < 130:  # Example threshold for carbs
        print("Carbohydrates are important for energy. Consider incorporating more healthy carbs into your diet.")

    if avg_fats is not None and avg_fats < 44:  # Example threshold for fats
        print("Healthy fats are essential for your body. Try to include sources of healthy fats like avocados, nuts, and olive oil.")




# -- Sleep Tracking --

#Query 7
# Average Sleep Duration  
def get_average_sleep_duration(user_id):
    sleeps = session.query(Sleep.start_time, Sleep.end_time).filter(Sleep.user_id == user_id).all()

    total_sleep_duration = timedelta()
    count = 0
    for start_time, end_time in sleeps:
        # Handling the case where sleep crosses midnight
        if end_time < start_time:
            duration = (datetime.combine(date.min, end_time) + timedelta(days=1)) - datetime.combine(date.min, start_time)
        else:
            duration = datetime.combine(date.min, end_time) - datetime.combine(date.min, start_time)
        
        total_sleep_duration += duration
        count += 1
    # Calculate average sleep duration in seconds
    avg_sleep_duration = total_sleep_duration.total_seconds() / count if count > 0 else 0
    # Convert average sleep duration from seconds to hours
    avg_sleep_hours = avg_sleep_duration / 3600
    return avg_sleep_hours


#Query 8
#Sleep Recommendation for a user based on their avg sleep 
def get_sleep_recommendations(user_id):
    avg_sleep_hours = get_average_sleep_duration(user_id)

    if avg_sleep_hours < 7:  # Assuming 7 hours is the minimum recommended duration
        print("Your average sleep duration seems a bit low. Try to get at least 7 hours of sleep for better health and fitness results.")
    else:
        print("You are getting a healthy amount of sleep. Keep it up!")



# -- User Progress-- 

#Query 9 
def get_weight_changes(user_id):
    return session.query(Workout.date, User.weight).join(User).filter(User.id == user_id).order_by(Workout.date).all()




#--Sample Data for Testing -- 

current_user_id = 5 
year_month = '2023-04'  
specific_date = date(2023, 4, 15)  

# Query 1 - Retrieve all workout records for a user
workouts = get_user_workouts(current_user_id)
print("Query 1 - User Workouts:")
for workout in workouts:
    print(f"Date: {workout.date}, Type: {workout.type}, Duration: {workout.duration}, Calories Burned: {workout.calories_burned}")

# Query 2 - Calculate the total calories burned by a user in a given month
total_calories = get_total_calories_burned(current_user_id, year_month)
print(f"\nQuery 2 - Total calories burned in {year_month} for user {current_user_id}: {total_calories}")

# Query 3 - Workout Recommendations
print("\nQuery 3 - Workout Recommendations:")
get_workout_recommendations(current_user_id)

# Query 4 - Get total nutritional intake for a specific date
total_nutrition = get_total_nutrition(current_user_id, specific_date)
print("\nQuery 4 - Total Nutrition on Specific Date:")
if total_nutrition is not None:
    print(f"Calories: {total_nutrition[0]}, Protein: {total_nutrition[1]}, Carbohydrates: {total_nutrition[2]}, Fat: {total_nutrition[3]}")
else:
    print(f"No nutrition data found on {specific_date} for user {current_user_id}")

# Query 5 - Calculate the average daily calorie intake for a user
print("\nQuery 5 - Average Daily Calorie Intake:")
print(f"Average Calories: {get_average_calories(current_user_id)}")

# Query 6 - Nutrition Recommendations
print("\nQuery 6 - Nutrition Recommendations:")
get_nutrition_recommendations(current_user_id)

# Query 7 - Average Sleep Duration
avg_sleep_hours = get_average_sleep_duration(current_user_id)
print(f"\nQuery 7 - Average Sleep Duration: {avg_sleep_hours} hours")

# Query 8 - Sleep Recommendations
print("\nQuery 8 - Sleep Recommendations:")
get_sleep_recommendations(current_user_id)

# Query 9 - User Weight Changes
weight_changes = get_weight_changes(current_user_id)
print("\nQuery 9 - User Weight Changes:")
for date, weight in weight_changes:
    print(f"Date: {date}, Weight: {weight}")