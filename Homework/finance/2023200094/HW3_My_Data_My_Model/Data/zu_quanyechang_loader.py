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

# 这里因为原先装有chromedriver的路径是/usr/local/bin/chromedriver
service = Service("/usr/local/bin/chromedriver")
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
driver = webdriver.Chrome(service=service, options=options)

url = 'https://tj.zu.fang.com/house-a037-b0154/'
driver.get(url)
table =driver.find_element('class name','houseList')
table.text
rows = table.find_elements(By.TAG_NAME, 'dl')

data = []
i = 0
Num_Pages = 20
while i < Num_Pages:
        table = driver.find_element('class name','houseList')
        rows = table.find_elements(By.TAG_NAME, 'dl')
        for row in rows:
            info_p_element = row.find_element(By.CSS_SELECTOR, "p.font15")
            info_text = info_p_element.text
            area_match = re.search(r'(\d+\.?\d*)㎡', info_text)
            area = int(area_match.group(1)) if area_match else None

            rent_span_element = row.find_element(By.CSS_SELECTOR, "span.price")
            rent_price_text = rent_span_element.text
            rent_price = int(rent_price_text) if rent_price_text else None

            data.append([area, rent_price])
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

df = pd.DataFrame(data, columns=['面积(㎡)', '租金(元/月)'])
output_filename = 'Tianjin_Quanyechang_zu_data.xlsx'
df.to_excel(output_filename, index=False)