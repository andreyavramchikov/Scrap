from selenium import webdriver


class SeleniumWebDriver(object):
    def __init__(self, kind=None, mode=False):

        if kind == 'chrome':
            #chromedriver = "/Users/adam/Downloads/chromedriver"
            # driver = webdriver.Chrome(chromedriver)
            chromeOptions = webdriver.ChromeOptions()
            prefs = {"profile.managed_default_content_settings.images":2}
            chromeOptions.add_experimental_option("prefs",prefs)
            self.driver = webdriver.Chrome(executable_path='/home/andrey/projects/scraping/chromedriver', chrome_options=chromeOptions)

        elif kind == 'firefox':
            if mode:
                self.driver = webdriver.Firefox()
            else:
                firefox_profile = webdriver.FirefoxProfile()
                # Disable CSS
                firefox_profile.set_preference('permissions.default.stylesheet', 2)
                # Disable images
                firefox_profile.set_preference('permissions.default.image', 2)
                # Disable Flash
                firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
                # Set the modified profile while creating the browser object
                self.driver = webdriver.Firefox(firefox_profile=firefox_profile)
