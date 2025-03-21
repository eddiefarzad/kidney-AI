from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_compatibility(data):
    # Dummy scoring logic (can replace later with AI model)
    score = 50
    if data.get('blood_type_match'):
        score += 25
    if abs(data.get('donor_age', 0) - data.get('patient_age', 0)) < 10:
        score += 10
    if data.get('hla_match_score'):
        score += data['hla_match_score'] * 0.5
    return round(min(score, 100), 2)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    score = calculate_compatibility(data)
    return jsonify({'compatibility_score': score})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
