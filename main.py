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

class Searcher():
    def __init__(self, max_tries=5, database=False):
        self.max_tries = max_tries
        options = Options()
        options.headless = True if os.getenv('HEADLESS') == 'TRUE' else False
        self.driver = webdriver.Firefox(options=options)
        self.client = Redfin()
        if database == True:
            self.db = psycopg2.connect(os.getenv('POSTGRES_URI'))
            self.cursor = self.db.cursor()
        self.table_name = ('prod_' if os.getenv('ENVIRONMENT') == 'PROD' else 'dev_') + 'propertydata'
        self.assessed_appraised_tax = {
            'assessed_value': None,
            'appraised_value': None,
            'tax': None
        }
        self.fmv = None

    def bcad(self, house):
        print("Searching in BCAD")
        def get_house_info():
            tries = 0
            while tries <= self.max_tries:
                try:
                    self.driver.get('https://esearch.brazoscad.org')
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "keywords")))
                    textbox = self.driver.find_element(By.ID, "keywords")
                    textbox.send_keys(house)
                    sleep(1)
                    textbox.send_keys(Keys.RETURN)
                    print(f'Searching for {house}')
                    WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.ID, "view-list")))
                    self.driver.find_element(By.ID, "view-list").click()
                    WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{house.upper()}')]")))
                    self.driver.find_element(By.XPATH, f"//a[contains(text(), '{house.upper()}')]").click()
                    print('Clicked on link')
                    return True
                except:
                    print('Error getting page info, Retrying')
                    tries += 1
        def assessed_value():
            tries = 0
            while tries <= self.max_tries:
                try:
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//tr/th[contains(text(), 'Assessed Value')]/following-sibling::td")))
                    assessed_value = self.driver.find_element(By.XPATH, "//tr/th[contains(text(), 'Assessed Value')]/following-sibling::td").text
                    self.assessed_appraised_tax['assessed_value'] = assessed_value
                    print("Got assessed value")
                    break
                except:
                    sleep(1)
                    print('Error getting assessed value, Retrying')
                    tries += 1
        def appraised_value():
            tries = 0
            while tries <= self.max_tries:
                try:
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//tr/th[contains(text(), 'Appraised Value')]/following-sibling::td")))
                    appraised_value = self.driver.find_element(By.XPATH, "//tr/th[contains(text(), 'Appraised Value')]/following-sibling::td").text
                    self.assessed_appraised_tax['appraised_value'] = appraised_value
                    print("Got appraised value")
                    break
                except:
                    sleep(1)
                    print('Error getting appraised value, Retrying')
                    tries += 1
        def tax():
            tries = 0
            while tries <= self.max_tries:
                try:
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//strong[contains(text(), 'Estimated Taxes Without Exemptions: ')]")))
                    tax = self.driver.find_element(By.XPATH, "//strong[contains(text(), 'Estimated Taxes Without Exemptions: ')]").find_element(By.XPATH, "..").text.split('Estimated Taxes Without Exemptions: ')[1]
                    if not tax: raise ValueError('Tax is empty')
                    self.assessed_appraised_tax['tax'] = tax
                    print("Got tax value")
                    break
                except:
                    sleep(1)
                    print('Error getting tax value, Retrying')
                    tries += 1
        if get_house_info():
            assessed_value()
            appraised_value()
            tax()

    def wcad(self, house):
        print("Searching in WCAD")
        self.driver.get('https://search.wcad.org/')
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.ID, "SearchText")))
        textbox = self.driver.find_element(By.ID, "SearchText")
        textbox.send_keys(house)
        textbox.send_keys(Keys.RETURN)
        print(f'Searching for {house}')
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//td[contains(text(), '{}')]".format(house.upper()))))
        self.driver.find_element(By.XPATH, "//td[contains(text(), '{}')]".format(house.upper())).click()
        print('Clicked on link')
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "dnn_ctr1460_View_ddTaxYears")))
        dropdown = Select(self.driver.find_element(By.ID, "dnn_ctr1460_View_ddTaxYears"))
        dropdown.select_by_visible_text('2021')
        def assessed_value(max_tries):
            tries = 0
            while tries <= max_tries:
                try:
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "dnn_ctr1460_View_tdVITotalAssessedValueRP")))
                    assessed = self.driver.find_element(By.ID, "dnn_ctr1460_View_tdVITotalAssessedValueRP").text
                    self.assessed_appraised_tax['assessed_value'] = assessed
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
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "dnn_ctr1460_View_tdVITotalAppraisedValue")))
                    appraised = self.driver.find_element(By.ID, "dnn_ctr1460_View_tdVITotalAppraisedValue").text
                    self.assessed_appraised_tax['appraised_value'] = appraised
                    print("Got appraised value")
                    break
                except:
                    sleep(1)
                    print("Error retreiving appraised value, Retrying")
                    tries += 1
        assessed_value(self.max_tries)
        appraised_value(self.max_tries)
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID, "tdDropDownLinks")))
        self.driver.find_element(By.ID, "tdDropDownLinks").click()
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Tax Office')]")))
        self.driver.find_element(By.XPATH, "//a[contains(text(), 'Tax Office')]").click()
        print("Clicked on tax office")
        sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[1])
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "dnn_ctr377_View_divBillDetails")))
        div = self.driver.find_element(By.ID, "dnn_ctr377_View_divBillDetails")
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
                    self.assessed_appraised_tax['tax'] = tax
                    print("Got tax")
                    break
                except:
                    sleep(1)
                    print("Error retrieving tax, Retrying")
                    tries += 1
        get_tax(self.max_tries)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def get_fmv(self, house):
        house = house + ' Hutto'
        for i in range(self.max_tries):
            try:
                response = self.client.search(house)
                url = response['payload']['exactMatch']['url']
                initial_info = self.client.initial_info(url)['payload']
                avm_details = self.client.avm_details(initial_info['propertyId'], initial_info['listingId'])
                break
            except ConnectionError:
                print("Connection Error, Retrying")
        print("Got Redfin FMV")
        self.driver.get('https://trulia.com/')
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, 'banner-search')))
        textbox = self.driver.find_element(By.ID, 'banner-search')
        textbox.send_keys(house)
        textbox.send_keys(Keys.RETURN)
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 nBoMt']")))
        trulia_fmv = self.driver.find_element(By.XPATH, "//div[@class='Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 nBoMt']").text
        print("Got Trulia FMV")
        self.fmv = (avm_details['payload']['predictedValue'], trulia_fmv)

    def reset_data(self):
        self.assessed_appraised_tax = {
            'assessed_value': None,
            'appraised_value': None,
            'tax': None
        }
        self.fmv = None

    def insert_database(self, name):
        if self.assessed_appraised_tax['assessed_value']: self.assessed_appraised_tax['assessed_value'] = float(self.assessed_appraised_tax['assessed_value'].replace(',', '').replace('$', ''))
        if self.assessed_appraised_tax['appraised_value']: self.assessed_appraised_tax['appraised_value'] = float(self.assessed_appraised_tax['appraised_value'].replace(',', '').replace('$', ''))
        if self.assessed_appraised_tax['tax']: self.assessed_appraised_tax['tax'] = float(self.assessed_appraised_tax['tax'].replace(',', '').replace('$', ''))
        if self.fmv:
            redfin_fmv, zillow_fmv = self.fmv
            zillow_fmv = float(zillow_fmv.replace(',', '').replace('$', ''))
            average_fmv = round((zillow_fmv + redfin_fmv) / 2, 2)
            self.cursor.execute(f"UPDATE {self.table_name} SET zillow_fmv={zillow_fmv}, redfin_fmv={redfin_fmv}, avg_fmv={average_fmv} WHERE name='{name}';")
            print('Updated FMV')
        self.cursor.execute(f"SELECT current_assessed, current_appraised, current_tax FROM {self.table_name} WHERE name = '{name}';")
        last_assessed, last_appraised, last_tax = self.cursor.fetchone()
        if any(value for value in [last_assessed, last_appraised, last_tax]):
            query = 'UPDATE {table_name} SET {values} WHERE name={house};'
            subquery = []
            for key, value in {'last_assessed': last_assessed, 'last_appraised': last_appraised, 'last_tax': last_tax}.items():
                if value:
                    subquery.append(f'{key}={value}')
            query = query.format(table_name=self.table_name, values=','.join(subquery), house=f"'{name}'")
            self.cursor.execute(query)
        if any(value for value in self.assessed_appraised_tax.values()):
            query = 'UPDATE {table_name} SET {values}, last_updated=now() WHERE name={house};'
            subquery = []
            for key, value in {'current_assessed': self.assessed_appraised_tax['assessed_value'], 'current_appraised': self.assessed_appraised_tax['appraised_value'], 'current_tax': self.assessed_appraised_tax['tax']}.items():
                if value:
                    subquery.append(f'{key}={value}')
            query = query.format(table_name=self.table_name, values=', '.join(subquery), house=f"'{name}'")
            print(query)
            self.cursor.execute(query)
        print(f"Updated {name}")
        self.assessed_appraised_tax = {
            'assessed_value': None,
            'appraised_value': None,
            'tax': None
        }
        self.fmv = None

    def shutdown(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()
        self.driver.quit()


def main():
    searcher = Searcher(database=True)
    searcher.cursor.execute(f'SELECT name, cad FROM {searcher.table_name};')
    houses = [house for house in searcher.cursor.fetchall()]
    print(searcher.table_name)
    print('Retrieved data from database')
    for house in houses:
        name, cad = house
        searcher.bcad(name) if cad == 'b' else searcher.wcad(name)
        if cad == 'w': searcher.get_fmv(name)
        searcher.insert_database(name)
    searcher.shutdown()
if __name__ == '__main__':
    main()
