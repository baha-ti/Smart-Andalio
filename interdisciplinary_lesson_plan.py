import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get OpenAI API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OpenAI API key not found in environment variables")

# Initialize OpenAI client with API key
client = OpenAI(api_key=api_key)

def generate_interdisciplinary_lesson_plan(main_learningactivity, grade_level, lesson_duration, time_distribution):
    """
    Generates an interdisciplinary lesson plan using the OpenAI API.
    
    Args:
        main_learningactivity (str): The main learning activity or topic
        grade_level (str): The grade level of the students
        lesson_duration (int): Duration of the lesson in minutes
        time_distribution (dict): Dictionary containing time allocation for different stages
        
    Returns:
        dict: The generated lesson plan
    """
    try:
        # Create prompt for the API
        prompt = f"""Create an interdisciplinary lesson plan for the following specifications:

Main Learning Activity: {main_learningactivity}
Grade Level: {grade_level}
Lesson Duration: {lesson_duration} minutes

Time Distribution:
- Introduction: {time_distribution['introduction']} minutes
- Competence Development: {time_distribution['competence_development']} minutes
- Design: {time_distribution['design']} minutes
- Realisation: {time_distribution['realisation']} minutes

The lesson plan should:
1. Integrate multiple disciplines
2. Follow the IDDR model and 5E's approach
3. Include clear learning objectives for each discipline
4. Specify how the disciplines are interconnected
5. Provide assessment methods for each discipline

Return valid JSON only. Do not include any extra text."""

        # Make the API request
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that creates detailed interdisciplinary lesson plans. Always respond with valid JSON."
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
        required_keys = ["Main_Learning_Activity", "Integrated_Disciplines", "Learning_Objectives", "Lesson_Plan", "Assessment_Methods", "Remarks"]
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
        print(f"Error generating interdisciplinary lesson plan: {e}")
        return {
            "error": "An unexpected error occurred while generating the interdisciplinary lesson plan.",
            "details": str(e)
        }
