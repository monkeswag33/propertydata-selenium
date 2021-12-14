from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import sqlite3

db = sqlite3.connect('database.db')
cursor = db.cursor()
driver = webdriver.Firefox()
driver.get('https://esearch.brazoscad.org')

house_name = "802 San Pedro"
textbox = driver.find_element(By.ID, "keywords")
textbox.send_keys(house_name)
textbox.send_keys(Keys.RETURN)
sleep(3)
driver.find_element(By.ID, "view-list").click()
driver.find_element(By.XPATH, f"//a[contains(text(), '{house_name.upper()}')]").click()
sleep(2)
#property_values = driver.find_element(By.XPATH, "//*[contains(text(), 'Assessed Value')]").text
assessed_value = driver.find_element(By.XPATH, "//tr/th[contains(text(), 'Assessed Value')]/following-sibling::td").text
appraised_value = driver.find_element(By.XPATH, "//tr/th[contains(text(), 'Appraised Value')]/following-sibling::td").text
tax = driver.find_element(By.XPATH, "//strong[contains(text(), 'Estimated Taxes Without Exemptions: ')]").find_element(By.XPATH, "..").text.split('Estimated Taxes Without Exemptions: ')[1]
assessed_value = float(assessed_value.replace(',', '').replace('$', ''))
appraised_value = float(appraised_value.replace(',', '').replace('$', ''))
tax = float(tax.replace(',', '').replace('$', ''))
cursor.execute(f"UPDATE propertydata SET assessed={assessed_value}, appraised={appraised_value}, tax={tax} WHERE name='{house_name}'")
db.commit()
cursor.close()
db.close()