import pickle

# Get modal and vecotrizer for NaiveBayes
with open("trained/naivebayes_model.pkl", 'rb') as f:
    nb_from_pickle = pickle.load(f)
vectorizer_nb = pickle.load(open("trained/naivebayes_vectorizer.pickle", 'rb'))

# Get modal and vecotrizer for Logistic regression
with open("trained/logistic_regression_model.pkl", 'rb') as f:
    lr_from_pickle = pickle.load(f)
vectorizer_lr = pickle.load(open("trained/logistic_regression_vectorizer.pickle", 'rb'))

# Get modal and vecotrizer for Decision Tree
with open("trained/decisionTree_model.pkl", 'rb') as f:
    dt_from_pickle = pickle.load(f)
vectorizer_dt = pickle.load(open("trained/decisionTree_vectorizer.pickle", 'rb'))


def predict_sentiment_nb(input_text):
    input_vec = vectorizer_nb.transform([input_text])
    sentiment = nb_from_pickle.predict(input_vec)[0]
    return sentiment


def predict_sentiment_lr(input_text):
    input_vec = vectorizer_lr.transform([input_text])
    sentiment = lr_from_pickle.predict(input_vec)[0]
    return sentiment


def predict_sentiment_dt(input_text):
    input_vec = vectorizer_dt.transform([input_text])
    sentiment = dt_from_pickle.predict(input_vec)[0]
    return sentiment


while True:
    # Test the custom input function
    print("Enter custom review (type q to stop):")
    input_text = input()
    if input_text == "q":
        break
    sentiment = predict_sentiment_nb(input_text)
    print(f"\nPrediction [NaiveBayes]: \t\t{('Negative (-)', 'Positive (+)')[int(sentiment) == 1]}")
    sentiment = predict_sentiment_lr(input_text)
    print(f"Prediction [LogisticRegression]: \t{('Negative (-)', 'Positive (+)')[int(sentiment) == 1]}")
    sentiment = predict_sentiment_dt(input_text)
    print(f"Prediction [DecisionTree]: \t\t{('Negative (-)', 'Positive (+)')[int(sentiment) == 1]}\n")
