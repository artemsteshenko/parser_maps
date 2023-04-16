from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains


class SoupContentParser(object):

    def get_name(self, soup_content):
        try:
            for data in soup_content.find_all("h1", {"class": "orgpage-header-view__header"}):
                name = data.getText()
            return name
        except Exception:
            return ""

    def get_phone(self, soup_content):
        try:
            phones = []
            for data in soup_content.find_all("div", {"class": "card-phones-view__number"}):
                phone = data.getText()
                phones.append(phone)
            return phones
        except Exception:
            return []

    def get_social(self, soup_content):
        try:
            socials = []
            for data in soup_content.find_all("a", {"class": "button _view_secondary-gray _ui _size_medium _link"}):
                social = data['href']
                socials.append(social)
            return socials
        except Exception:
            return []

    def get_address(self, soup_content):
        try:
            for data in soup_content.find_all("a", {"class": "business-contacts-view__address-link"}):
                address = data.getText()
            return address
        except Exception:
            return ""

    def get_website(self, soup_content):
        try:
            for data in soup_content.find_all("span", {"class": "business-urls-view__text"}):
                website = data.getText()
            return website
        except Exception:
            return ""

    def get_opening_hours(self, soup_content):
        opening_hours = []
        try:
            for data in soup_content.find_all("meta", {"itemprop": "openingHours"}):
                opening_hours.append(data.get('content'))
            return opening_hours
        except Exception:
            return ""

    def get_goods(self, soup_content):
        dishes = []
        prices = []
        try:
            for dish_s in soup_content.find_all("div", {"class": "related-item-photo-view__title"}):
                dishes.append(dish_s.getText())

            for price_s in soup_content.find_all("span", {"class": "related-product-view__price"}):
                prices.append(price_s.getText())

            for dish_l in soup_content.find_all("div", {"class": "related-item-list-view__title"}):
                dishes.append(dish_l.getText())

            for price_l in soup_content.find_all("div", {"class": "related-item-list-view__price"}):
                prices.append(price_l.getText())

        except NoSuchElementException:
            try:
                for dish_l in soup_content.find_all("div", {"class": "related-item-list-view__title"}):
                    dishes.append(dish_l.getText())

                for price_l in soup_content.find_all("div", {"class": "related-item-list-view__price"}):
                    prices.append(price_l.getText())
            except Exception:
                pass
        except Exception:
            return ""

        return dict(zip(dishes, prices))

    def get_rating(self, soup_content):
        rating = ""
        try:
            for data in soup_content.find_all("span", {"class": "business-summary-rating-badge-view__rating-text"}):
                rating += data.getText()
            return rating
        except Exception:
            return ""

    def get_reviews(self, soup_content, driver):
        reviews = []
        slider = driver.find_element_by_class_name(name='scroll__scrollbar-thumb')
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
