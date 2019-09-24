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
toy_stars_class_css_sel = "span[aria-label*='out of'] > span > a > i"
toy_desc_css_sel = "a[class*='a-link-normal a-text-normal'] > span"
toy_review_numbers_css_sel = " span[class='a-size-base']"

results_count = 0
id_4_plus = 1
id_other = 1
four_plus_products = {}
other_products = {}

'''
dict = {1: {'description': 'Monster Trucks Inertia Car', 'rating': '4.5', 'reviews': '55', 'stars': "a-star-small-4-5"},
        2: {'description': 'Monster Trucks Trucks', 'rating': '4.2', 'reviews': '49', 'stars': "a-star-small-4"}}
'''

while True:
    result_div = driver.find_element(By.CSS_SELECTOR, all_results_css_sel)
    results = result_div.find_elements(By.XPATH, single_result_xpath)

    for result in range(len(results)):
        try:
            toy_desc = results[result].find_element(By.CSS_SELECTOR, toy_desc_css_sel).text
        except NoSuchElementException:
            toy_desc = "Name not found"

        try:
            toy_rating = results[result].find_element(By.CSS_SELECTOR, toy_rating_css_sel).get_attribute('aria-label')
            if toy_rating == "by":
                toy_rating = "0.0"
        except NoSuchElementException:
            toy_rating = "0.0"

        try:
            classes_list = results[result].find_element(By.CSS_SELECTOR, toy_stars_class_css_sel).get_attribute(
                'class')
            classes_names = str(classes_list).split()
            for name in classes_names:
                if name.startswith("a-star-small"):
                    toy_stars = name
                    break
                else:
                    toy_stars = ""
        except NoSuchElementException:
            toy_stars = ""

        try:
            toy_review_numbers = results[result].find_element(By.CSS_SELECTOR, toy_review_numbers_css_sel).text
        except NoSuchElementException:
            toy_review_numbers = "0"

        results_count += 1
        try:
            if int(float(toy_rating[0:3])) == 4 and int(toy_review_numbers.replace(",", "")) >= 50:
                four_plus_products[id_4_plus] = {"description": toy_desc.replace(",", ""),
                                                 "rating": toy_rating[0:3],
                                                 "reviews": toy_review_numbers,
                                                 "stars": toy_stars}
                id_4_plus += 1
            else:
                other_products[id_other] = {"description": toy_desc.replace(",", ""),
                                            "rating": toy_rating[0:3],
                                            "reviews": toy_review_numbers,
                                            "stars": toy_stars}
                id_other += 1
        except ValueError:
            print("")

        if results_count == 10:
            break

    if results_count == 10:
        break
    else:
        next_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Next')]")
        next_button.click()
        time.sleep(5)

file = open("4_stars_plus.csv", "w")
for product_id, product_details in four_plus_products.items():
    row = ""
    row += str(product_id)
    for key in product_details:
        if key == "stars":
            continue
        row += "," + product_details[key]
    row += "\n"
    file.write(row)
file.close()

file = open("all_others.csv", "w")
for product_id, product_details in other_products.items():
    row = ""
    row += str(product_id)
    for key in product_details:
        if key == "stars":
            continue
        row += "," + product_details[key]
    row += "\n"
    file.write(row)
file.close()

driver.close()
driver.quit()


count_four_plus = 1
for product in sorted(four_plus_products, key=lambda x: (four_plus_products[x]['rating']), reverse=True):
    actual_class_name = four_plus_products[product]["stars"]
    rating = four_plus_products[product]["rating"]
    expected_class_name = ""

    if "0" <= rating[2] <= "2":
        expected_class_name = "a-star-small-" + rating[0]

    if "3" <= rating[2] <= "7":
        expected_class_name = "a-star-small-" + rating[0] + "-5"

    if rating[2] >= "8":
        expected_class_name = "a-star-small-" + str(int(rating[0]) + 1)

    try:
        assert actual_class_name == expected_class_name
        print("Assertion Successful! Product: \"" + four_plus_products[product]["description"] + "\"")
    except AssertionError as e:
        print("Assertion Failed! Product: \"" + four_plus_products[product]["description"] + "\" Rating: \"" + four_plus_products[product]["rating"] + "\"")
        print("Actual class name: \"" + actual_class_name + "\". Expected class name: \"" + expected_class_name+ "\"")

    if count_four_plus == 5:
        break
    count_four_plus += 1

print("********")

count_other = 1
for product in sorted(other_products, key=lambda x: (other_products[x]['rating']), reverse=True):
    actual_class_name = other_products[product]["stars"]
    rating = other_products[product]["rating"]
    expected_class_name = ""

    if "0" <= rating[2] <= "2":
        expected_class_name = "a-star-small-" + rating[0]

    if "3" <= rating[2] <= "7":
        expected_class_name = "a-star-small-" + rating[0] + "-5"

    if rating[2] >= "8":
        expected_class_name = "a-star-small-" + str(int(rating[0]) + 1)

    try:
        assert actual_class_name == expected_class_name
        print("Assertion Successful! Product: \"" + other_products[product]["description"] + "\"")
    except AssertionError as e:
        print("Assertion Failed! Product: \"" + other_products[product]["description"] + "\" Rating: \"" + other_products[product]["rating"] + "\"")
        print("Actual class name: \"" + actual_class_name + "\". Expected class name: \"" + expected_class_name+ "\"")

    if count_other == 5:
        break
    count_other += 1

'''
4.0 = 4
4.0 ~ 4.2 = 4
4.3 ~ 4.7 = 4.5
4.8 ~ 5.0 = 5
'''