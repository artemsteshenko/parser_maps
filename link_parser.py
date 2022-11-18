import os
import random
import json
import argparse
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains

from utils.constants import districts, ACCEPT_BUTTON, type_org_mapping

class LinksCollector:

    def __init__(self, driver, link='https://yandex.ru/maps', max_errors=5, accept_button=ACCEPT_BUTTON):
        self.driver = driver
        self.slider = None
        self.max_errors = max_errors
        self.link = link
        self.accept_button = accept_button

    def _init_driver(self):
        self.driver.maximize_window()


    def _open_page(self, request):
        self.driver.get(self.link)
        sleep(random.uniform(1, 2))
        self.driver.find_element_by_class_name(name='search-form-view__input').send_keys(request)
        sleep(random.uniform(0.4, 0.7))
        self.driver.find_element_by_class_name(name='small-search-form-view__button').click()
        # Нажимаем на кнопку поиска
        sleep(random.uniform(1.4, 2))
        self.slider = self.driver.find_element_by_class_name(name='scroll__scrollbar-thumb')

        # Соглашение куки
        # flag = True
        # count = 0
        # while flag:
        #     try:
        #         count += 1
        #         sleep(3)
        #         self.driver.find_element_by_xpath(self.accept_button).click()
        #         flag = False
        #     except:
        #         if count > 5:
        #             self.driver.quit()
        #             self.init_driver()
        #             self.open_page(request)
        #         flag = True


    def run(self, city, district, type_org_ru, type_org):
        self._init_driver()
        request = city + ' ' + district + ' ' + type_org_ru
        self._open_page(request)
        organizations_hrefs = []

        count = 0
        link_number = [0]
        errors = 0
        while self.max_errors > errors:
            try:
                ActionChains(self.driver).click_and_hold(self.slider).move_by_offset(0, int(100/errors)).release().perform()
                slider_organizations_hrefs = self.driver.find_elements_by_class_name(name='search-snippet-view__link-overlay')
                slider_organizations_hrefs = [href.get_attribute("href") for href in slider_organizations_hrefs]
                organizations_hrefs = list(set(organizations_hrefs + slider_organizations_hrefs))
                count += 1
                if count % 3 == 0:
                    if len(organizations_hrefs) == link_number[-1]:
                        errors = errors + 1
                    print(len(organizations_hrefs))
                    link_number.append(len(organizations_hrefs))

                sleep(random.uniform(0.05, 0.1))
            except Exception:
                errors = errors + 1
                print('errors', errors)
                sleep(random.uniform(0.3, 0.4))

        directory = f'links/{type_org}'
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.driver.quit()
        with open(f'{directory}/{request}.json', 'w') as file:
            json.dump({'1': organizations_hrefs}, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type_org", help="organization type")
    args = parser.parse_args()
    type_org = args.type_org

    for type_org in ['translator', 'accountant', 'massage']:
        for district in districts:
            sleep(1)
            driver = webdriver.Safari()
            grabber = LinksCollector(driver)
            grabber.run(city="Москва", district=district, type_org_ru=type_org_mapping[type_org], type_org=type_org)

