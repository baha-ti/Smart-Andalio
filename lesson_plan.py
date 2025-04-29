# Save this as lesson_plan.py

from openai import OpenAI
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

client = OpenAI(
    api_key=api_key,
    base_url="https://api.openai.com/v1"
)

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

        # Create prompt for the OpenAI API
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

CRITICAL INSTRUCTIONS FOR LESSON TYPE: {lesson_type.upper()}

{'''
REGULAR LESSON REQUIREMENTS:
1. Adherence to Existing Conditions:
   - Strictly follow all existing lesson plan conditions
   - Maintain the provided learning activity exactly as specified
   - Ensure grade-level appropriateness
   - Follow established lesson plan structure
   - Adhere to curriculum standards

2. Single-Discipline Focus:
   - Maintain content strictly within a single discipline
   - DO NOT introduce any interdisciplinary elements
   - Focus on depth of understanding within the specific subject
   - Develop subject-specific skills and knowledge

3. Real-life Examples and Activities:
   - Integrate relevant real-life examples specific to the discipline
   - Ensure examples are age-appropriate and contextually relevant
   - Include practical activities that demonstrate real-world applications
   - Use examples students can easily relate to

4. Validation and Adjustment:
   - Validate that all content strictly matches teacher-provided activity, specified grade level, single-discipline focus
   - Immediately adjust if the lesson deviates

5. Stage-Specific Requirements:
   - INTRODUCTION:
     • Engage with discipline-specific content
     • Use real-world examples
     • Set clear learning objectives
   - COMPETENCE DEVELOPMENT:
     • Develop subject-specific knowledge with guided practice
   - DESIGN:
     • Deepen understanding of the subject
     • Include practice exercises with feedback
   - REALISATION:
     • Final tasks that demonstrate subject mastery
     • Evaluate subject-specific understanding

6. Assessment Criteria Format:
   - Strictly reflect the tasks students perform
   - If a student task is to define a function, the criterion is: a function is defined
   - All in passive present tense, no qualifiers like 'correctly' or 'properly'

7. Return the plan in JSON format with:
   • "Main_Learning_Activity"
   • "Specific_Learning_Activities" with sub-activities
   • "Lesson_Plan" with IDDR + 5E stages
   • "Remarks" as a single list
''' if lesson_type and lesson_type.lower() == 'regular' else ''}

{'''
PROJECT-BASED LESSON REQUIREMENTS:
1. Design an extended, hands-on project that spans multiple sessions
2. Include clear project goals, deliverables, and success criteria
3. Incorporate student choice and autonomy
4. Focus on problem-solving and critical thinking
5. Use rubrics for project assessment
6. Real-world applications and connections
7. Collaboration and teamwork
''' if lesson_type and lesson_type.lower() == 'project' else ''}

The lesson plan should follow the IDDR model and 5E's approach:
1. Introduction (Engage) - Variation Principle: CONTRAST
2. Competence Development (Explore/Explain) - Variation Principle: SEPARATION
3. Design (Elaborate) - Variation Principle: GENERALIZATION
4. Realisation (Evaluate) - Variation Principle: FUSION

Return valid JSON only. Do not include any extra text."""
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional lesson planner. Your task is to create "
                        "detailed lesson plans following the IDDR model and 5E's approach. "
                        "Always return valid JSON."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        response_text = response.choices[0].message.content.strip()
        
        # Clean up the response text
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        
        try:
            lesson_plan = json.loads(response_text)
            
            # Validate keys
            required_keys = ["Main_Learning_Activity", "Specific_Learning_Activities", "Lesson_Plan", "Remarks"]
            for key in required_keys:
                if key not in lesson_plan:
                    raise ValueError(f"Missing required key in lesson plan: {key}")
            
            # Ensure key sections exist
            if "Specific_Learning_Activities" not in lesson_plan:
                lesson_plan["Specific_Learning_Activities"] = {}
            
            if "Lesson_Plan" not in lesson_plan:
                lesson_plan["Lesson_Plan"] = []
            
            if "Remarks" not in lesson_plan:
                lesson_plan["Remarks"] = []
            
            # Make sure Teaching Activities are teacher-focused (not starting with 'Students')
            for stage in lesson_plan.get("Lesson_Plan", []):
                if "Teaching Activities" in stage:
                    teaching_activities = stage["Teaching Activities"]
                    if teaching_activities.lower().startswith("students"):
                        teaching_activities = teaching_activities[8:].strip()
                        teaching_activities = teaching_activities[0].upper() + teaching_activities[1:]
                        stage["Teaching Activities"] = teaching_activities
            
            return lesson_plan

        except json.JSONDecodeError as e:
            print(f"Initial JSON parsing failed: {str(e)}")
            print(f"Raw response: {response_text}")
            
            # Try cleanup
            response_text = response_text.replace("'", '"')  
            response_text = re.sub(r'(\\w+):', r'\"\\1\":', response_text)
            response_text = re.sub(r',\\s*}', '}', response_text)
            response_text = re.sub(r',\\s*]', ']', response_text)
            
            try:
                lesson_plan = json.loads(response_text)
                # Validate again
                required_keys = ["Main_Learning_Activity", "Specific_Learning_Activities", "Lesson_Plan", "Remarks"]
                for key in required_keys:
                    if key not in lesson_plan:
                        raise Exception(f"Missing required key in lesson plan: {key}")
                return lesson_plan
            except json.JSONDecodeError as e:
                print(f"Second JSON parsing attempt failed: {str(e)}")
                print(f"Cleaned response: {response_text}")
                
                return {
                    "Main_Learning_Activity": main_learningactivity,
                    "Specific_Learning_Activities": {
                        "1": {
                            "Activity": "Activity related to " + main_learningactivity,
                            "Features": ["Feature 1", "Feature 2"]
                        }
                    },
                    "Lesson_Plan": [
                        {
                            "Stage": "Introduction",
                            "Time (Minutes)": time_distribution['introduction'],
                            "Teaching Activities": f"Show examples related to {main_learningactivity}",
                            "Learning Activities": "Activity 1",
                            "Assessment Criteria": "Criterion 1",
                            "Variation Principle": "CONTRAST",
                            "5E Component": "Engage"
                        }
                    ],
                    "Remarks": [
                        "Error occurred while generating the full lesson plan. Simplified version provided."
                    ]
                }
        
        except Exception as e:
            print(f"Error generating lesson plan: {str(e)}")
            return {
                "Main_Learning_Activity": main_learningactivity,
                "Specific_Learning_Activities": {
                    "1": {
                        "Activity": "Activity related to " + main_learningactivity,
                        "Features": ["Feature 1", "Feature 2"]
                    }
                },
                "Lesson_Plan": [
                    {
                        "Stage": "Introduction",
                        "Time (Minutes)": time_distribution['introduction'],
                        "Teaching Activities": f"Show examples related to {main_learningactivity}",
                        "Learning Activities": "Activity 1",
                        "Assessment Criteria": "Criterion 1",
                        "Variation Principle": "CONTRAST",
                        "5E Component": "Engage"
                    }
                ],
                "Remarks": [
                    "Error occurred while generating the full lesson plan. Simplified version provided."
                ]
            }

    except Exception as e:
        print(f"Error generating lesson plan: {str(e)}")
        return {
            "Main_Learning_Activity": main_learningactivity,
            "Specific_Learning_Activities": {
                "1": {
                    "Activity": "Activity related to " + main_learningactivity,
                    "Features": ["Feature 1", "Feature 2"]
                }
            },
            "Lesson_Plan": [
                {
                    "Stage": "Introduction",
                    "Time (Minutes)": time_distribution['introduction'],
                    "Teaching Activities": f"Show examples related to {main_learningactivity}",
                    "Learning Activities": "Activity 1",
                    "Assessment Criteria": "Criterion 1",
                    "Variation Principle": "CONTRAST",
                    "5E Component": "Engage"
                }
            ],
            "Remarks": [
                "Error occurred while generating the full lesson plan. Simplified version provided."
            ]
        }

def customize_lesson_plan(current_lesson_plan, customization, lesson_type=None):
    """
    Customize an existing lesson plan based on user requests.
    This function calls the OpenAI API to adjust the existing plan
    according to the user's customization request, then returns
    a new or updated JSON lesson plan.
    """
    print(f"Customizing lesson plan with request: {customization}")
    
    try:
        if not isinstance(current_lesson_plan, dict):
            return {"Error": "Invalid lesson plan format"}
        
        if not isinstance(customization, str):
            return {"Error": "Invalid customization request"}
        
        original_main_activity = current_lesson_plan.get("Main_Learning_Activity", "")
        
        prompt = f"""Modify the following lesson plan based on this request: "{customization}"

        Current Lesson Plan:
        {json.dumps(current_lesson_plan, indent=2)}

        Lesson Type: {lesson_type if lesson_type else "regular"}
        
        CRITICAL INSTRUCTIONS:
        1. Keep the Main_Learning_Activity exactly as it is: \"{original_main_activity}\"
        2. Do not remove keys: \"Main_Learning_Activity\", \"Specific_Learning_Activities\", \"Lesson_Plan\", \"Remarks\"
        3. Maintain IDDR + 5E structure
        4. Keep assessment criteria in passive voice, present tense
        5. Return valid JSON only, with no extra text
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional lesson planner. Your task is to create or modify "
                        "detailed lesson plans following the IDDR model and the 5E approach."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        response_text = response.choices[0].message.content.strip()
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        
        try:
            customized_plan = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"JSON parsing failed: {str(e)}\nRaw response: {response_text}")
            # Attempt basic cleanup
            cleaned_text = response_text.replace("'", '"')
            cleaned_text = re.sub(r'(\\w+):', r'\"\\1\":', cleaned_text)
            cleaned_text = re.sub(r',\\s*}', '}', cleaned_text)
            cleaned_text = re.sub(r',\\s*]', ']', cleaned_text)
            customized_plan = json.loads(cleaned_text)
        
        required_keys = ["Main_Learning_Activity", "Specific_Learning_Activities", "Lesson_Plan", "Remarks"]
        for key in required_keys:
            if key not in customized_plan:
                raise Exception(f"Missing required key in lesson plan: {key}")
        
        # Make sure the Main_Learning_Activity remains unchanged
        customized_plan["Main_Learning_Activity"] = original_main_activity
        
        # Ensure minimal structure is present
        if "Specific_Learning_Activities" not in customized_plan:
            customized_plan["Specific_Learning_Activities"] = {}
        if "Lesson_Plan" not in customized_plan:
            customized_plan["Lesson_Plan"] = []
        if "Remarks" not in customized_plan:
            customized_plan["Remarks"] = []
        
        return customized_plan

    except Exception as e:
        print(f"Error customizing lesson plan: {str(e)}")
        return {"Error": f"Could not customize lesson plan: {str(e)}"}
