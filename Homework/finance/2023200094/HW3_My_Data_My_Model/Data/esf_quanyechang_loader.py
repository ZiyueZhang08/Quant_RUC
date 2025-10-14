import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re

# 配置 Selenium WebDriver
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

service = Service("/usr/local/bin/chromedriver")
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
driver = webdriver.Chrome(service=service, options=options)

url = 'https://tj.esf.fang.com/house-a037-b0154/'
driver.get(url)
table =driver.find_element('class name','shop_list')
table.text
rows = table.find_elements(By.TAG_NAME, 'dl')

data = []
i = 0
Num_Pages = 20
while i < Num_Pages:
        table = driver.find_element('class name','shop_list')
        rows = table.find_elements(By.TAG_NAME, 'dl')
        for row in rows:
            info_element = row.find_element(By.CSS_SELECTOR, "p.tel_shop")
            info_text = info_element.text
            area_match = re.search(r'(\d+\.?\d*)㎡', info_text)
            area = float(area_match.group(1)) if area_match else None
            
            price_element = row.find_element(By.CSS_SELECTOR, "dd.price_right span.red b")
            price = float(price_element.text)

            unit_price_element = row.find_element(By.CSS_SELECTOR, "dd.price_right span:not(.red)")
            unit_price_text = unit_price_element.text
            unit_price_match = re.search(r'(\d+\.?\d*)元/㎡', unit_price_text)
            unit_price = int(unit_price_match.group(1)) if unit_price_match else None
            
            data.append([area, price, unit_price])
        print(f"Page {i+1} done")

        try:
            next_button = driver.find_element(By.LINK_TEXT, "下一页")
            next_button.click()
        
        except NoSuchElementException:
            print("找不到“下一页”按钮，已到达最后一页，爬取结束。")
            break # 跳出整个循环
        i += 1

# 关闭浏览器
driver.quit()

df = pd.DataFrame(data, columns=['面积(㎡)', '总价(万)', '单价(元/㎡)'])
output_filename = 'Tianjin_Quanyechang_esf_data.xlsx'
df.to_excel(output_filename, index=False)