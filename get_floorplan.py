import os
import time
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests

# chrome_options = Options()
# chrome_options.add_argument("--headless")

# driver = webdriver.Chrome(chrome_options=chrome_options)
driver = webdriver.Firefox()
base_url = 'https://streeteasy.com/'


def download_file(url, local_filename=None):
    if local_filename is None:
        local_filename = url.split('/')[-1]

    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


def get_page(url, outname):
    driver.get(url)
    time.sleep(10)

    elem = driver.find_element_by_xpath("//*")
    source_code = elem.get_attribute("outerHTML")
    print(source_code)
    soup = BeautifulSoup(source_code, "lxml")

    datalayer = ''

    try:
        floorplan = soup.select('.floorplan img')[0]
        src = floorplan.get('data-original')
        # floorplan = driver.find_element_by_css_selector('.floorplan img')
        # src = floorplan.get_attribute('data-original')
        download_file(src, outname)

        for line in source_code.split('\n'):
            if 'dataLayer = ' in line:
                datalayer = line.replace('dataLayer = [', '').replace('];', '')

    except Exception as e:
        print(e)

    with open(outname + '.json', 'w') as outfile:
        outfile.write(datalayer)





    # '''window.dataLayer[0]'''
    # dataLayer = driver.execute_script('alert(window.dataLayer[0])')
    # print(dataLayer)



def get_all():
    with open('apartments_bak.json', 'r') as infile:
        data = json.load(infile)

    for item in data:
        pid = item['id']
        outname = 'floorplans/' + pid + '.jpg'

        if os.path.exists(outname + '.json'):
            continue

        get_page(item['url'], outname)
        time.sleep(random.randint(1, 4))


if __name__ == '__main__':
    get_all()


