from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import sqlite3
from datetime import datetime
from selenium.webdriver.firefox.options import Options

def bcad(driver, house):
    driver.get('https://esearch.brazoscad.org')
    sleep(1)
    textbox = driver.find_element(By.ID, "keywords")
    textbox.send_keys(house)
    textbox.send_keys(Keys.RETURN)
    print(f'Searching for {house}')
    sleep(3)
    driver.find_element(By.ID, "view-list").click()
    driver.find_element(By.XPATH, f"//a[contains(text(), '{house.upper()}')]").click()
    sleep(2)
    print('Clicked on link')
    #property_values = driver.find_element(By.XPATH, "//*[contains(text(), 'Assessed Value')]").text
    assessed_value = driver.find_element(By.XPATH, "//tr/th[contains(text(), 'Assessed Value')]/following-sibling::td").text
    appraised_value = driver.find_element(By.XPATH, "//tr/th[contains(text(), 'Appraised Value')]/following-sibling::td").text
    tax = driver.find_element(By.XPATH, "//strong[contains(text(), 'Estimated Taxes Without Exemptions: ')]").find_element(By.XPATH, "..").text.split('Estimated Taxes Without Exemptions: ')[1]
    return assessed_value, appraised_value, tax

db = sqlite3.connect('/home/ishank/propertydata-selenium/database.db')
cursor = db.cursor()
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
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
    assessed_value, appraised_value, tax = bcad(driver, name)
    # driver.get('https://esearch.brazoscad.org')
    # sleep(1)
    # textbox = driver.find_element(By.ID, "keywords")
    # textbox.send_keys(house)
    # textbox.send_keys(Keys.RETURN)
    # print(f'Searching for {house}')
    # sleep(3)
    # driver.find_element(By.ID, "view-list").click()
    # driver.find_element(By.XPATH, f"//a[contains(text(), '{house.upper()}')]").click()
    # sleep(2)
    # print('Clicked on link')
    # #property_values = driver.find_element(By.XPATH, "//*[contains(text(), 'Assessed Value')]").text
    # assessed_value = driver.find_element(By.XPATH, "//tr/th[contains(text(), 'Assessed Value')]/following-sibling::td").text
    # appraised_value = driver.find_element(By.XPATH, "//tr/th[contains(text(), 'Appraised Value')]/following-sibling::td").text
    # tax = driver.find_element(By.XPATH, "//strong[contains(text(), 'Estimated Taxes Without Exemptions: ')]").find_element(By.XPATH, "..").text.split('Estimated Taxes Without Exemptions: ')[1]
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
