import os
import json
import traceback
from dotenv import load_dotenv
from openai import OpenAI
from interdisciplinary_lesson_plan import generate_interdisciplinary_lesson_plan

# Load environment variables
load_dotenv()

# Get OpenAI API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OpenAI API key not found in environment variables")

# Initialize OpenAI client with API key
client = OpenAI(api_key=api_key)

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

        # Create prompt for the API
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

        # Make the API request
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that creates detailed lesson plans. Always respond with valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000,
            response_format={ "type": "json_object" }
        )

        # Get the response content
        response_text = completion.choices[0].message.content.strip()

        # Parse the JSON response
        lesson_plan = json.loads(response_text)

        # Validate required keys in the JSON response
        required_keys = ["Main_Learning_Activity", "Specific_Learning_Activities", "Lesson_Plan", "Remarks"]
        for key in required_keys:
            if key not in lesson_plan:
                raise ValueError(f"Missing required key in lesson plan: {key}")

        return lesson_plan

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response text: {response_text}")
        return {
            "error": "Failed to parse the lesson plan response as JSON.",
            "details": str(e)
        }
    except Exception as e:
        print(f"Error generating lesson plan: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return {
            "error": "An unexpected error occurred while generating the lesson plan.",
            "details": str(e),
            "traceback": traceback.format_exc()
        }

def customize_lesson_plan(current_lesson_plan, customization, lesson_type=None):
    """
    Customize the provided lesson plan based on the customization instructions.
    
    :param current_lesson_plan: The existing lesson plan to be customized.
    :param customization: A dictionary of customization instructions.
    :param lesson_type: Optional; the type of lesson (e.g., 'regular', 'interdisciplinary').
    :return: The customized lesson plan.
    """
    try:
        # Example customization logic
        for key, value in customization.items():
            if key in current_lesson_plan:
                current_lesson_plan[key] = value

        # Optionally handle lesson_type-specific customization
        if lesson_type:
            current_lesson_plan['lesson_type'] = lesson_type

        return current_lesson_plan

    except Exception as e:
        raise ValueError(f"Error customizing the lesson plan: {str(e)}")
