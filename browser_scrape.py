import os
import time
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# chrome_options.add_argument("--headless")

# driver = webdriver.Chrome(chrome_options=chrome_options)
driver = webdriver.Firefox()
base_url = 'https://streeteasy.com/for-sale/nyc?page='

def get_page(page=1):
    driver.get(base_url + str(page))

    items = []
    listings = driver.find_elements_by_css_selector('article.item')
    for listing in listings:
        item = {
            'address': listing.find_element_by_css_selector('.details-title a').text,
            'id': listing.find_element_by_css_selector('.details-title a').get_attribute('data-gtm-listing-id'),
            'url': listing.find_element_by_css_selector('.details-title a').get_attribute('href'),
            'price':  listing.find_element_by_css_selector('.price').text,
            'monthly':  listing.find_element_by_css_selector('.monthly_payment').text,
            'details': [d.text.strip() for d in listing.find_elements_by_css_selector('ul.details_info li, li.details_info')],
            'location': listing.get_attribute('se:map:point'),
            'payment_details': {}
        }

        try:
            payment_details = listing.find_element_by_css_selector('.EstimateCalculator').get_attribute('se:monthly_payment:attributes')
            payment_details = json.loads(payment_details)
            item['payment_details'] = payment_details
        except:
            pass

        items.append(item)

    return items


def get_all(total_pages=1000, start_page=1):
    items = []
    for i in range(start_page, total_pages):
        try:
            _items = get_page(i)
        except Exception as e:
            print(e)
            _items = []
        items += _items
        print(len(items))
        with open('apartments.json', 'w') as outfile:
            json.dump(items, outfile, indent=2)
        time.sleep(random.randint(1, 4))


if __name__ == '__main__':
    get_all(1064, start_page=738)

