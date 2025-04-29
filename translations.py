"""
English-Swahili translations for educational terminology used in lesson plans.
This file contains translations for common educational terms, assessment criteria,
and lesson plan components.
"""

EDUCATIONAL_TRANSLATIONS = {
    # Lesson Plan Components
    "Smart Lesson Plan": "Andalio la Somo Janja",
    "Main Learning Activity": "Shughuli Kuu ya Ujifunzaji",
    "Specific Learning Activities": "Shughuli Mahususi za Ujifunzaji",
    "Lesson Plan": "Andalio la Somo",
    "Teaching Activities": "Shughuli za Ufundishaji",
    "Learning Activities": "Shughuli za Ujifunzaji",
    "Assessment Criteria": "Vigezo vya Upimaji",
    "Remarks": "Tathmini ya Mwalimu",
    "Resources": "Vitendea kazi",
    "Time": "Muda",
    "Minutes": "Dakika",
    
    # Assessment Terms
    "is analyzed": "inachambuliwa",
    "is created": "inaundwa",
    "is designed": "inabuniwa",
    "is demonstrated": "inaonyeshwa",
    "is explained": "inaelezwa",
    "is identified": "inatambuliwa",
    "is measured": "inapimwa",
    "is observed": "inatazamwa",
    "is performed": "inafanywa",
    "is presented": "inawasilishwa",
    "is solved": "inatatuliwa",
    "is used": "inatumiwa",
    
    # Educational Verbs
    "analyze": "chambua",
    "apply": "tumia",
    "assess": "tathmini",
    "calculate": "Kokotoa",
    "compare": "linganisha",
    "create": "unda",
    "demonstrate": "onyesha",
    "design": "buni",
    "develop": "endeleza",
    "evaluate": "tathmini",
    "explain": "eleza",
    "identify": "baini",
    "implement": "tekeleza",
    "measure": "pima",
    "observe": "tazama",
    "perform": "fanya",
    "present": "wasilisha",
    "solve": "tatua",
    "use": "tumia",
    
    # Educational Nouns
    "activity": "shughuli",
    "assessment": "upimaji",
    "competence": "ujuzi",
    "concept": "dhana",
    "criteria": "vigezo",
    "demonstration": "maonyesho",
    "design": "kuunda",
    "development": "kuendeleza",
    "evaluation": "tathmini",
    "example": "mfano",
    "exercise": "zoezi",
    "experiment": "jaribio",
    "implementation": "utekelezaji",
    "learning": "ujifunzaji",
    "measurement": "kipimo",
    "method": "mbinu",
    "observation": "utazamaji",
    "performance": "utendaji",
    "presentation": "wasilisho",
    "problem": "tatizo",
    "project": "mradi",
    "resource": "rasilimali",
    "solution": "ufumbuzi",
    "task": "kazi",
    "technique": "mbinu",
    "tool": "chombo",
    "introduction": "utangulizi",
    "competence development": "kuendeleza ujuzi",
    "design [one of the lesson plan stages]": "Kubuni",
    "Realize [one of the lesson plan stages]": "Tekeleza",
    "variation [in teaching and learning]": "Mabadiliko ya shughuli",
    
    # Educational Adjectives
    "accurate": "sahihi",
    "appropriate": "sahihi",
    "clear": "wazi",
    "complete": "kamili",
    "correct": "sahihi",
    "effective": "bora",
    "efficient": "ufanisi",
    "proper": "sahihi",
    "relevant": "husika",
    "specific": "mahususi",
    "suitable": "sahihi",
    "useful": "muhimu",
    
    # Common Phrases
    "Students were able to": "Wanafunzi waliweza",
    "However, some students failed": "Hata hivyo, baadhi ya wanafunzi hawakuweza",
    "Therefore, I will": "Kwa hivyo, nitafanya",
    "in relation to": "kuhusiana na",
    "due to": "kutokana na",
    "the use of": "matumizi ya",
    "teaching and learning methods": "mbinu za kufundishia na kujifunzia",
    "interactive": "shirikishi",
    "next period": "kipindi kijacho",
    "by using": "kwa kutumia",
    "more examples": "mifano zaidi",
    "specific areas": "maeneo mahususi",
    "which were challenging": "ambayo yalikuwa magumu",
    "to help these students": "kuwasaidia wanafunzi hawa",
    "to achieve": "kufanikiwa",
    "to understand": "kuelewa",
    "to demonstrate": "kuonyesha",
    "to apply": "kutumia",
    "to create": "kuunda",
    "to design": "kubuni",
    "to develop": "kuendeleza",
    "to evaluate": "kutathmini",
    "to explain": "kueleza",
    "to identify": "kubaini",
    "to implement": "kutekeleza",
    "to measure": "kupima",
    "to observe": "kutazama",
    "to perform": "kufanya",
    "to present": "kuwasilisha",
    "to solve": "kutatua",
    "to use": "kutumia",
    "contrast": "linganisha",
    "separate": "tenganisha",
    "generalisaze": "hitimisha",
    "fusion": "unganisha"
}

def translate_educational_term(english_term):
    """
    Translate an educational term from English to Swahili.
    Returns the Swahili translation if found, otherwise returns the original English term.
    
    Note: This function only handles English-to-Swahili translations.
    """
    return EDUCATIONAL_TRANSLATIONS.get(english_term, english_term)

def translate_educational_text(english_text):
    """
    Translate educational text from English to Swahili.
    Attempts to translate each word while preserving the structure.
    Returns the translated text.
    
    Note: This function only handles English-to-Swahili translations.
    """
    words = english_text.split()
    translated_words = [translate_educational_term(word) for word in words]
    return ' '.join(translated_words) 