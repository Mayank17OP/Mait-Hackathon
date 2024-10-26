from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
from dotenv import load_dotenv
import torch
from flask_cors import CORS
import requests  # Add this import for making API calls

load_dotenv()  # Load environment variables
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load model and tokenizer
model_name = "microsoft/DialoGPT-medium"  # You can change this to a medical-specific model if available
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Add this line after model initialization
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Encode the input and generate a response
    try:
        input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt').to(device)
        chat_history_ids = model.generate(
            input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=100,
            top_p=0.7,
            temperature=0.8
        )
        
        response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/gemini', methods=['POST'])
def gemini():
    data = request.json
    user_input = data.get('message', '')

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Call the Gemini API
    try:
        response = requests.post(
            'https://api.gemini.com/v1/your_endpoint',  # Replace with the actual Gemini API endpoint
            headers={'Authorization': 'Bearer AIzaSyDxQSIR3uXc46uD-ElB7kVEIhYajRbsPuM'},
            json={'message': user_input}
        )
        response_data = response.json()
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
