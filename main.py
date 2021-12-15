from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import sqlite3
from datetime import datetime

db = sqlite3.connect('database.db')
cursor = db.cursor()
driver = webdriver.Firefox()
cursor.execute('SELECT name FROM propertydata;')
houses = [house[0] for house in cursor.fetchall()]
for house in houses:
    driver.get('https://esearch.brazoscad.org')
    sleep(1)
    textbox = driver.find_element(By.ID, "keywords")
    textbox.send_keys(house)
    textbox.send_keys(Keys.RETURN)
    sleep(3)
    driver.find_element(By.ID, "view-list").click()
    driver.find_element(By.XPATH, f"//a[contains(text(), '{house.upper()}')]").click()
    sleep(2)
    #property_values = driver.find_element(By.XPATH, "//*[contains(text(), 'Assessed Value')]").text
    assessed_value = driver.find_element(By.XPATH, "//tr/th[contains(text(), 'Assessed Value')]/following-sibling::td").text
    appraised_value = driver.find_element(By.XPATH, "//tr/th[contains(text(), 'Appraised Value')]/following-sibling::td").text
    tax = driver.find_element(By.XPATH, "//strong[contains(text(), 'Estimated Taxes Without Exemptions: ')]").find_element(By.XPATH, "..").text.split('Estimated Taxes Without Exemptions: ')[1]
    assessed_value = float(assessed_value.replace(',', '').replace('$', ''))
    appraised_value = float(appraised_value.replace(',', '').replace('$', ''))
    tax = float(tax.replace(',', '').replace('$', ''))
    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    cursor.execute(f"UPDATE propertydata SET current_assessed={assessed_value}, current_appraised={appraised_value}, current_tax={tax}, last_updated='{time}' WHERE name='{house}'")
db.commit()
cursor.close()
db.close()