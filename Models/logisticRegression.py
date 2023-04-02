from fetchData import get_reviews
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle

NUMBER_OF_REVIEWS = 500000

print("Please wait for the model to be trained...\n")
print("Model is being trained based on [" + str(NUMBER_OF_REVIEWS) + "] reviews \n")

# Load the dataset
reviews = get_reviews(NUMBER_OF_REVIEWS)

# Split the dataset into training and testing sets
train_data, test_data = train_test_split(reviews, stratify=reviews['positive'], random_state=1)

# Create a bag of words representation of the text data
vectorizer = CountVectorizer(max_features=1000, binary=False)
train_vectors = vectorizer.fit_transform(train_data['review'])
test_vectors = vectorizer.transform(test_data['review'])

# Train a logistic regression model on the training data
lr = LogisticRegression(C=10, solver='lbfgs', max_iter=1000)
lr.fit(train_vectors, train_data['positive'])

# Evaluate the model on the testing data
accuracy = lr.score(test_vectors, test_data['positive'])
print(f"Modal accuracy: {accuracy:.3f}\n")

file = "trained/logistic_regression_model.pkl"
with open(file, 'wb') as f:
    pickle.dump(lr, f)
print(f"Modal has been saved to: '{file}'")

file = "trained/logistic_regression_vectorizer.pickle"
pickle.dump(vectorizer, open(file, "wb"))
print(f"Vectorizer has been saved to: '{file}'")
