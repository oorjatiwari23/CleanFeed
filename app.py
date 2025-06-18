import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER lexicon if not already present
nltk.download("vader_lexicon")

# Initialize Flask App
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app, resources={r"/moderate": {"origins": "*"}})

# Load AI Models
vectorizer = joblib.load("tfidf_vectorizer.pkl")
labels = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
models = {label: joblib.load(f"{label}_model.pkl") for label in labels}




# Initialize VADER Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Set your Gemini API Key
genai.configure(api_key="AIzaSyDwhanLyM8-AEZUoTqNh0RGGboRCzxt9VI")  

def rephrase_text(offensive_text):
    """Rephrases offensive text to be polite using Google Gemini API"""
    prompt = f"Rewrite the following text to be polite and non-offensive. Handle explicit language also.:\n\n{offensive_text}"

    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest") 
        response = model.generate_content(prompt)
        polite_text = response.text.strip()
        return polite_text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Error in rephrasing."

def analyze_sentiment(text):
    """Analyzes sentiment using NLTK's VADER"""
    sentiment_scores = sia.polarity_scores(text)
    compound_score = sentiment_scores["compound"]

    if compound_score >= 0.05:
        return "Positive"
    elif compound_score<= -0.05:
        return "Negative"
    else:
        return "Neutral"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/moderate", methods=["POST"])
def moderate_text():
    data = request.get_json()
    user_input = data.get("text", "")

    if not user_input:
        return jsonify({"error": "No text provided"}), 400

    # Text moderation model prediction
    input_tfidf = vectorizer.transform([user_input])
    probabilities = {label: models[label].predict_proba(input_tfidf)[0][1] for label in labels}

    detected_label = max(probabilities, key=probabilities.get)
    highest_prob = probabilities[detected_label]
    confidence_score = round(highest_prob * 100, 2)

    status = "Flagged" if highest_prob > 0.6 else "Safe" if highest_prob < 0.3 else "Needs Review"

    # If flagged, generate a polite alternative
    polite_version = rephrase_text(user_input) if status == "Flagged" else None

    # Sentiment Analysis
    sentiment = analyze_sentiment(user_input)

    response = {
        "text": user_input,
        "category": detected_label,
        "confidence": confidence_score,
        "status": status,
        "polite_version": polite_version,
        "sentiment": sentiment  # New field added
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=50611)



