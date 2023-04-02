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

language = "English"
# default number of scraped pages
num_page = 40

url = "https://www.tripadvisor.com/Hotel_Review-g188590-d273177-Reviews-XO_Hotels_Infinity-Amsterdam_North_Holland_Province.html"

driver.get(url)

WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))).click()

scrapedReviews = []

# change the value inside the range to save more or less reviews
for i in range(0, num_page):
    # expand the review
    time.sleep(2)
    print(f'container: {i}')
    container = driver.find_elements("xpath", "//div[@data-reviewid]")
    for j in range(len(container)):
        print(f'review: {j + 1}/{len(container)}')
        rating = (int(container[j].find_element("xpath", ".//span[contains(@class, 'ui_bubble_rating bubble_')]")
                      .get_attribute("class").split("_")[3]) >= 30)
        review = container[j].find_element("xpath", ".//span[contains(@class,'QewHA')]/span").text.replace("\n", "  ")
        scrapedReviews.append([review, rating])

    driver.find_element("xpath", './/a[contains(@class,"next")]').click()

scrapedReviewsDF = pd.DataFrame(scrapedReviews, columns=['review', 'positive'])

driver.quit()
scrapedReviewsDF.to_csv("../Data/tripadvisor_scraped_reviews.csv", sep=',', index=False)
