from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import sqlite3
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
load_dotenv()
import os

def bcad(driver, house):
    print("Searching in BCAD")
    driver.get('https://esearch.brazoscad.org')
    sleep(1)
    textbox = driver.find_element(By.ID, "keywords")
    textbox.send_keys(house)
    textbox.send_keys(Keys.RETURN)
    print(f'Searching for {house}')
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "view-list")))
    driver.find_element(By.ID, "view-list").click()
    sleep(0.5)
    driver.find_element(By.XPATH, f"//a[contains(text(), '{house.upper()}')]").click()
    sleep(2)
    print('Clicked on link')
    assessed_value = driver.find_element(By.XPATH, "//tr/th[contains(text(), 'Assessed Value')]/following-sibling::td").text
    print("Got assessed value")
    appraised_value = driver.find_element(By.XPATH, "//tr/th[contains(text(), 'Appraised Value')]/following-sibling::td").text
    print("Got appraised value")
    tax = driver.find_element(By.XPATH, "//strong[contains(text(), 'Estimated Taxes Without Exemptions: ')]").find_element(By.XPATH, "..").text.split('Estimated Taxes Without Exemptions: ')[1]
    print("Got tax")
    return assessed_value, appraised_value, tax

def wcad(driver, house):
    print("Searching in WCAD")
    driver.get('https://search.wcad.org/')
    sleep(1)
    textbox = driver.find_element(By.ID, "SearchText")
    textbox.send_keys(house)
    textbox.send_keys(Keys.RETURN)
    print(f'Searching for {house}')
    sleep(1)
    driver.find_element(By.XPATH, "//td[contains(text(), '{}')]".format(house.upper())).click()
    print('Clicked on link')
    dropdown = Select(driver.find_element(By.ID, "dnn_ctr1460_View_ddTaxYears"))
    dropdown.select_by_visible_text('2021')
    sleep(1)
    appraised_value = driver.find_element(By.ID, "dnn_ctr1460_View_tdVITotalAppraisedValue").text
    print("Got appraised value")
    assessed_value = driver.find_element(By.ID, "dnn_ctr1460_View_tdVITotalAssessedValueRP").text
    print("Got assessed value")
    driver.find_element(By.ID, "tdDropDownLinks").click()
    sleep(1)
    driver.find_element(By.XPATH, "//a[contains(text(), 'Tax Office')]").click()
    print("Clicked on tax office")
    # implicity wait 15 seconds
    sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "dnn_ctr377_View_tdPMCurrentAmountDue")))
    tax = driver.find_element(By.ID, 'dnn_ctr377_View_tdPMCurrentAmountDue').text
    print("Got tax")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return appraised_value, assessed_value, tax

db = sqlite3.connect(os.getenv('DATABASE_LOCATION'))
cursor = db.cursor()
options = Options()
options.headless = True if os.getenv('HEADLESS') == 'TRUE' else False
driver = webdriver.Chrome(options=options)
cursor.execute('SELECT name, cad FROM propertydata;')
houses = [house for house in cursor.fetchall()]
websites = {
    'b': 'https://esearch.brazoscad.org',
    'w': 'https://search.wcad.org'
}
print('Retrieved data from database')
for house in houses:
    name = house[0]
    cad = house[1]
    assessed_value, appraised_value, tax = bcad(driver, name) if cad == 'b' else wcad(driver, name)
    assessed_value = float(assessed_value.replace(',', '').replace('$', ''))
    appraised_value = float(appraised_value.replace(',', '').replace('$', ''))
    tax = float(tax.replace(',', '').replace('$', ''))
    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    last_assessed, last_appraised, last_tax = cursor.execute(f'SELECT current_assessed, current_appraised, current_tax FROM propertydata WHERE name = "{name}";').fetchone()
    cursor.execute(f"UPDATE propertydata SET current_assessed={assessed_value}, current_appraised={appraised_value}, current_tax={tax}, last_updated='{time}' WHERE name='{name}'")
    if last_assessed and last_appraised and tax:
        cursor.execute(f'UPDATE propertydata SET last_assessed={last_assessed}, last_appraised={last_appraised}, last_tax={last_tax} WHERE name = "{name}";')
db.commit()
cursor.close()
db.close()
driver.quit()
