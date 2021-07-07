from flask import Flask, url_for, request
from flask import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
# options.set_headless(True)


def getUpdate():
    driver = webdriver.Firefox(executable_path='./geckodriver.exe', options=options)
    driver.execute_script("window.open('https://www.mangago.me/list/latest/all/1/'),'_blannk'")
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#searchbar")))
    truyen = driver.find_elements_by_css_selector("#search_list > li")
    arr = []
    for t in truyen:
        try:
            arr = arr + [{
                "image": t.find_element_by_css_selector('div > a > img').get_attribute('src'),
                "url": t.find_element_by_css_selector('div > a').get_attribute('href'),
                "title": t.find_element_by_css_selector('div:nth-child(2) > div.row-1 > span > h2 > a').get_attribute('textContent'),
                "othertitle": t.find_element_by_css_selector('div:nth-child(2) > div.row-2').get_attribute('innerText').strip()[13:],
                "author": t.find_element_by_css_selector('div:nth-child(2) > div.row-3').get_attribute('textContent').strip()[8:],
                "gentes": t.find_element_by_css_selector('div:nth-child(2) > div.row-4 > span').get_attribute('innerText').strip(),
                "latest": {
                    "name": t.find_element_by_css_selector('div:nth-child(2) > div:nth-child(6) > a:nth-child(2)').get_attribute('innerText').strip(),
                    "url": t.find_element_by_css_selector('div:nth-child(2) > div:nth-child(6) > a:nth-child(2)').get_attribute('href')
                }
            }]
        except:
            arr = arr + [{
                "image": t.find_element_by_css_selector('div > a > img').get_attribute('src'),
                "url": t.find_element_by_css_selector('div > a').get_attribute('href'),
                "title": t.find_element_by_css_selector('div:nth-child(2) > div.row-1 > span > h2 > a').get_attribute('textContent'),
                "othertitle": t.find_element_by_css_selector('div:nth-child(2) > div.row-2').get_attribute('innerText').strip()[13:],
                "author": t.find_element_by_css_selector('div:nth-child(2) > div.row-3').get_attribute('textContent').strip()[8:],
                "gentes": t.find_element_by_css_selector('div:nth-child(2) > div.row-4 > span').get_attribute('innerText').strip(),
                "latest": {
                    "name": "",
                    "url": ""
                }
            }]
    driver.quit()
    return arr

def getChapters(url):
    driver = webdriver.Firefox(executable_path='./geckodriver.exe', options=options)
    driver.execute_script("window.open('" + url + "'),'_blannk'")
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#chapter_table")))
    chapter = driver.find_elements_by_css_selector("#chapter_table > tbody > tr > td:nth-child(1) > h4 > a")
    arr = []
    for c in chapter:
        arr = arr + [{
            "name": c.get_attribute("innerText").strip(),
            "url": c.get_attribute("href")
        }]
    driver.quit()
    return arr

def getImagesChap(urltruyen, urlchap):
    arr = []
    driver = webdriver.Firefox(executable_path='./geckodriver.exe', options=options)
    driver.execute_script("window.open('" + urltruyen + "'),'_blannk'")
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#chapter_table")))
    driver.find_element_by_css_selector("a[href='"+ urlchap + "']").click()
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".main-body")))
    count = 0
    try:
        page = driver.find_elements_by_css_selector("#dropdown-menu-page li a")
        i = 0
        while i < len(page):
            try:
                page = driver.find_elements_by_css_selector("#dropdown-menu-page li a")
                driver.find_element_by_css_selector(".page").click()
                driver.find_element_by_css_selector("#dropdown-menu-page > li:nth-child(" + page[i].get_attribute("innerText").split(" ")[1] + ") > a").click()
                time.sleep(0.6)
                try:
                    img = driver.find_element_by_css_selector("img#page" + page[i].get_attribute("innerText").split(" ")[1])
                    arr.append(img.get_attribute("src"))
                    i = i + 1
                except:
                    count = count + 1
                    if count > 2:
                        i = i + 1
            except:
                print(i)    
    except:
        print("not loaded")
    print(arr)
    driver.quit()
    return arr

app = Flask(__name__)

@app.route('/update', methods = ['GET'])
def update():
    data = getUpdate()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/chapter', methods = ['POST'])
def chapter():
    param = request.get_json(force=True)
    data = getChapters(param['url'])
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/image', methods = ['POST'])
def image():
    param = request.get_json(force=True)
    data = getImagesChap(param['urltruyen'], param['urlchap'])
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(debug = True)