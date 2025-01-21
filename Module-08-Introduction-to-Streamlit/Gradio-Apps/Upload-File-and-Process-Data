import gradio as gr
import pandas as pd

# Function to calculate BMI
def calculate_bmi(weight, height):
    height_in_meters = height / 100  # Convert cm to meters
    bmi = weight / (height_in_meters ** 2)
    
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
    else:
        category = "Overweight"
    
    return bmi, category

# Function to estimate daily calorie intake based on activity level
def calorie_intake(age, gender, weight, height, activity_level):
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    activity_multiplier = {
        "Sedentary": 1.2,
        "Lightly active": 1.375,
        "Moderately active": 1.55,
        "Very active": 1.725,
        "Super active": 1.9
    }
    
    calories_needed = bmr * activity_multiplier[activity_level]
    return calories_needed

# Function to read the CSV file and calculate BMI & Calorie Intake for each user
def process_csv(file):
    df = pd.read_csv(file.name)
    results = []
    
    for _, row in df.iterrows():
        name = row["Name"]
        age = row["Age"]
        gender = row["Gender"]
        height = row["Height_cm"]
        weight = row["Weight_kg"]
        activity_level = row["Activity_Level"]
        
        bmi, bmi_category = calculate_bmi(weight, height)
        calories = calorie_intake(age, gender, weight, height, activity_level)
        
        results.append({
            "Name": name,
            "BMI": f"{bmi:.2f}",
            "BMI Category": bmi_category,
            "Daily Calorie Needs (kcal)": f"{calories:.0f}",
        })
    
    return pd.DataFrame(results)

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Personal Health Tracker")
    gr.Markdown("### Upload your CSV file to calculate BMI and daily calorie needs for each person. format should be: Name,Age,Gender,Height_cm,Weight_kg,Activity_Level")
    
    # File Upload
    file_upload = gr.File(label="Upload CSV File", type="filepath")
    
    # Output for the result
    output = gr.DataFrame(headers=["Name", "BMI", "BMI Category", "Daily Calorie Needs (kcal)"])
    
    # Button to trigger processing
    process_button = gr.Button("Process CSV")
    
    # Function trigger
    process_button.click(fn=process_csv, inputs=[file_upload], outputs=[output])

# Launch the app
demo.launch()
