from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OpenAI API key not found in environment variables")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.openai.com/v1"
)

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

    Example of Correct Interpretation:
    Main Learning Activity: "Use geometric principles to analyze bridge design"
    Valid Learning Outcomes:
    - "Apply geometric theorems to calculate bridge load distribution"
    - "Analyze structural stability using geometric relationships"
    - "Evaluate bridge design efficiency using geometric principles"

    Example of INCORRECT Interpretation:
    Main Learning Activity: "Use geometric principles to analyze bridge design"
    Invalid Learning Outcomes:
    - "Understand physics of bridge construction" (introduces concepts not in main activity)
    - "Create 3D models of bridges" (goes beyond analysis focus)
    - "Study different types of bridges" (deviates from geometric focus)

    1. Interdisciplinary Theme Generation (CRITICAL):
       - Theme MUST directly relate to the provided Main Learning Activity
       - MUST include Mathematics as one of the integrated disciplines
       - The mathematical concept chosen MUST be explicitly mentioned in or directly implied by the Main Learning Activity
       - Explicitly integrate Mathematics with at least one other discipline
       - Choose the most appropriate format for the theme based on the context:
         A. Question Format (emphasizing mathematical relationships):
            - "How can we use [mathematical concept] to [action] in [other discipline]?"
            - "How does [mathematical principle] enhance our understanding of [concept from other discipline]?"
            - "What role do [mathematical patterns/relationships] play in [other discipline context]?"
         B. Problem Statement Format (emphasizing interdependence):
            - "Design a solution that applies [mathematical concept] to solve [problem in other discipline]"
            - "Create a [product/system] that demonstrates how [mathematical principle] enables [other discipline process]"
            - "Develop a model showing how [mathematical concept] and [other discipline] interact to [achieve goal]"
       
       - Integration Requirements (CRITICAL):
         • Explicitly show how mathematics is ESSENTIAL to understanding the other discipline(s)
         • Demonstrate clear DEPENDENCY between mathematics and other discipline(s)
         • Show how removing either discipline would make the solution impossible
         
       - Integration Examples:
         • Mathematics + Physics: Using calculus to model motion
         • Mathematics + Biology: Using statistics to analyze population growth
         • Mathematics + Art: Using geometry to create perspective in drawings
         • Mathematics + Music: Using ratios to understand harmonics
         • Mathematics + Geography: Using trigonometry for mapping

    2. Learning Outcomes (CRITICAL ADHERENCE):
       - Each outcome MUST be a direct interpretation of the Main Learning Activity
       - NO outcomes should introduce concepts not present in the Main Learning Activity
       - Format Requirements:
         • Start with action verbs
         • Directly reference components from the Main Learning Activity
         • Show clear connection to mathematical concepts present in the activity
       
       Validation Questions for Each Outcome:
       • Can this outcome be directly traced to the Main Learning Activity?
       • Does it introduce any concepts not present in the Main Learning Activity?
       • Does it maintain the same focus and scope as the Main Learning Activity?

    3. Task Design Requirements (CRITICAL):
       - Every task MUST demonstrate interdependence:
         • Show how mathematical concepts are NECESSARY for the other discipline
         • Show how the other discipline PROVIDES CONTEXT for mathematics
         • Make it impossible to complete the task without both disciplines
       
       - Example Tasks:
         • "Create a scale model where geometric principles determine structural integrity"
         • "Develop a statistical analysis that reveals patterns in biological data"
         • "Design an experiment where mathematical modeling predicts physical outcomes"

    4. Assessment Criteria (CRITICAL):
       - Must assess BOTH:
         • Mathematical understanding
         • Other discipline knowledge
         • How they work together
       
       - Example Criteria:
         • "Mathematical model is applied to predict biological growth"
         • "Geometric principles are integrated into architectural design"
         • "Statistical analysis is used to validate experimental results"

    5. Strict Grade-Level Adherence:
       - Content explicitly suitable for grade level: {grade_level}
       - Theme format should be age-appropriate:
         • Lower grades (Form 1-3): Prefer question format for exploration
         • Middle grades (Form 4-6): Mix of questions and simple problem statements
         • Higher grades (Form 7-12): Can use more complex problem statements

    6. Strict Alignment with Provided Learning Activity:
       - Theme and content strictly derived from main learning activity: {main_learningactivity}
       - Format choice should enhance the learning activity's objectives

    7. Resource Suggestions:
       - Explicitly supporting interdisciplinary theme
       - Resources should match the chosen theme format

    8. Comprehensive Integration in ALL Lesson Plan Stages:
       - Introduction (Engage)
       - Competence Development (Explore, Explain)
       - Design (Elaborate)
       - Realisation (Evaluate)

    Lesson Duration: {lesson_duration} minutes

    Time Distribution:
    - Introduction: {time_distribution['introduction']} minutes
    - Competence Development: {time_distribution['competence_development']} minutes
    - Design: {time_distribution['design']} minutes
    - Realisation: {time_distribution['realisation']} minutes

    IMPORTANT: Use the following Remarks format (same as in lesson_plan.py):
    "Students were able to [what they were able to do] in relation to the specific activities enacted due to [provide reasons that enabled them to achieve e.g the use of interactive teaching and learning methods, and resources]. However, some students failed [If some students did not achieve the competences] to [list specific areas which were challenging]. Therefore, I will [provide mechanisms you will use to help these students e.g clarify it next period by using more examples.]"

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

    FINAL VALIDATION:
    Before returning the JSON, verify that:
    1. All Learning Outcomes can be traced back to the Main Learning Activity
    2. No new concepts have been introduced
    3. The scope matches exactly with the Main Learning Activity
    4. Mathematical integration is explicitly present in the Main Learning Activity

    Do not include any extra text. Return JSON only.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a professional interdisciplinary lesson planner."},
                  {"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000
    )

    response_text = response.choices[0].message.content.strip()
    response_text = response_text.replace("```json", "").replace("```", "").strip()

    try:
        lesson_plan = json.loads(response_text)
    except json.JSONDecodeError:
        response_text = re.sub(r'(\\w+):', r'"\\1":', response_text.replace("'", '"'))
        lesson_plan = json.loads(response_text)

    required_keys = ["Interdisciplinary_Theme", "Learning_Outcomes", "Resources", "Lesson_Plan", "Remarks"]
    for key in required_keys:
        if key not in lesson_plan:
            raise ValueError(f"Missing required key in lesson plan: {key}")

    return lesson_plan
