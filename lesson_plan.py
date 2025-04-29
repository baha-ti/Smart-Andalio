import requests  # Assuming the deepseek API is accessed via HTTP requests
import os
import json
from dotenv import load_dotenv
from interdisciplinary_lesson_plan import generate_interdisciplinary_lesson_plan

# Load environment variables
load_dotenv()

# Initialize deepseek API key
api_key = os.getenv('DEEPSEEK_API_KEY')  # Replace with the correct key for the deepseek API
if not api_key:
    raise ValueError("Deepseek API key not found in environment variables")

# Define the base URL for the deepseek API
DEEPSEEK_API_URL = "https://api.deepseek.com/v1"  # Replace with the correct deepseek API endpoint

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

def generate_lesson_plan(main_learningactivity, grade_level, lesson_duration, time_distribution, lesson_type="regular"):
    """
    Generate a lesson plan (regular or project-based) based on the IDDR model and 5E approach.
    
    If lesson_type is interdisciplinary, this function delegates to generate_interdisciplinary_lesson_plan.
    Otherwise, it generates a single-discipline (regular or project) lesson plan.
    """
    try:
        # If interdisciplinary, forward to specialized function
        if lesson_type and lesson_type.lower() == 'interdisciplinary':
            return generate_interdisciplinary_lesson_plan(main_learningactivity, grade_level, lesson_duration, time_distribution)

        # Create prompt for the deepseek API
        prompt = f"""Create a detailed lesson plan for the following specifications:

Main Learning Activity: {main_learningactivity}
Grade Level: {grade_level}
Lesson Duration: {lesson_duration} minutes
Lesson Type: {lesson_type}

Time Distribution:
- Introduction: {time_distribution['introduction']} minutes
- Competence Development: {time_distribution['competence_development']} minutes
- Design: {time_distribution['design']} minutes
- Realisation: {time_distribution['realisation']} minutes

The lesson plan should follow the IDDR model and 5E's approach:
1. Introduction (Engage) - Variation Principle: CONTRAST
2. Competence Development (Explore/Explain) - Variation Principle: SEPARATION
3. Design (Elaborate) - Variation Principle: GENERALIZATION
4. Realisation (Evaluate) - Variation Principle: FUSION

Return valid JSON only. Do not include any extra text."""

        # Prepare the request payload
        payload = {
            "model": "r1",  # Assuming "r1" is the correct model for deepseek
            "prompt": prompt,
            "temperature": 0.7,
            "max_tokens": 2000
        }

        # Make the API request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(f"{DEEPSEEK_API_URL}/generate", headers=headers, json=payload)

        # Check for a successful response
        if response.status_code != 200:
            raise ValueError(f"Deepseek API request failed with status code {response.status_code}: {response.text}")

        # Parse the response JSON
        response_text = response.json().get("choices", [{}])[0].get("text", "").strip()

        # Clean up and validate the JSON response
        try:
            lesson_plan = json.loads(response_text)
        except json.JSONDecodeError:
            # Attempt to fix malformed JSON
            response_text = re.sub(r'(\\w+):', r'"\\1":', response_text.replace("'", '"'))
            lesson_plan = json.loads(response_text)

        # Validate required keys in the JSON response
        required_keys = ["Main_Learning_Activity", "Specific_Learning_Activities", "Lesson_Plan", "Remarks"]
        for key in required_keys:
            if key not in lesson_plan:
                raise ValueError(f"Missing required key in lesson plan: {key}")

        return lesson_plan

    except Exception as e:
        print(f"Error generating lesson plan: {e}")
        return {
            "error": "An unexpected error occurred while generating the lesson plan.",
            "details": str(e)
        }
