from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains


class InfoGetter(object):
    """ Класс с логикой парсинга данных из объекта BeautifulSoup"""

    @staticmethod
    def get_name(soup_content):
        """ Получение названия организации """

        try:
            for data in soup_content.find_all("h1", {"class": "orgpage-header-view__header"}):
                name = data.getText()

            return name
        except Exception:
            return ""

    @staticmethod
    def get_phone(soup_content):
        """ Получение телефона организации """

        try:
            phones = []
            for data in soup_content.find_all("div", {"class": "card-phones-view__number"}):
                phone = data.getText()
                phones.append(phone)
            return phones
        except Exception:
            return []


    @staticmethod
    def get_social(soup_content):
        """ Получение соц сети организации """

        try:
            socials = []
            for data in soup_content.find_all("a", {"class": "button _view_secondary-gray _ui _size_medium _link"}):
                social = data['href']
                socials.append(social)
            return socials
        except Exception:
            return []

    @staticmethod
    def get_address(soup_content):
        """ Получение адреса организации """

        try:
            for data in soup_content.find_all("a", {"class": "business-contacts-view__address-link"}):
                address = data.getText()

            return address
        except Exception:
            return ""

    @staticmethod
    def get_website(soup_content):
        """ Получение сайта организации"""

        try:
            for data in soup_content.find_all("span", {"class": "business-urls-view__text"}):
                website = data.getText()

            return website
        except Exception:
            return ""

    @staticmethod
    def get_opening_hours(soup_content):
        """ Получение графика работы"""

        opening_hours = []
        try:
            for data in soup_content.find_all("meta", {"itemprop": "openingHours"}):
                opening_hours.append(data.get('content'))

            return opening_hours
        except Exception:
            return ""

    @staticmethod
    def get_goods(soup_content):
        """ Получение списка товаров и услуг"""

        dishes = []
        prices = []

        try:
            # Получаем название блюда/товара/услуги (из меню-витрины)
            for dish_s in soup_content.find_all("div", {"class": "related-item-photo-view__title"}):
                dishes.append(dish_s.getText())

            # Получаем цену блюда/товара/услуги (из меню-витрины)
            for price_s in soup_content.find_all("span", {"class": "related-product-view__price"}):
                prices.append(price_s.getText())

            # Получаем название блюда/товара/услуги (из меню-списка)
            for dish_l in soup_content.find_all("div", {"class": "related-item-list-view__title"}):
                dishes.append(dish_l.getText())

            # Получаем цену блюда/товара/услуги (из меню-списка)
            for price_l in soup_content.find_all("div", {"class": "related-item-list-view__price"}):
                prices.append(price_l.getText())

        # Если меню организации полностью представлено в виде списка
        except NoSuchElementException:
            try:
                # Получаем название блюда/товара/услуги (из меню-списка)
                for dish_l in soup_content.find_all("div", {"class": "related-item-list-view__title"}):
                    dishes.append(dish_l.getText())

                # Получаем цену блюда/товара/услуги (из меню-списка)
                for price_l in soup_content.find_all("div", {"class": "related-item-list-view__price"}):
                    prices.append(price_l.getText())
            except Exception:
                pass

        except Exception:
            return ""

        return dict(zip(dishes, prices))

    @staticmethod
    def get_rating(soup_content):
        """ Получение рейтинга организации"""

        rating = ""
        try:
            for data in soup_content.find_all("span", {"class": "business-summary-rating-badge-view__rating-text"}):
                rating += data.getText()
            return rating
        except Exception:
            return ""

    @staticmethod
    def get_reviews(soup_content, driver):
        """ Получение отзывов о организации"""

        reviews = []
        slider = driver.find_element_by_class_name(name='scroll__scrollbar-thumb')

        # Узнаём количество отзывов
        try:
            reviews_count = int(soup_content.find_all("div", {"class": "tabs-select-view__counter"})[-1].text)

        except ValueError:
            reviews_count = 0

        except AttributeError:
            reviews_count = 0

        except Exception:
            return ""

        if reviews_count > 150:
            find_range = range(100)
        else:
            find_range = range(30)

        for i in find_range:
            try:
                ActionChains(driver).click_and_hold(slider).move_by_offset(0, 50).release().perform()

            except MoveTargetOutOfBoundsException:
                break

        try:
            soup_content = BeautifulSoup(driver.page_source, "lxml")
            for data in soup_content.find_all("div", {"class": "business-review-view__body-text _collapsed"}):
                reviews.append(data.getText())

            return reviews
        except Exception:
            return ""
