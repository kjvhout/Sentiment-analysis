import sys
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
import time
import pandas as pd

# accepting cookies
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# default path to file to store data
path_to_file = "reviews1.csv"

language = "English"
# default number of scraped pages
num_page = 20

url = "https://www.booking.com/hotel/nl/ruby-emma.en-gb.html?aid=304142&label=gen173nr-1FCAEoggI46AdICVgEaKkBiAEBmAEJuAEXyAEM2AEB6AEB-AECiAIBqAIDuAKMgNuLBsACAdICJGRkNDlmMzBkLThhMTYtNDEwNi04MWY2LTNkODNkNTkzNTY1ZtgCBeACAQ&sid=947fceb5e722310406e5ed98f83f59a1&dest_id=-2140479;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=2;hpos=2;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1678177436;srpvid=af0c3b0d37be0031;type=total;ucfs=1&#tab-reviews"

driver.get(url)
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))).click()

scrapedReviews = []

# change the value inside the range to save more or less reviews
for i in range(0, num_page):

    # expand the review
    time.sleep(2)
    container = driver.find_elements("xpath", '//*[@id="review_list_page_container"]/ul/li')
    print(len(container))
    for j in range(len(container)):
        reviews = container[j].find_elements("xpath", ".//span[contains(@class,'c-review__body')]")
        if len(reviews) > 1:
            negative_review = reviews[1].text.replace("\n", "  ")
            scrapedReviews.append([negative_review, False])

        positive_review = reviews[0].text.replace("\n", "  ")
        scrapedReviews.append([positive_review, True])

    driver.find_element("xpath", './/a[@class="pagenext"]').click()

scrapedReviewsDF = pd.DataFrame(scrapedReviews, columns=['review', 'positive'])

scrapedReviewsDF.head(10)
driver.quit()
print('Done scraping ....')
scrapedReviewsDF.to_csv("../Data/Booking.com_scraped_reviews.csv", sep=',', index=False)
