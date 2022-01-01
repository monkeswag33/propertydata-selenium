from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from redfin import Redfin
from time import sleep
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import os

def bcad(driver, house, assessed_appraised_tax, max_tries, tries=0):
    if tries >= max_tries:
        print(f"Errored more than {max_tries} times, exiting")
        return
    try:
        tries += 1
        print("Searching in BCAD")
        driver.get('https://esearch.brazoscad.org')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "keywords")))
        textbox = driver.find_element(By.ID, "keywords")
        textbox.send_keys(house)
        sleep(1)
        textbox.send_keys(Keys.RETURN)
        print(f'Searching for {house}')
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "view-list")))
        driver.find_element(By.ID, "view-list").click()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{house.upper()}')]")))
        driver.find_element(By.XPATH, f"//a[contains(text(), '{house.upper()}')]").click()
        print('Clicked on link')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//tr/th[contains(text(), 'Assessed Value')]/following-sibling::td")))
        assessed_appraised_tax[0] = driver.find_element(By.XPATH, "//tr/th[contains(text(), 'Assessed Value')]/following-sibling::td").text
        print("Got assessed value")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//tr/th[contains(text(), 'Appraised Value')]/following-sibling::td")))
        assessed_appraised_tax[1] = driver.find_element(By.XPATH, "//tr/th[contains(text(), 'Appraised Value')]/following-sibling::td").text
        print("Got appraised value")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//strong[contains(text(), 'Estimated Taxes Without Exemptions: ')]")))
        assessed_appraised_tax[2] = driver.find_element(By.XPATH, "//strong[contains(text(), 'Estimated Taxes Without Exemptions: ')]").find_element(By.XPATH, "..").text.split('Estimated Taxes Without Exemptions: ')[1]
        print("Got tax")
    except KeyboardInterrupt:
        driver.quit()
        exit()
    except Exception as e:
        print(e)
        print("Error, Retrying")
        bcad(driver, house, assessed_appraised_tax, max_tries, tries)

def wcad(driver, house, assessed_appraised_tax, max_tries, tries=0):
    if tries >= max_tries:
        print(f"Errored more than {max_tries} times, exiting")
        return
    try:
        print("Searching in WCAD")
        driver.get('https://search.wcad.org/')
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "SearchText")))
        textbox = driver.find_element(By.ID, "SearchText")
        textbox.send_keys(house)
        textbox.send_keys(Keys.RETURN)
        print(f'Searching for {house}')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//td[contains(text(), '{}')]".format(house.upper()))))
        driver.find_element(By.XPATH, "//td[contains(text(), '{}')]".format(house.upper())).click()
        print('Clicked on link')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "dnn_ctr1460_View_ddTaxYears")))
        dropdown = Select(driver.find_element(By.ID, "dnn_ctr1460_View_ddTaxYears"))
        dropdown.select_by_visible_text('2021')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "dnn_ctr1460_View_tdVITotalAppraisedValue")))
        assessed_appraised_tax[0] = driver.find_element(By.ID, "dnn_ctr1460_View_tdVITotalAppraisedValue").text
        print("Got appraised value")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "dnn_ctr1460_View_tdVITotalAssessedValueRP")))
        assessed_appraised_tax[1] = driver.find_element(By.ID, "dnn_ctr1460_View_tdVITotalAssessedValueRP").text
        print("Got assessed value")
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "tdDropDownLinks")))
        driver.find_element(By.ID, "tdDropDownLinks").click()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Tax Office')]")))
        driver.find_element(By.XPATH, "//a[contains(text(), 'Tax Office')]").click()
        print("Clicked on tax office")
        sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "dnn_ctr377_View_tdPMCurrentAmountDue")))
        tax = ''
        while not tax:
            tax = driver.find_element(By.ID, 'dnn_ctr377_View_tdPMCurrentAmountDue').text
        assessed_appraised_tax[2] = tax
        print("Got tax")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except KeyboardInterrupt:
        driver.quit()
        exit()
    except Exception as e:
        print(e)
        print("Error, Retrying")
        wcad(driver, house, assessed_appraised_tax, max_tries, tries)

def fmv(driver, client, house):
    house = house + ' Hutto'
    response = client.search(house)
    url = response['payload']['exactMatch']['url']
    initial_info = client.initial_info(url)['payload']
    avm_details = client.avm_details(initial_info['propertyId'], initial_info['listingId'])
    print("Got Redfin FMV")
    driver.get('https://trulia.com/')
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'banner-search')))
    textbox = driver.find_element(By.ID, 'banner-search')
    textbox.send_keys(house)
    textbox.send_keys(Keys.RETURN)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 nBoMt']")))
    trulia_fmv = driver.find_element(By.XPATH, "//div[@class='Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 nBoMt']").text
    print("Got Trulia FMV")
    return (avm_details['payload']['predictedValue'], trulia_fmv)

db = psycopg2.connect(os.getenv('POSTGRES_URI'))
table_name = ('prod_' if os.getenv('ENVIRONMENT') == 'PROD' else 'dev_') + 'propertydata'
print(table_name)
cursor = db.cursor()
options = Options()
options.headless = True if os.getenv('HEADLESS') == 'TRUE' else False
driver = webdriver.Firefox(options=options)
cursor.execute(f'SELECT name, cad FROM {table_name};')
houses = [house for house in cursor.fetchall()]
client = Redfin()
print('Retrieved data from database')
for house in houses:
    name = house[0]
    cad = house[1]
    assessed_appraised_tax = [None, None, None]
    bcad(driver, name, assessed_appraised_tax, 5) if cad == 'b' else wcad(driver, name, assessed_appraised_tax, 5)
    assessed_value = float(assessed_appraised_tax[0].replace(',', '').replace('$', ''))
    appraised_value = float(assessed_appraised_tax[1].replace(',', '').replace('$', ''))
    tax = float(assessed_appraised_tax[2].replace(',', '').replace('$', ''))
    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    if cad == 'w':
        redfin_fmv, zillow_fmv = fmv(driver, client, name)
        zillow_fmv = float(zillow_fmv.replace(',', '').replace('$', ''))
        average_fmv = (zillow_fmv + redfin_fmv) / 2
        cursor.execute(f"UPDATE {table_name} SET zillow_fmv={zillow_fmv}, redfin_fmv={redfin_fmv}, avg_fmv={average_fmv} WHERE name='{name}';")
        
    cursor.execute(f"SELECT current_assessed, current_appraised, current_tax FROM {table_name} WHERE name = '{name}';")
    last_assessed, last_appraised, last_tax = cursor.fetchone()
    cursor.execute(f"UPDATE {table_name} SET current_assessed={assessed_value}, current_appraised={appraised_value}, current_tax={tax} WHERE name='{name}'")
    if last_assessed and last_appraised and tax:
        cursor.execute(f"UPDATE {table_name} SET last_assessed={last_assessed}, last_appraised={last_appraised}, last_tax={last_tax} WHERE name = '{name}';")
db.commit()
cursor.close()
db.close()
driver.quit()
