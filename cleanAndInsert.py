from nltk.corpus import stopwords
import pandas as pd
import sqlalchemy as sql
import config

# Used to filter out the reviews with less than x amount of reviews
MIN_WORD_AMOUNT = 3

# Make connection to the database
engine = sql.create_engine(f'mysql+pymysql://{config.login}@localhost/bdasignment1')

# Read all the data
hotel_dataset = pd.read_csv('Data/Hotel_Reviews.csv')
scraped_booking_dataset = pd.read_csv('Data/Booking.com_scraped_reviews.csv')
scraped_tripadvisor_dataset = pd.read_csv('Data/tripadvisor_scraped_reviews.csv')
hand_written_dataset = pd.read_csv('Data/hand_written_reviews.csv')

# Get the positive and Negative reviews from the hotel dataset
positive_reviews = hotel_dataset.loc[:, ['Positive_Review', 'Review_Total_Positive_Word_Counts', 'Reviewer_Nationality',
                                         'lat', 'lng', 'Hotel_Name', 'Average_Score']]
negative_reviews = hotel_dataset.loc[:, ['Negative_Review', 'Review_Total_Negative_Word_Counts', 'Reviewer_Nationality',
                                         'lat', 'lng', 'Hotel_Name', 'Average_Score']]
# Rename columns
positive_reviews = positive_reviews.rename(columns={"Positive_Review": "review", "Review_Total_Positive_Word_Counts": "total_words"})
negative_reviews = negative_reviews.rename(columns={"Negative_Review": "review", "Review_Total_Negative_Word_Counts": "total_words"})

# Replace with boolean value
positive_reviews['positive'] = True
negative_reviews['positive'] = False

# Add total_words to scraped and handwritten datasets
scraped_booking_dataset['total_words'] = scraped_booking_dataset['review'].str.split().str.len()
scraped_tripadvisor_dataset['total_words'] = scraped_tripadvisor_dataset['review'].str.split().str.len()
hand_written_dataset['total_words'] = hand_written_dataset['review'].str.split().str.len()

# Add all reviews to one variable
all_reviews = pd.concat([positive_reviews, negative_reviews, scraped_booking_dataset, scraped_tripadvisor_dataset,
                         hand_written_dataset])

# Filter out all the stopwords
stop = stopwords.words('english')
# add custom stopwords
custom_stop_words = ['hotel', 'Hotel', 'food', 'room', 'Room', 'rooms', 'Rooms', 'staff', 'pool', 'location',
                     'breakfast', 'lunch', 'restaurant', 'dinner', 'location', 'bathroom', 'family', 'fiance',
                     'girlfriend', 'boyfriend', 'decoration', 'Bedroom', 'bedroom', 'Bedrooms', 'bedrooms', 'bed',
                     'beds', 'shower', 'brunch', 'building', 'pool', 'Pool', 'spa', 'reception', 'Reception',
                     'interior', 'nights', 'property', '24', 'hour', 'Location', 'facilities', 'Parking', 'parking',
                     'city', 'public-transport', 'beach', 'Beach', 'the', 'The', 'placement', 'daytime', 'activities',
                     'fitness', 'Gym', 'people', 'hotels', 'Hotels', 'money', 'check-in', 'weekend', 'booking']
stop.extend(custom_stop_words)
all_reviews['review'] = all_reviews['review'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop]))

# Remove all reviews with less than X amount of words
all_reviews['total_words'] = all_reviews['review'].str.split().str.len()
all_reviews = all_reviews[all_reviews['total_words'] > MIN_WORD_AMOUNT]

# Add all the reviews to the database
all_reviews.to_sql(name='review', con=engine, index=True, if_exists='replace', chunksize=1000)

