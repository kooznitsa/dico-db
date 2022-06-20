import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from pprint import pprint


def scrape_tables(url, num_art):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    driver = webdriver.Chrome(r'chromedriver', options=options)
    driver.get(url)

    entries_num = 20 # number of entries per page
    n = 0 # number of output file

    while entries_num <= num_art:
        driver.implicitly_wait(20)
        table = driver.find_elements(By.TAG_NAME, 'table')[2].get_attribute('outerHTML')
        df = pd.read_html(table)
        # pprint(df)

        file_name = f'FR/legal/legal{n}.csv'
        df[0].to_csv(file_name, encoding='utf-8-sig', index=False) # [0] helps overcome ValueError

        try:
            driver.find_element(By.XPATH, "//a[text()='>>']").click() # 'next' button
            n += 1
            entries_num += 20
            print(entries_num)
        except exceptions.StaleElementReferenceException as e:
            for i in range(0, 4):
                try:
                    driver.refresh()
                    driver.implicitly_wait(10)
                    driver.find_element(By.XPATH, "//a[text()='>>']").click()
                    n += 1
                    entries_num += 20
                except:
                    print(e)
                    pass

    print('Finished')
    driver.quit()


scrape_tables('https://www.multitran.com/m.exe?a=110&l1=4&l2=2&sc=48', 25723)