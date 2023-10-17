import time
import traceback

from retrying import retry
import binascii

from quantplay.utils.selenium_utils import Selenium
from quantplay.exception.exceptions import (
    InvalidArgumentException,
    RetryableException,
    retry_exception,
    WrongLibrarySetup,
)
import pyotp
from selenium.common.exceptions import WebDriverException
import undetected_chromedriver as uc


class KiteUtils:
    zerodha_username = "zerodha_username"
    zerodha_password = "zerodha_password"
    zeordha_totp_unique_id = "zerodha_totp_unique_id"

    user_id_xpath = '//*[@id="container"]/div/div/div[2]/form/div[1]/input'
    password_xpath = '//*[@id="container"]/div/div/div[2]/form/div[2]/input'
    login_xpath = '//*[@id="container"]/div/div/div[2]/form/div[4]/button'
    kite_pin_xpath = (
        "/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/input"
    )
    authorize_xpath = "/html/body/div[1]/div/div[1]/div/div/form/div/button"

    @staticmethod
    def check_error(page_source):
        for error_message in [
            "User profile not found",
            "Invalid username or password",
            "Invalid TOTP",
        ]:
            if error_message in page_source:
                raise InvalidArgumentException(error_message)

        if "Invalid" in page_source:
            start_index = page_source.find("Invalid")
            print(page_source[start_index : min(start_index + 20, len(page_source))])

        if "Invalid" in page_source and "api_key":
            raise InvalidArgumentException(f"Invalid API Key")

    @staticmethod
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def get_request_token(api_key=None, user_id=None, password=None, totp=None):

        try:
            pyotp.TOTP(totp).now()
            driver = Selenium().get_browser()

            # TODO api should be fetched from configuration

            kite_url = "https://kite.trade/connect/login?api_key={}&v=3".format(api_key)
            print("Kite Url {}".format(kite_url))

            driver.get(kite_url)
            time.sleep(2)
            page_source = driver.page_source
            KiteUtils.check_error(page_source)

            user_id_element = driver.find_element("xpath", KiteUtils.user_id_xpath)
            password_element = driver.find_element("xpath", KiteUtils.password_xpath)

            user_id_element.send_keys(user_id)
            password_element.send_keys(password)

            login_attempt = driver.find_element("xpath", KiteUtils.login_xpath)
            login_attempt.submit()
            time.sleep(2)

            page_source = driver.page_source
            KiteUtils.check_error(page_source)

            kite_pin = driver.find_element("xpath", KiteUtils.kite_pin_xpath)
            kite_pin.send_keys(pyotp.TOTP(totp).now())
            time.sleep(1)

            page_source = driver.page_source
            KiteUtils.check_error(page_source)
            if "Authorize" in page_source:
                print(f"Authorizing {api_key}")
                authorize = driver.find_element("xpath", KiteUtils.authorize_xpath)
                authorize.submit()

            url = driver.current_url
            print("got kite url {}".format(url))
            request_token = url.split("token=")[1].split("&")[0]

            driver.close()

            return request_token
        except binascii.Error as e:
            raise InvalidArgumentException("Invalid TOTP key provided")
        except InvalidArgumentException as e:
            raise
        except WebDriverException as e:
            raise WrongLibrarySetup("Selenium setup need to be fixed")
        except Exception as e:
            print(traceback.print_exc())
            raise RetryableException(str(e))
