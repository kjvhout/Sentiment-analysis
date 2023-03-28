from fetchData import get_reviews
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

NUMBER_OF_REVIEWS = 500000

print("Please wait for the model to be trained...\n")
print("Model is being trained based on [" + str(NUMBER_OF_REVIEWS) + "] reviews \n")

# Load hotel reviews dataset
reviews = get_reviews(NUMBER_OF_REVIEWS)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(reviews['review'], reviews['positive'], random_state=0)

# Vectorize the text data using a Bag of Words model
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)

# Train the Naive Bayes classifier
nb = MultinomialNB()
nb.fit(X_train_vec, y_train)

# Evaluate the classifier on the testing set
X_test_vec = vectorizer.transform(X_test)
accuracy = nb.score(X_test_vec, y_test)
print(f"Modal accuracy: {accuracy:.3f}\n")

file = "trained/naivebayes_model.pkl"
with open(file, 'wb') as f:
    pickle.dump(nb, f)
print(f"Modal has been saved to: '{file}'")

file = "trained/naivebayes_vectorizer.pickle"
pickle.dump(vectorizer, open(file, "wb"))
print(f"Vectorizer has been saved to: '{file}'")
