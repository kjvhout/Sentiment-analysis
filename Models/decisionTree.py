from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from fetchData import get_reviews
import pickle

NUMBER_OF_REVIEWS = 500000

print("Please wait for the model to be trained...\n")
print("Model is being trained based on [" + str(NUMBER_OF_REVIEWS) + "] reviews \n")

# Load the dataset
reviews = get_reviews(NUMBER_OF_REVIEWS)

# Split the dataset into training and testing sets
train_data, test_data = train_test_split(reviews, random_state=1)

# Create a bag of words representation of the text data
vectorizer = CountVectorizer(binary=False)
train_vectors = vectorizer.fit_transform(train_data['review'])
test_vectors = vectorizer.transform(test_data['review'])

# Train a decision tree model on the training data
model = DecisionTreeClassifier(min_samples_leaf=4, max_depth=400, min_samples_split=10,
                               criterion='gini')
model.fit(train_vectors, train_data['positive'])

# Evaluate the model on the testing data
predictions = model.predict(test_vectors)
accuracy = accuracy_score(test_data['positive'], predictions)
print('Accuracy:', accuracy)

file = "trained/decisionTree_model.pkl"
with open(file, 'wb') as f:
    pickle.dump(model, f)
print(f"Modal has been saved to: '{file}'")

file = "trained/decisionTree_vectorizer.pickle"
pickle.dump(vectorizer, open(file, "wb"))
print(f"Vectorizer has been saved to: '{file}'")
