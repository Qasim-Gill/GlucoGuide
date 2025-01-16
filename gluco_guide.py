import streamlit as st
import anthropic

# API key for Claude AI
ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]

# Initialize Claude AI client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Function to get meal plans from Claude AI
def get_meal_plan(fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preferences):
    # Construct the prompt for Claude AI
    system_instruction = (
        "You are a world-class nutritionist. Based on the user's fasting sugar level, pre-meal sugar level, "
        "post-meal sugar level, and dietary preferences, generate a suitable meal plan. "
        "Be detailed about portions, timings, and ingredients, ensuring the meal plan is healthy and balanced."
    )

    user_prompt = (
        f"My fasting sugar level is {fasting_sugar} mg/dL, pre-meal sugar level is {pre_meal_sugar} mg/dL, "
        f"and post-meal sugar level is {post_meal_sugar} mg/dL. My dietary preferences are: {dietary_preferences}. "
        "Please suggest a detailed meal plan."
    )

    # Generate the response using Claude AI
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=250,
            temperature=0.7,
            system=system_instruction,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        }
                    ]
                }
            ]
        )
        return message.content  # Return the AI's response
    except Exception as e:
        return f"Error fetching meal plan: {e}"  # Handle API errors gracefully

# Streamlit app setup
st.title("🌟 GlucoGuide: Personalized Meal Planner for Diabetics 🌟")
st.write("""
Welcome to **GlucoGuide**, your trusted companion for managing diabetes. 
This app helps you track your sugar levels and provides personalized meal plans tailored to your dietary preferences and health needs. 
Stay healthy and in control with GlucoGuide!
""")

# Sidebar for user input
st.sidebar.header("Enter Your Details")

# Input fields
fasting_sugar = st.sidebar.number_input("Fasting Sugar Levels (mg/dL)", min_value=0, max_value=500, step=1, value=100)
pre_meal_sugar = st.sidebar.number_input("Pre-Meal Sugar Levels (mg/dL)", min_value=0, max_value=500, step=1, value=100)
post_meal_sugar = st.sidebar.number_input("Post-Meal Sugar Levels (mg/dL)", min_value=0, max_value=500, step=1, value=120)

# Dietary preferences
dietary_preference = st.sidebar.selectbox(
    "Dietary Preference",
    ["Vegetarian", "Non-Vegetarian", "Vegan", "Keto", "Low Carb"]
)

# Generate personalized meal plan button
if st.sidebar.button("Generate Meal Plan"):
    st.subheader("Your Personalized Meal Plan")
    
    # Fetch meal plan from Claude AI
    with st.spinner("Generating your meal plan..."):
        meal_plan = get_meal_plan(fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preference)
    
    # Display the response from Claude AI
    if "Error" not in meal_plan:
        st.success("Here's your personalized meal plan:")
        st.markdown(meal_plan)  # Display AI response
    else:
        st.error(meal_plan)  # Display error message if any

# Footer
st.write("---")
st.write("🔖 *This app is for informational purposes only. Consult your doctor for medical advice.*")
