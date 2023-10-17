import requests
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from liveramp_automation.utils.allure import allure_drive_screenshot, allure_page_screenshot
from liveramp_automation.utils.log import Logger
from liveramp_automation.utils.playwright import PlaywrightUtils
from liveramp_automation.utils.selenium import SeleniumUtils
from liveramp_automation.utils.time import fixed_wait


class LoginHepler:
    OKTA_LOGIN_ROUTED_TIME_SECONDS = 10

    @staticmethod
    def liveramp_okta_login_page(page, url, username, password, seconds=OKTA_LOGIN_ROUTED_TIME_SECONDS):
        """
        Facilitates Okta login using Playwright.

        :param page: Playwright page object.
        :param url: URL of the Okta login page.
        :param username: Okta username.
        :param password: Okta password.
        :param seconds: Optional time to wait after successful login (default: 10 seconds).
        """

        page.goto(url)
        page.wait_for_load_state()
        url_new = page.url
        Logger.info("The current url is {}.".format(url_new))
        if url_new.__contains__(url):
            Logger.info("Already logged in to OKTA.")
        else:
            page.get_by_label("Username").fill(username)
            page.get_by_label("Username").press("Enter")
            allure_page_screenshot(page, "username_filled")
            page.get_by_label("Password").fill(password)
            page.get_by_label("Password").press("Enter")
            allure_page_screenshot(page, "password_filled")
            Logger.info("Logging in to OKTA...")
            fixed_wait(15)
            PlaywrightUtils(page).close_popup_banner()

    @staticmethod
    def liveramp_okta_login_driver(driver, url, username, password, seconds=OKTA_LOGIN_ROUTED_TIME_SECONDS):
        """
        Facilitates Okta login using Playwright.

        :param driver: Selennium Webdriver object.
        :param url: URL of the Okta login page.
        :param username: Okta username.
        :param password: Okta password.
        :param seconds: Optional time to wait after successful login (default: 20 seconds).
        """

        Logger.info("Going to login to OKTA...")
        Logger.info("The login URL is {}".format(url))
        driver.get(url)
        fixed_wait()
        if url in driver.current_url:
            Logger.info("Already logged in to OKTA.")
        else:
            username_box = driver.find_element(by=By.ID, value='idp-discovery-username')
            username_box.send_keys(username)
            username_box.send_keys(Keys.ENTER)
            allure_drive_screenshot(driver, "username_filled")
            fixed_wait()
            # changed on Aug 20
            # password_box = driver.find_element(by=By.ID, value='okta-signin-password')
            password_box = driver.find_element(by=By.CSS_SELECTOR, value="input[type='password']")
            password_box.send_keys(password)
            password_box.send_keys(Keys.ENTER)
            allure_drive_screenshot(driver, "passwrod_filled")
            Logger.info("Logging in to OKTA...")
            fixed_wait(seconds)
            Logger.info("Successfully logged in to OKTA.")
            # Logger.info("Trying to close the banners..")
            # fixed_wait(20)
            # SeleniumUtils(driver).close_popup_banner()
            # SeleniumUtils(driver).close_pendo_banners()
            # Logger.info("Close the popups while there are banners.")

    @staticmethod
    def call_oauth2_get_token(username, password) -> str:
        """Initiates an OAuth2 login to obtain an access token.
        Both the API username and password (sensitive) are mandatory for this process.
        Please ensure that you provide the required username and password from os.environ[] when calling this API.
        :param username:
        :param password:
        :return: str
        """
        data = {
            "grant_type": "password",
            "scope": "openid",
            "client_id": "liveramp-api"
        }
        Logger.info("Initiating OAuth2 login...")
        Logger.info("Default parameters: {}".format(data))
        headers = {"content-type": "application/x-www-form-urlencoded"}
        data.update(username=username)
        data.update(password=password)
        response = requests.post(
            "https://serviceaccounts.liveramp.com/authn/v1/oauth2/token", data=data, headers=headers)
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            token_type = response.json().get('token_type')
            if access_token and token_type:
                Logger.info("OAuth2 login successful.")
                return "{} {}".format(token_type, access_token)
            else:
                Logger.error("Invalid response data: {}".format(response.json()))
        else:
            Logger.error("OAuth2 login failed. Status code: {}".format(response.status_code))
