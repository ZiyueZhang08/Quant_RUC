# STEP1: Rent and house price data crawling
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import re
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException

# Initialize Edge browser driver
service = Service()
driver = webdriver.Edge(service=service)

# webpage_1
url = "https://zhangjiakou.zu.fang.com/house-a014963/#"
driver.get(url)

# Initialize data storage list
all_data = []
page_count = 0
max_pages = 3

# Start crawling loop
while page_count < max_pages:
    # Wait for page to load completely
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "houseList"))
        )
    except Exception:
        break

    # Get all property elements on current page
    house_elements = driver.find_elements(By.CSS_SELECTOR, ".list.hiddenMap.rel")

    # Iterate through each property element and extract data
    for house in house_elements:
        try:
            # Initialize dictionary to store current property data
            house_data = {}

            # Fixed field: region
            house_data["region"] = "Hebei-Xiahuayuan"

            # Extract p tag containing all information
            try:
                info_element = house.find_element(By.CSS_SELECTOR, ".font15.mt12.bold")
                full_text = info_element.text
                # Split by space and remove empty strings
                parts = [part.strip() for part in full_text.split("|") if part.strip()]

                # Assign values in order
                if len(parts) >= 1:
                    house_data["rental_type"] = parts[0]
                if len(parts) >= 2:
                    house_data["layout"] = parts[1]
                if len(parts) >= 3:
                    # Extract area number
                    area_match = re.search(r"(\d+)", parts[2])
                    if area_match:
                        house_data["area"] = float(area_match.group(1))
                    else:
                        house_data["area"] = None
                if len(parts) >= 4:
                    house_data["orientation"] = parts[3]

            except NoSuchElementException:
                continue

            # Extract monthly rent and convert to number
            try:
                rent_element = house.find_element(By.CLASS_NAME, "price")
                house_data["monthly_rent"] = float(rent_element.text)
            except (NoSuchElementException, ValueError):
                house_data["monthly_rent"] = None

            # Extract location description
            try:
                location_element = house.find_element(By.CSS_SELECTOR, ".gray6.mt12")
                house_data["location_description"] = location_element.text
            except NoSuchElementException:
                house_data["location_description"] = None

            # Add current property data to total list
            all_data.append(house_data)

        except Exception:
            continue
    
    # Next page button
    try:
        next_page = driver.find_element(By.LINK_TEXT, "下一页")
        next_page.click()
    except NoSuchElementException:
        break

    page_count += 1

# Convert to DataFrame and save data
df = pd.DataFrame(all_data)
df.to_csv("xiahuayuan_rental_data.csv", index=False, encoding="utf-8-sig")

# webpage_2
url = "https://zhangjiakou.esf.fang.com/house-a014963/"
driver.get(url)

# Initialize data storage list
all_data = []
page_count = 0
max_pages = 8

# Start crawling loop
while page_count < max_pages:
    # Wait for page to load completely
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".shop_list.shop_list_4"))
        )
    except Exception:
        break

    # Get all property elements on current page
    house_elements = driver.find_elements(
        By.CSS_SELECTOR, ".shop_list.shop_list_4>.clearfix"
    )

    # Iterate through each property element and extract data
    for house in house_elements:
        try:
            # Initialize dictionary to store current property data
            house_data = {}

            # Fixed field: region
            house_data["region"] = "Hebei-Xiahuayuan"

            # Extract p tag containing all information
            try:
                info_element = house.find_element(By.CLASS_NAME, "tel_shop")
                full_text = info_element.text
                # Split by | and remove empty strings
                parts = [part.strip() for part in full_text.split("|") if part.strip()]

                # Assign values in order
                if len(parts) >= 1:
                    house_data["layout"] = parts[0]
                if len(parts) >= 2:
                    house_data["area"] = parts[1]
                if len(parts) >= 3:
                    house_data["floor"] = parts[2]
                if len(parts) >= 4:
                    house_data["orientation"] = parts[3]
                if len(parts) >= 5:
                    house_data["construction_time"] = parts[4]

            except NoSuchElementException:
                continue

            # Extract price information
            try:
                price_dd = house.find_element(By.CLASS_NAME, "price_right")

                # Extract total price
                try:
                    total_price_element = price_dd.find_element(By.CLASS_NAME, "red")
                    house_data["total_price"] = total_price_element.text.strip()
                except NoSuchElementException:
                    house_data["total_price"] = None

                # Extract unit price
                try:
                    span = price_dd.find_element(By.CSS_SELECTOR, "span:last-of-type")
                    text = span.text.strip()
                    unit_price = text
                    house_data["unit_price"] = unit_price
                except NoSuchElementException:
                    house_data["unit_price"] = None

            except NoSuchElementException:
                house_data["total_price"] = None
                house_data["unit_price"] = None

            # Extract location description
            try:
                location_element = house.find_element(By.CLASS_NAME, "add_shop")
                house_data["location_description"] = location_element.text.replace(
                    "\n", " "
                ).replace("\r", " ")
            except NoSuchElementException:
                house_data["location_description"] = None

            # Add current property data to total list
            all_data.append(house_data)

        except Exception:
            continue
    
    # Next page button
    try:
        if page_count < max_pages - 1:
            next_page = driver.find_element(By.LINK_TEXT, "下一页")
            driver.execute_script("arguments[0].click();", next_page)
    except NoSuchElementException:
        break

    page_count += 1

# Convert to DataFrame and save data
df = pd.DataFrame(all_data)
df.to_csv("xiahuayuan_sell_data.csv", index=False, encoding="utf-8-sig")

# Close browser
driver.quit()