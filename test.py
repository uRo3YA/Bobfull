from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotInteractableException
import time
import urllib.request # 이미를 받기위한 라이브러리
import json

test_result = []
test_result_image = []

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

URL = "https://map.kakao.com/"
driver.get(url=URL)
driver.implicitly_wait(5)

# 검색창의 아이디를 선택
elem = driver.find_element(By.ID, 'search.keyword.query')

page = []
lst = set()
c = set()
session = set()

# 원하는 값 입력
elem.send_keys("판교 맛집")
elem.send_keys(Keys.RETURN)
time.sleep(3)

# 더보기 클릭
more = driver.find_element(By.ID, 'info.search.place.more')
driver.execute_script("arguments[0].click();", more)
# moreview = more.get_attribute('href')
# driver.get(url=moreview)
time.sleep(3)
    

next_btn = driver.find_element(By.ID, "info.search.page.next")
# for j in range(6):
#     for i in range(1, 6):
#         p = driver.find_element(By.XPATH, '//*[@id="info.search.page.no' + str(i) + '"]')
#         driver.execute_script("arguments[0].click();", p)
#         time.sleep(2)
#         url_ = driver.find_elements(By.CLASS_NAME, 'moreview')   
#         for u in url_:
#             lst.add(u.get_attribute("href"))
#     driver.execute_script("arguments[0].click();", next_btn)
# for i in range(1, 5):
#     p = driver.find_element(By.XPATH, '//*[@id="info.search.page.no' + str(i) + '"]')
#     driver.execute_script("arguments[0].click();", p)
#     time.sleep(2)
#     url_ = driver.find_elements(By.CLASS_NAME, 'moreview')   
#     for u in url_:
#         lst.add(u.get_attribute("href"))

p = driver.find_element(By.XPATH, '//*[@id="info.search.page.no1"]')
driver.execute_script("arguments[0].click();", p)
time.sleep(2)
url_ = driver.find_elements(By.CLASS_NAME, 'moreview')   
for u in url_:
    lst.add(u.get_attribute("href"))

i = 0
for l in lst:
    i += 1
    result = {"model": "restaurant.restaurant", "pk": i, "fields": {"name": 0, 'address': 0, 'category': 15, 'detail': ''}}
    URL = l
    
    # 상세보기 페이지로 이동
    driver.get(url=URL)
    driver.implicitly_wait(5)
    
    name = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/div/h2")
    result['fields']['name'] = name.text
    
    address = driver.find_element(By.CLASS_NAME, "txt_address")
    result['fields']['address'] = address.text
    
    try:
        driver.execute_script("arguments[0].click();", driver.find_elements(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[3]/a')[0])
    except:
        pass
    menu = driver.find_elements(By.CLASS_NAME, 'loss_word')
    detail = ''
    if menu[-1].text == '제공 : 카카오맵 평가':
        for j in range(len(menu) - 2):
            detail += menu[j].text
            detail += ', '
        detail += menu[-2].text
    else:
        for j in range(len(menu) - 1):    
            detail += menu[j].text
            detail += ', '
        detail += menu[-1].text
    result['fields']['detail'] = detail
    
    picture = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/a')
    driver.execute_script("arguments[0].click();", picture)
    
    next_pic_btn = driver.find_element(By.CLASS_NAME, 'link_next')
    original = driver.find_element(By.CLASS_NAME, 'link_original')
    
    pic1 = driver.find_element(By.CLASS_NAME, 'img_photo')
    result_image1 = {'model':'restaurant.restaurantimage', 'fields': {'image': pic1.get_attribute('src'), 'restaurant_id': i}}
    test_result_image.append(result_image1)
    
    driver.execute_script("arguments[0].click();", next_pic_btn)
    time.sleep(1)
    pic2 = driver.find_element(By.CLASS_NAME, 'img_photo')
    result_image2 = {'model':'restaurant.restaurantimage', 'fields': {'image': pic2.get_attribute('src'), 'restaurant_id': i}}
    test_result_image.append(result_image2)
    
    driver.execute_script("arguments[0].click();", next_pic_btn)
    time.sleep(1)
    pic3 = driver.find_element(By.CLASS_NAME, 'img_photo')
    result_image3 = {'model':'restaurant.restaurantimage', 'fields': {'image': pic3.get_attribute('src'), 'restaurant_id': i}}
    test_result_image.append(result_image3)
    
    driver.execute_script("arguments[0].click();", next_pic_btn)
    time.sleep(1)
    pic4 = driver.find_element(By.CLASS_NAME, 'img_photo')
    result_image4 = {'model':'restaurant.restaurantimage', 'fields': {'image': pic4.get_attribute('src'), 'restaurant_id': i}}
    test_result_image.append(result_image4)
    
    driver.execute_script("arguments[0].click();", next_pic_btn)
    time.sleep(1)
    pic5 = driver.find_element(By.CLASS_NAME, 'img_photo')
    result_image5 = {'model':'restaurant.restaurantimage', 'fields': {'image': pic5.get_attribute('src'), 'restaurant_id': i}}
    test_result_image.append(result_image5)
    
    # category = driver.find_element(By.CLASS_NAME, 'txt_location')
    # c.add(category.text)
            
    test_result.append(result)

with open('test.json', 'w', encoding='utf-8') as f:
    json.dump(test_result, f, ensure_ascii=False, indent=4)
    
with open('test_image.json', 'w', encoding='utf-8') as f:
    json.dump(test_result_image, f, ensure_ascii=False, indent=4)

# f = open('category.txt', 'w', encoding='utf-8')
# for cat in c:
#     f.write(cat)
#     f.write('\n')
    

    
