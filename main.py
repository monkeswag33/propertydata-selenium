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
from dotenv import load_dotenv
load_dotenv()
import os

def bcad(driver, house, assessed_appraised_tax, max_tries):
    print("Searching in BCAD")
    def get_house_info(max_tries):
        tries = 0
        while tries <= max_tries:
            try:
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
                return True
            except:
                print('Error getting page info, Retrying')
                tries += 1
    def assessed_value(max_tries):
        tries = 0
        while tries <= max_tries:
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//tr/th[contains(text(), 'Assessed Value')]/following-sibling::td")))
                assessed_value = driver.find_element(By.XPATH, "//tr/th[contains(text(), 'Assessed Value')]/following-sibling::td").text
                assessed_appraised_tax['assessed_value'] = assessed_value
                print("Got assessed value")
                break
            except:
                sleep(1)
                print('Error getting assessed value, Retrying')
                tries += 1
    def appraised_value(max_tries):
        tries = 0
        while tries <= max_tries:
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//tr/th[contains(text(), 'Appraised Value')]/following-sibling::td")))
                appraised_value = driver.find_element(By.XPATH, "//tr/th[contains(text(), 'Appraised Value')]/following-sibling::td").text
                assessed_appraised_tax['appraised_value'] = appraised_value
                print("Got appraised value")
                break
            except:
                sleep(1)
                print('Error getting appraised value, Retrying')
                tries += 1
    # create function to get tax value
    # function name is "tax"
    def tax(max_tries):
        tries = 0
        while tries <= max_tries:
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//strong[contains(text(), 'Estimated Taxes Without Exemptions: ')]")))
                tax = driver.find_element(By.XPATH, "//strong[contains(text(), 'Estimated Taxes Without Exemptions: ')]").find_element(By.XPATH, "..").text.split('Estimated Taxes Without Exemptions: ')[1]
                if not tax: raise ValueError('Tax is empty')
                assessed_appraised_tax['tax'] = tax
                print("Got tax value")
                break
            except:
                sleep(1)
                print('Error getting tax value, Retrying')
                tries += 1
    if get_house_info(max_tries):
        assessed_value(max_tries)
        appraised_value(max_tries)
        tax(max_tries)

def wcad(driver, house, assessed_appraised_tax, max_tries):
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
    def assessed_value(max_tries):
        tries = 0
        while tries <= max_tries:
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "dnn_ctr1460_View_tdVITotalAssessedValueRP")))
                assessed = driver.find_element(By.ID, "dnn_ctr1460_View_tdVITotalAssessedValueRP").text
                assessed_appraised_tax['assessed_value'] = assessed
                print("Got assessed value")
                break
            except:
                sleep(1)
                print("Error retreiving assessed value, Retrying")
                tries += 1
    def appraised_value(max_tries):
        tries = 0
        while tries <= max_tries:
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "dnn_ctr1460_View_tdVITotalAppraisedValue")))
                appraised = driver.find_element(By.ID, "dnn_ctr1460_View_tdVITotalAppraisedValue").text
                assessed_appraised_tax['appraised_value'] = appraised
                print("Got appraised value")
                break
            except:
                sleep(1)
                print("Error retreiving appraised value, Retrying")
                tries += 1
    assessed_value(max_tries)
    appraised_value(max_tries)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "tdDropDownLinks")))
    driver.find_element(By.ID, "tdDropDownLinks").click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Tax Office')]")))
    driver.find_element(By.XPATH, "//a[contains(text(), 'Tax Office')]").click()
    print("Clicked on tax office")
    sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "dnn_ctr377_View_divBillDetails")))
    div = driver.find_element(By.ID, "dnn_ctr377_View_divBillDetails")
    div = div.find_elements(By.TAG_NAME, "div")[0]
    table = div.find_elements(By.TAG_NAME, "table")[1]
    tbody = table.find_element(By.TAG_NAME, "tbody")
    tr = tbody.find_elements(By.TAG_NAME, "tr")[-1]
    def get_tax(max_tries):
        tries = 0
        while tries <= max_tries:
            try:
                tax = tr.find_elements(By.TAG_NAME, "td")[1].text
                if not tax: raise ValueError("Tax is empty")
                assessed_appraised_tax['tax'] = tax
                print("Got tax")
                break
            except:
                sleep(1)
                print("Error retrieving tax, Retrying")
                tries += 1
    get_tax(max_tries)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def fmv(driver, client, house, retries=5):
    house = house + ' Hutto'
    for i in range(retries):
        try:
            response = client.search(house)
            url = response['payload']['exactMatch']['url']
            initial_info = client.initial_info(url)['payload']
            avm_details = client.avm_details(initial_info['propertyId'], initial_info['listingId'])
            break
        except ConnectionError:
            print("Connection Error, Retrying")
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

def init_programs():
    options = Options()
    options.headless = True if os.getenv('HEADLESS') == 'TRUE' else False
    driver = webdriver.Firefox(options=options)
    client = Redfin()
    return driver, client

def main():
    driver, client = init_programs()
    db = psycopg2.connect(os.getenv('POSTGRES_URI'))
    cursor = db.cursor()
    table_name = ('prod_' if os.getenv('ENVIRONMENT') == 'PROD' else 'dev_') + 'propertydata'
    cursor.execute(f'SELECT name, cad FROM {table_name};')
    houses = [house for house in cursor.fetchall()]
    print(table_name)
    print('Retrieved data from database')
    for house in houses:
        name = house[0]
        print(name)
        cad = house[1]
        assessed_appraised_tax = {
            'assessed_value': None,
            'appraised_value': None,
            'tax': None
        }
        if cad == 'w': continue
        bcad(driver, name, assessed_appraised_tax, 5) if cad == 'b' else wcad(driver, name, assessed_appraised_tax, 5)
        print(assessed_appraised_tax)
        if assessed_appraised_tax['assessed_value']: assessed_appraised_tax['assessed_value'] = float(assessed_appraised_tax['assessed_value'].replace(',', '').replace('$', ''))
        if assessed_appraised_tax['appraised_value']: assessed_appraised_tax['appraised_value'] = float(assessed_appraised_tax['appraised_value'].replace(',', '').replace('$', ''))
        if assessed_appraised_tax['tax']: assessed_appraised_tax['tax'] = float(assessed_appraised_tax['tax'].replace(',', '').replace('$', ''))
        if cad == 'w':
            redfin_fmv, zillow_fmv = fmv(driver, client, name)
            zillow_fmv = float(zillow_fmv.replace(',', '').replace('$', ''))
            average_fmv = round((zillow_fmv + redfin_fmv) / 2, 2)
            cursor.execute(f"UPDATE {table_name} SET zillow_fmv={zillow_fmv}, redfin_fmv={redfin_fmv}, avg_fmv={average_fmv} WHERE name='{name}';")
            print('Updated FMV')
        cursor.execute(f"SELECT current_assessed, current_appraised, current_tax FROM {table_name} WHERE name = '{name}';")
        last_assessed, last_appraised, last_tax = cursor.fetchone()
        if any(value for value in [last_assessed, last_appraised, last_tax]):
            query = 'UPDATE {table_name} SET {values} WHERE name={house};'
            subquery = []
            for key, value in {'last_assessed': last_assessed, 'last_appraised': last_appraised, 'last_tax': last_tax}.items():
                if value:
                    subquery.append(f'{key}={value}')
            query = query.format(table_name=table_name, values=','.join(subquery), house=f"'{name}'")
            cursor.execute(query)
        if any(value for value in assessed_appraised_tax.values()):
            query = 'UPDATE {table_name} SET {values}, last_updated=now() WHERE name={house};'
            subquery = []
            for key, value in {'current_assessed': assessed_appraised_tax['assessed_value'], 'current_appraised': assessed_appraised_tax['appraised_value'], 'current_tax': assessed_appraised_tax['tax']}.items():
                if value:
                    subquery.append(f'{key}={value}')
            query = query.format(table_name=table_name, values=', '.join(subquery), house=f"'{name}'")
            print(query)
            cursor.execute(query)
        print(f"Updated {name}")
    db.commit()
    cursor.close()
    db.close()
    driver.quit()
if __name__ == '__main__':
    main()
