# Save this as lesson_plan.py

import openai  # Correct import for the OpenAI library
import os
import json
from dotenv import load_dotenv
import re
from interdisciplinary_lesson_plan import generate_interdisciplinary_lesson_plan

# Load environment variables
load_dotenv()

# Debug: Print environment details
print(f"Current working directory: {os.getcwd()}")
print(f"Environment file path: {os.path.join(os.getcwd(), '.env')}")

# Initialize the OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key loaded: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"API Key starts with: {api_key[:7]}...")

if not api_key:
    raise ValueError("OpenAI API key not found in environment variables")

# Set the OpenAI API key
openai.api_key = api_key

def calculate_time_distribution(lesson_duration, grade_level):
    """
    Calculate time distribution for different stages based on grade level.
    Returns a dictionary with time allocations for each stage.
    """
    try:
        lesson_duration = int(lesson_duration)
    except (ValueError, TypeError):
        raise ValueError("Lesson duration must be a number")
    
    # Base time distribution
    time_distribution = {
        "introduction": 0.15 * lesson_duration,     # 15% of total time
        "competence_development": 0.40 * lesson_duration,  # 40% of total time
        "design": 0.25 * lesson_duration,           # 25% of total time
        "realisation": 0.20 * lesson_duration       # 20% of total time
    }
    
    # Adjust for certain grade levels
    if grade_level.lower() in ["form1", "form2", "form3"]:
        # More time for introduction and competence development for younger grades
        time_distribution["introduction"] *= 1.2
        time_distribution["competence_development"] *= 1.1
        time_distribution["design"] *= 0.9
        time_distribution["realisation"] *= 0.8
    elif grade_level.lower() in ["form4", "form5", "form6"]:
        # Balanced distribution for middle grades
        pass
    else:
        # More time for design and realisation for older grades
        time_distribution["introduction"] *= 0.8
        time_distribution["competence_development"] *= 0.9
        time_distribution["design"] *= 1.1
        time_distribution["realisation"] *= 1.2
    
    # Round to nearest minute
    for stage in time_distribution:
        time_distribution[stage] = round(time_distribution[stage])
    
    return time_distribution
