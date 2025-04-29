# Save this as app.py

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests  # for catching network/connection errors if needed
from lesson_plan import generate_lesson_plan, customize_lesson_plan, calculate_time_distribution
from interdisciplinary_lesson_plan import generate_interdisciplinary_lesson_plan

load_dotenv()  # Load environment variables

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# For session management, ensure you have a secure, persistent secret key in production
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    # Render your index or UI page
    return render_template('index.html')

@app.route('/generate_lesson_plan', methods=['POST'])
def generate_lesson_plan_route():
    try:
        # Ensure request is JSON
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400

        data = request.get_json()

        # Update required fields to match new frontend field name
        required_fields = ['main_learning_activity', 'grade_level', 'lesson_duration', 'lesson_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Calculate time distribution
        time_distribution = calculate_time_distribution(data['lesson_duration'], data['grade_level'])

        # Decide whether to generate an interdisciplinary or regular lesson plan
        if data['lesson_type'].lower() == 'interdisciplinary':
            lesson_plan = generate_interdisciplinary_lesson_plan(
                main_learningactivity=data['main_learning_activity'],  # Updated field name
                grade_level=data['grade_level'],
                lesson_duration=data['lesson_duration'],
                time_distribution=time_distribution
            )
        else:
            lesson_plan = generate_lesson_plan(
                main_learningactivity=data['main_learning_activity'],  # Updated field name
                grade_level=data['grade_level'],
                lesson_duration=data['lesson_duration'],
                time_distribution=time_distribution,
                lesson_type=data['lesson_type']
            )

        return jsonify(lesson_plan)

    except requests.exceptions.RequestException as net_err:
        # Add more detailed error logging
        print(f"[Network Error in generate_lesson_plan_route]: {str(net_err)}")
        return jsonify({
            'error': 'A network error occurred while generating the lesson plan. '
                     'Please check your internet connection or try again later.',
            'details': str(net_err)
        }), 503

    except ValueError as val_err:
        print(f"[ValueError in generate_lesson_plan_route]: {str(val_err)}")
        return jsonify({
            'error': str(val_err),
            'details': 'Invalid input provided'
        }), 400

    except Exception as e:
        print(f"[Error in generate_lesson_plan_route]: {str(e)}")
        return jsonify({
            'error': 'An unexpected error occurred while generating the lesson plan. Please try again.',
            'details': str(e)
        }), 500

@app.route('/customize_lesson_plan', methods=['POST'])
def customize_lesson_plan_route():
    try:
        # Ensure request is JSON
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400

        data = request.get_json()

        # Validate required fields
        required_fields = ['current_lesson_plan', 'customization']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Optional: get lesson_type if provided
        lesson_type = data.get('lesson_type', None)

        # Customize the lesson plan
        customized_plan = customize_lesson_plan(
            data['current_lesson_plan'],
            data['customization'],
            lesson_type
        )

        return jsonify(customized_plan)

    except requests.exceptions.RequestException as net_err:
        # Catch network/connection-related errors
        print(f"[Network Error in customize_lesson_plan_route]: {str(net_err)}")
        return jsonify({
            'error': 'A network error occurred while customizing the lesson plan. '
                     'Please check your internet connection or try again later.'
        }), 503

    except ValueError as val_err:
        print(f"[ValueError in customize_lesson_plan_route]: {str(val_err)}")
        return jsonify({'error': str(val_err)}), 400

    except Exception as e:
        print(f"[Error in customize_lesson_plan_route]: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred while customizing the lesson plan. Please try again.'}), 500

if __name__ == '__main__':
    # Adjust host/port if needed. 0.0.0.0 is typical for container deployments.
    # In production, disable debug mode and set a stable secret key.
    app.run(debug=True, host='0.0.0.0', port=5000)
