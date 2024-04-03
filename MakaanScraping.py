from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

BHK, type, locations, prices, sqfts, statuses, deposits, availabilities, bathroom_list = [], [], [], [], [], [], [], [], []

driver = webdriver.Chrome()
base_url = 'https://www.makaan.com/hyderabad-property/kompally-rental-flats-51562'


for page_num in range(1, 3):
    page_url = f'{base_url}'
    driver.get(page_url)

    wait = WebDriverWait(driver, 10)

    cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/main/div/div/div[2]/div/div[2]/div/div[1]/div[3]/ul/li/div')))

    for card in cards:
        details_bhk_type = card.find_element(By.XPATH, ".//div/div[3]/div[1]/div[1]/a/strong")
        text_dbt = details_bhk_type.text
        br_hs_parts = text_dbt.split('BHK')

        if len(br_hs_parts) == 2:
            br, hs = br_hs_parts
        else:
            br = hs = ''

        location = card.find_element(By.XPATH, ".//div/div[3]/div[1]/div[2]/div/span/span/span/a/span[1]/strong")
        text_loc = location.text
        price = card.find_element(By.XPATH, ".//div/div[3]/table/tbody/tr[2]/td[1]/div/span[1]")
        text_prc = price.text
        sqft = card.find_element(By.XPATH, ".//div/div[3]/table/tbody/tr[3]/td[1]/span")
        text_sqft = sqft.text
        status = card.find_element(By.XPATH, ".//div/div[3]/table/tbody/tr[4]/td[1]")
        text_status = status.text
        deposit = card.find_element(By.XPATH, ".//div/div[3]/ul/li[1]/span/strong")
        text_dpst = deposit.text
        deposit_amnt = text_dpst.split('deposit')[0]

        try:
            availability = card.find_element(By.XPATH, ".//div/div[3]/ul/li[2]/span/strong/span")
            avl = availability.text
        except NoSuchElementException:
            avl = 'N/A'
            #print("Availability element not found.")

        try:
            bathrooms_element = card.find_element(By.XPATH, ".//div/div[3]/ul/li[3]/span")
            text_bthrms = bathrooms_element.text
            tot_bthrms = text_bthrms.split('bathrooms')[0]
        except NoSuchElementException:
            text_bthrms = 'N/A'

        BHK.append(br.strip())
        type.append(hs.strip())
        locations.append(text_loc.strip())
        prices.append(text_prc.strip())
        sqfts.append(text_sqft.strip())
        statuses.append(text_status.strip())
        deposits.append(deposit_amnt.strip())
        availabilities.append(avl.strip())
        #bathroom_list.append(tot_bthrms.strip())

driver.quit()

data = {
    'BHK': BHK,
    'Type': type,
    'Location': locations,
    'Price': prices,
    'Sqft': sqfts,
    'Status': statuses,
    'Deposit': deposits,
    'Availability': availabilities,
    'Bathrooms': bathroom_list
}

final_df = pd.DataFrame(data)

print(final_df.to_string())
final_df.to_csv('scrapped.csv', index=False)
