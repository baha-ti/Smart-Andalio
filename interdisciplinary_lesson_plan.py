import openai  # Correct import for the OpenAI library
import os
import json
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Initialize OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OpenAI API key not found in environment variables")

# Set the OpenAI API key
openai.api_key = api_key

def generate_interdisciplinary_lesson_plan(main_learningactivity, grade_level, lesson_duration, time_distribution):
    prompt = f"""
    Create a detailed interdisciplinary lesson plan strictly adhering to these standards:

    CRITICAL - MAIN LEARNING ACTIVITY INTERPRETATION:
    Main Learning Activity provided: "{main_learningactivity}"
    
    Rules for Main Learning Activity Interpretation (STRICT ADHERENCE REQUIRED):
    1. Learning Outcomes MUST be directly derived from this Main Learning Activity
    2. DO NOT introduce concepts that are not implied by the Main Learning Activity
    3. DO NOT deviate from or expand beyond the scope of the Main Learning Activity
    4. Break down the Main Learning Activity into its core components to create outcomes
    5. Each Learning Outcome must be traceable back to the Main Learning Activity

    Lesson Duration: {lesson_duration} minutes

    Time Distribution:
    - Introduction: {time_distribution['introduction']} minutes
    - Competence Development: {time_distribution['competence_development']} minutes
    - Design: {time_distribution['design']} minutes
    - Realisation: {time_distribution['realisation']} minutes

    Output JSON format strictly:
    {{
        "Interdisciplinary_Theme": {{
            "Format": "question" or "problem_statement",
            "Content": "Theme that directly relates to the Main Learning Activity",
            "Integrated_Disciplines": ["Mathematics", "Other Discipline"],
            "Rationale": "Explanation showing direct connection to Main Learning Activity"
        }},
        "Learning_Outcomes": [
            "Outcomes that are direct interpretations of the Main Learning Activity",
            "No outcomes that introduce concepts beyond the Main Learning Activity"
        ],
        "Resources": ["Resource 1 supporting mathematical integration", "Resource 2"],
        "Lesson_Plan": [
            {{
                "Stage": "Introduction",
                "Time (Minutes)": "{time_distribution['introduction']}",
                "Teaching Activities": "Activities showing discipline integration",
                "Learning Activities": "Tasks requiring both disciplines",
                "Assessment Criteria": "Criteria showing integration",
                "Variation Principle": "CONTRAST",
                "5E Component": "Engage"
            }},
            {{
                "Stage": "Competence Development",
                "Time (Minutes)": "{time_distribution['competence_development']}",
                "Teaching Activities": "...",
                "Learning Activities": "...",
                "Assessment Criteria": "...",
                "Variation Principle": "SEPARATION",
                "5E Component": "Explore, Explain"
            }},
            {{
                "Stage": "Design",
                "Time (Minutes)": "{time_distribution['design']}",
                "Teaching Activities": "...",
                "Learning Activities": "...",
                "Assessment Criteria": "...",
                "Variation Principle": "GENERALIZATION",
                "5E Component": "Elaborate"
            }},
            {{
                "Stage": "Realisation",
                "Time (Minutes)": "{time_distribution['realisation']}",
                "Teaching Activities": "...",
                "Learning Activities": "...",
                "Assessment Criteria": "...",
                "Variation Principle": "FUSION",
                "5E Component": "Evaluate"
            }}
        ],
        "Remarks": [
            "Students were able to [what they were able to do] in relation to the specific activities enacted due to [provide reasons that enabled them to achieve e.g the use of interactive teaching and learning methods, and resources]. However, some students failed [If some students did not achieve the competences] to [list specific areas which were challenging]. Therefore, I will [provide mechanisms you will use to help these students e.g clarify it next period by using more examples.]"
        ]
    }}
    """

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional interdisciplinary lesson planner."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )

    response_text = response.choices[0].message.content.strip()
    response_text = response_text.replace("```json", "").replace("```", "").strip()

    try:
        lesson_plan = json.loads(response_text)
    except json.JSONDecodeError:
        # Attempt to fix malformed JSON
        response_text = re.sub(r'(\\w+):', r'"\\1":', response_text.replace("'", '"'))
        lesson_plan = json.loads(response_text)

    # Validate required keys in the JSON response
    required_keys = ["Interdisciplinary_Theme", "Learning_Outcomes", "Resources", "Lesson_Plan", "Remarks"]
    for key in required_keys:
        if key not in lesson_plan:
            raise ValueError(f"Missing required key in lesson plan: {key}")

    return lesson_plan
