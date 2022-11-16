import os
import json
import random
import argparse

from time import sleep

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

from infogetter import InfoGetter
from utils import json_pattern


class Parser:

    def __init__(self, driver):
        self.driver = driver

    def parse_data(self, hrefs, type_org):
        self.driver.maximize_window()
        self.driver.get('https://yandex.ru/maps')
        parent_handle = self.driver.window_handles[0]
        org_id = 0
        outputs = []

        for organization_url in hrefs:
            try:
            # if True:
                self.driver.execute_script(f'window.open("{organization_url}","org_tab");')
                child_handle = [x for x in self.driver.window_handles if x != parent_handle][0]
                self.driver.switch_to.window(child_handle)
                sleep(1)
                soup = BeautifulSoup(self.driver.page_source, "lxml")
                org_id += 1
                name = InfoGetter.get_name(soup)
                address = InfoGetter.get_address(soup)
                website = InfoGetter.get_website(soup)
                opening_hours = InfoGetter.get_opening_hours(soup)
                ypage = self.driver.current_url
                rating = InfoGetter.get_rating(soup)
                social = InfoGetter.get_social(soup)
                phone = InfoGetter.get_phone(soup)
                goods, reviews = None, None
                output = json_pattern.into_json(org_id, name, address, website, opening_hours, ypage, goods, rating,
                                                reviews, phone, social)
                outputs.append(output)

                if len(outputs) % 100 == 0:
                    df = pd.DataFrame()
                    df['outputs'] = outputs
                    df.to_csv(f'result_output/{type_org}_outputs.csv')
                    self.driver.quit()
                    sleep(random.uniform(2.2, 2.4))
                    self.driver = webdriver.Safari()
                    self.driver.maximize_window()
                    self.driver.get('https://yandex.ru/maps')
                    parent_handle = self.driver.window_handles[0]
                print(f'Данные добавлены, id - {org_id}')

                self.driver.switch_to.window(parent_handle)
                sleep(random.uniform(0.2, 0.4))

            except:
                print('except')
                # driver.quit()
                sleep(random.uniform(2.2, 2.4))
                self.driver = webdriver.Safari()
                self.driver.maximize_window()
                self.driver.get('https://yandex.ru/maps')
                parent_handle = self.driver.window_handles[0]
        print('Данные сохранены')
        self.driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type_org", help="organization type")
    args = parser.parse_args()
    type_org = args.type_org

    all_hrefs = []
    files = os.listdir(f'links/{type_org}')
    for file in files:
        with open(f'links/{type_org}/{file}', 'r', encoding='utf-8') as f:
            hrefs = json.load(f)['1']
            all_hrefs += hrefs
    all_hrefs = list(set(all_hrefs))
    print('all_hrefs', len(all_hrefs))


    driver = webdriver.Safari()
    parser = Parser(driver)
    parser.parse_data(all_hrefs, type_org)