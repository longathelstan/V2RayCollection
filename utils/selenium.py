from seleniumwire import webdriver
import config


class Selenium:
    def init_driver(proxy=False):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-oopr-debug-crash-dump")
        options.add_argument("--no-crash-upload")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-low-res-tiling")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        options.add_experimental_option(
            "prefs", {"profile.managed_default_content_settings.images": 2})
        if proxy:
            driver = webdriver.Chrome(
                options=options, seleniumwire_options=config.seleniumwire_options)
        else:
            driver = webdriver.Chrome(options=options)
        return driver
