import gradio as gr

def calculate_bmi(weight, feet, inches):
    # Convert height to meters (1 foot = 0.3048 meters, 1 inch = 0.0254 meters)
    height_in_meters = (feet * 0.3048) + (inches * 0.0254)
    
    # Calculate BMI
    bmi = weight / (height_in_meters ** 2)
    
    # Return BMI category
    if bmi < 18.5:
        return f"Your BMI is {bmi:.2f}. You are underweight."
    elif 18.5 <= bmi < 24.9:
        return f"Your BMI is {bmi:.2f}. You have a normal weight."
    else:
        return f"Your BMI is {bmi:.2f}. You are overweight."

# Create the Gradio interface with a title and custom layout
interface = gr.Interface(
    fn=calculate_bmi,
    inputs=[
        gr.Number(label="Weight (kg)"),  # Input for weight
        gr.Number(label="Feet"),         # Input for feet
        gr.Number(label="Inches")        # Input for inches
    ],
    outputs="text",
    title="BMI Calculator",
    description="Enter your weight in kilograms (kg), height in feet, and inches. Click 'Submit' to calculate your BMI.",
    live=False  # This will require user to click "Submit" button to trigger the function
)

# Launch the interface
interface.launch()
