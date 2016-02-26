import time
from django.core.management.base import BaseCommand
from selenium.webdriver.support import expected_conditions as EC
from selen.driver import SeleniumWebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from selen.models import TripAdvisorHotelCity

USA_TRIPADVISOR_HOTELS = 'http://www.tripadvisor.com/Hotels-g191-United_States-Hotels.html'

# python manage.py tripadvisor_hotels
class Command(BaseCommand):

    def get_next_page(self, driver):
        # page_numbers = driver.find_element_by_class_name('pageNumbers')
        wait = WebDriverWait(driver, 10)
        # page_numbers = wait.until(lambda driver: driver.find_element_by_class_name('pageNumbers'))
        page_numbers = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pageNumbers"))
        )
        page_numbers = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "pageNumbers"))
        )
        # current_page = wait.until(lambda page_numbers: page_numbers.find_element_by_class_name('current'))
        current_page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "current"))
        )
        current_page = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "current"))
        )
        # current_page = page_numbers.find_element_by_class_name('current')

        next_page = WebDriverWait(page_numbers, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, str(int(current_page.text) + 1)))
        )

        next_page = WebDriverWait(page_numbers, 10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, str(int(current_page.text) + 1)))
        )
        # next_page = wait.until(lambda page_numbers: page_numbers.find_element_by_link_text(str(int(current_page.text) + 1)))
        # next_page = page_numbers.find_element_by_link_text(str(int(current_page.text) + 1))
        if next_page:
            print next_page.text
        return next_page

    def handle(self, *args, **options):
        begin_time = time.time()
        print begin_time
        driver = SeleniumWebDriver(kind='chrome').driver
        driver.get(USA_TRIPADVISOR_HOTELS)
        next_page = self.get_next_page(driver)
        # pageCount = 431 #maybe change by dynamic getting thin number
        x = 0
        while next_page:
            SDTOPDESTCONTENT = driver.find_element_by_id('SDTOPDESTCONTENT')
            BROAD_GRID = SDTOPDESTCONTENT.find_element_by_id('BROAD_GRID')
            geo_wraps = BROAD_GRID.find_elements_by_class_name('geo_wrap') #it should be 20 or less
            for geo_wrap in geo_wraps:
                geo_name = geo_wrap.find_element_by_class_name('geo_name')
                a = geo_name.find_element_by_tag_name('a')
                name = a.text
                url = a.get_attribute('href')
                obj, created = TripAdvisorHotelCity.objects.get_or_create(name=name, url=url)
            next_page.click()
            next_page = self.get_next_page(driver)
            x += 1

        print x
        print time.time() - begin_time

        driver.close()