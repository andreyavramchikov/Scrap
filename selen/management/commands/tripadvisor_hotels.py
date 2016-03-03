import time
from django.core.management.base import BaseCommand
from selenium.webdriver.support import expected_conditions as EC
from selen.driver import SeleniumWebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException, NoSuchElementException
from optparse import make_option

from selen.models import TripAdvisorHotelCity, TripAdvisorHotel, TripAdvisorHotelInfo

USA_TRIPADVISOR_HOTELS = 'http://www.tripadvisor.com/Hotels-g191-United_States-Hotels.html'


# python manage.py tripadvisor_hotels
class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
       make_option('--all-links', dest='all-links', help='all-links', default=''),
       make_option('--start', dest='start', help='all-links', default=''),
       make_option('--end', dest='end', help='all-links', default=''),
    )

    def get_next_page(self, driver):
        page_numbers = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pageNumbers"))
        )
        # page_numbers = WebDriverWait(driver, 20).until(
        #     EC.visibility_of_element_located((By.CLASS_NAME, "pageNumbers"))
        # )
        current_page = WebDriverWait(page_numbers, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "current"))
        )
        # current_page = WebDriverWait(page_numbers, 20).until(
        #     EC.visibility_of_element_located((By.CLASS_NAME, "current"))
        # )

        next_page = WebDriverWait(page_numbers, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, str(int(current_page.text) + 1)))
        )

        # next_page = WebDriverWait(page_numbers, 20).until(
        #     EC.visibility_of_element_located((By.LINK_TEXT, str(int(current_page.text) + 1)))
        # )

        return next_page

    def save_main_category_links(self, driver):
        begin_time = time.time()
        driver.get(USA_TRIPADVISOR_HOTELS)
        next_page = self.get_next_page(driver)
        # pageCount = 431
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
                TripAdvisorHotelCity.objects.get_or_create(name=name, url=url)
            next_page.click()
            try:
                next_page = self.get_next_page(driver)
            except Exception as e:
                print 1
                try:
                    next_page = self.get_next_page(driver)
                except Exception as e:
                    print '2'
                    try:
                        next_page = self.get_next_page(driver)
                    except:
                        print 'x = '
                        print x
                        next_page = None
            x += 1

        if not next_page:
            print time.time() - begin_time
            TripAdvisorHotelCity.objects.get_or_create(name='DONE', url='DONE')

    def get_all_page_links(self, driver):
        pages = driver.find_elements_by_class_name('')
        return pages

    def get_pages(self, driver, city):
        try:
            a = driver.find_element_by_css_selector('.pageNumbers').find_elements_by_tag_name('a')
        except NoSuchElementException:
            return [city.url]
        last_link = a[len(a)-1]
        second_link = a[0].get_attribute('href')
        count_of_pages = last_link.text
        pages = [city.url]
        for i in range(2, int(count_of_pages)):
            pages.append(second_link.replace('oa30', 'oa' + str(i * 30)))

        return pages

    def save_city_links(self, driver, city):
        driver.get(city.url)
        time.sleep(3)
        pages = self.get_pages(driver, city)
        for page in pages:
            driver.get(page)
            time.sleep(2)
            elements = driver.find_elements_by_css_selector('#taplc_hotels_list_short_cells2_0 .prw_rup.prw_common_short_cell_thumbnail a')
            for element in elements:
                TripAdvisorHotel.objects.get_or_create(name='name', url=element.get_attribute('href'), category=city)

    def save_second_type_category_links(self, driver, start=None, end=None):
        cities = TripAdvisorHotelCity.objects.filter(done=False)[start:end] if start and end else TripAdvisorHotelCity.objects.filter(done=False)
        for city in cities:
            self.save_city_links(driver, city)
            city.done = True
            city.save()
            print city.name
 

    def get_element_by_selector(self, driver, selector):
        try:
            # return WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            return driver.find_element_by_css_selector(selector)
        except NoSuchElementException as e:
            return None

    def get_elements_by_selector(self, driver, selector):
        try:
            return driver.find_elements_by_css_selector(selector)
        except NoSuchElementException as e:
            return None

    def get_text_of_element(self, driver, element, index=None):
        if not element:
            return None
        if index is not None:
            try:
                return element[index].text
            except IndexError:
                return None
        else:
            return element.text

    def handle(self, *args, **options):
        # from selenium import webdriver
        # driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)

        driver = SeleniumWebDriver(kind='chrome').driver
        if not options.get('all-links'):
            if TripAdvisorHotelCity.objects.filter(name='DONE', url='DONE').first():

                start = options.get('start')
                end = options.get('end')
                self.save_second_type_category_links(driver, start, end)
            else:
                self.save_main_category_links(driver)
                self.save_second_type_category_links(driver)
        else:
            # go thhrought all links
            start = options.get('start')
            end = options.get('end')
            for link in TripAdvisorHotel.objects.filter(done=False)[start:end]:
                driver.get(link.url)
                name = ''
                street_address = ''
                extended_address = ''
                locality_spans = ''
                city = ''
                state = ''
                postal = ''
                phone = ''
                email = ''
                email_text = ''
                website = ''
                website_text = ''
                time.sleep(2)
                name = self.get_element_by_selector(driver, '#HEADING_GROUP .heading_name')
                name = name.text if name else ''
                street_address = self.get_element_by_selector(driver, '#HEADING_GROUP .format_address .street-address')
                extended_address = self.get_element_by_selector(driver, '#HEADING_GROUP .format_address .extended-address')
                locality_spans = self.get_elements_by_selector(driver, '#HEADING_GROUP .format_address .locality span')
                if locality_spans:
                    city = self.get_text_of_element(driver, locality_spans, 0)
                    state = self.get_text_of_element(driver, locality_spans, 1)
                    postal = self.get_text_of_element(driver, locality_spans, 2)

                elements = self.get_elements_by_selector(driver, '#HEADING_GROUP .bl_details .fl.contact_item')
                if elements:
                    phone = self.get_text_of_element(driver, elements, 0)
                    try:
                        email = elements[2]
                    except IndexError:
                        pass
                    if email and self.get_text_of_element(driver, elements, 2) == 'E-mail hotel':
                        email.click()
                        email_text = self.get_element_by_selector(driver, '.text.emailOwnerReadonly')
                        email_text = email_text.get_attribute('value') if email_text else ''
                        print email_text
                        driver.refresh()

                elements = self.get_elements_by_selector(driver, '#HEADING_GROUP .bl_details .fl.contact_item')
                try:
                    website = elements[1]
                except IndexError:
                    website = None

                if website and website.text == 'Hotel website':
                    website.click()
                    time.sleep(4)
                    driver.switch_to_window(driver.window_handles[1])
                    website_text = driver.current_url
                    driver.close()
                    driver.switch_to_window(driver.window_handles[0])
                    print website_text

                TripAdvisorHotelInfo.objects.create(hotel=link, name=name, url=link.url,
                                                    city=city, state=state,
                                                    postal=postal, phone=phone,
                                                    website=website_text, email=email_text)
                link.done = True
                link.save()