import time

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Chrome details
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.amazon.com")

# Search input field
search_field = driver.find_element(By.CSS_SELECTOR, "input[id='twotabsearchtextbox']")
search_field.send_keys("monster truck toys")
time.sleep(1)

# Search button
search_button = driver.find_element(By.CSS_SELECTOR, "input[type=submit][value=Go]")
search_button.click()
time.sleep(1)

# Results
all_results_css_sel = "div[class*='s-search-results']"
single_result_xpath = "//div[starts-with(@data-asin, 'B0') and div[not(contains(@data-index, '999999'))]]"
toy_rating_css_sel = "span[aria-label*='out of']"

results_count = 0
id_4_plus = 1
id_other = 1
row = ""
four_plus_collection = ""
other_collection = ""

while True:
    result_div = driver.find_element(By.CSS_SELECTOR, all_results_css_sel)
    results = result_div.find_elements(By.XPATH, single_result_xpath)

    for result in range(len(results)):
        try:
            toy_desc = results[result].find_element(By.CSS_SELECTOR, "a[class*='a-link-normal a-text-normal'] > span").text
        except NoSuchElementException:
            toy_desc = "Name not found"

        try:
            toy_rating = results[result].find_element(By.CSS_SELECTOR, toy_rating_css_sel).get_attribute('aria-label')
        except NoSuchElementException:
            toy_rating = "0.0"

        try:
            toy_review_numbers = results[result].find_element(By.CSS_SELECTOR, " span[class='a-size-base']").text
        except NoSuchElementException:
            toy_review_numbers = "0"

        results_count += 1

        if int(float(toy_rating[0:3])) >= 4 and int(toy_review_numbers.replace(",", "")) >= 50:
            row = "{0},{1},{2},{3}".format(id_4_plus, toy_desc.replace(",", ""), toy_rating[0:3], toy_review_numbers)
            four_plus_collection += row + "\n"
            id_4_plus += 1
        else:
            row = "{0},{1},{2},{3}".format(id_other, toy_desc.replace(",", ""), toy_rating[0:3], toy_review_numbers)
            other_collection += row + "\n"
            id_other += 1

        if results_count == 100:
            break

    if results_count == 100:
        break
    else:
        next_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Next')]")
        next_button.click()
        time.sleep(5)

file = open("4_stars_plus.csv", "w")
file.write(four_plus_collection)
file.close()

file = open("all_others.csv", "w")
file.write(other_collection)
file.close()

driver.close()
driver.quit()


