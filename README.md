# 🧼 CleanFeed

CleanFeed is a lightweight AI-powered text moderation API that detects toxic content, analyzes sentiment, and rephrases offensive text into polite alternatives using Google Gemini.

---

## 🚀 Features

1. **Multi-label Toxicity Detection**  
   Detects six types of toxicity using pre-trained Logistic Regression models.

2. **Polite Rephrasing**  
   Automatically rephrases flagged content using **Google Gemini 1.5 Pro**.

3. **Sentiment Analysis**  
   Classifies user input as Positive / Neutral / Negative using **VADER (NLTK)**.

4. **Built with Flask**  
   Simple REST API design for easy integration.

5. **Customizable Moderation Thresholds**  
   Set your own confidence level for classification and response.

---

## 🧠 Tech Stack

| Task                | Model Used                          |
|---------------------|--------------------------------------|
| Toxicity Detection  | TF-IDF + Logistic Regression (6 classes) |
| Sentiment Analysis  | VADER from NLTK                      |
| Rephrasing          | Google Gemini 1.5 Pro (via API)     |

---

## 📦 How to Run Locally

```bash
git clone https://github.com/oorjatiwari23/CleanFeed.git
cd CleanFeed
pip install -r requirements.txt

# Add your API key
echo GEMINI_API_KEY=your_api_key > .env

# Run the app
python app.py
