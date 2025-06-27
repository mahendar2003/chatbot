from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Flask app initialization
app = Flask(__name__)

# Sample training data (simple intents)
intents = {
    "greet": ["hello", "hi", "hey", "good morning", "howdy", "hey there", "what's up", "yo"],
    "goodbye": ["bye", "goodbye", "see you", "take care", "farewell"],
    "ask_question": ["what is your name?", "who are you?", "what can you do?", "tell me about yourself", "what is your purpose?"],
    "weather": ["what's the weather like?", "is it going to rain?", "what's the forecast?", "will it be sunny tomorrow?"],
    "time": ["what time is it?", "tell me the time", "what's the current time?", "is it morning yet?", "what's the hour?"],
    "thank_you": ["thank you", "thanks", "thanks a lot", "thank you so much", "appreciate it"],
    "help": ["can you help me?", "I need assistance", "please assist me", "help me out", "can you guide me?"],
    "affirmative": ["yes", "yeah", "yup", "sure", "absolutely", "of course"],
    "negative": ["no", "nope", "not at all", "never", "definitely not"],
    "joke": ["tell me a joke", "make me laugh", "tell me something funny", "crack a joke", "give me a joke"],
}

# Training data
training_sentences = []
training_labels = []

for label, examples in intents.items():
    for example in examples:
        training_sentences.append(example)
        training_labels.append(label)

# Vectorize the text data and train a model
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(training_sentences)
model = MultinomialNB()
model.fit(X, training_labels)

# Save the model and vectorizer for later use
joblib.dump(model, 'model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    user_input = request.form['message']
    model = joblib.load('model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')

    # Transform input into a vector using the vectorizer
    input_vector = vectorizer.transform([user_input])

    # Get prediction from the model
    prediction = model.predict(input_vector)
    response = prediction[0]

    # Define responses for each intent
    if response == "greet":
        return jsonify({'response': 'Hello! How can I assist you today?'})
    elif response == "goodbye":
        return jsonify({'response': 'Goodbye! Have a great day!'})
    elif response == "ask_question":
        return jsonify({'response': 'I am a chatbot created to assist you. Ask me anything!'})
    elif response == "weather":
        return jsonify({'response': 'I am currently unable to fetch live weather data. You can check your local weather app.'})
    elif response == "time":
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        return jsonify({'response': f'The current time is {current_time}.'})
    elif response == "thank_you":
        return jsonify({'response': 'You\'re welcome! Let me know if you need anything else.'})
    elif response == "help":
        return jsonify({'response': 'Sure! I can assist you with different queries. Just type and I will respond.'})
    elif response == "affirmative":
        return jsonify({'response': 'Great! Glad to know that.'})
    elif response == "negative":
        return jsonify({'response': 'Oh! Please let me know if you need any help.'})
    elif response == "joke":
        return jsonify({'response': 'Why don’t skeletons fight each other? They don’t have the guts!'})
    else:
        return jsonify({'response': 'Sorry, I didn’t understand that. Could you please rephrase?'})


if __name__ == '__main__':
    app.run(debug=True)
