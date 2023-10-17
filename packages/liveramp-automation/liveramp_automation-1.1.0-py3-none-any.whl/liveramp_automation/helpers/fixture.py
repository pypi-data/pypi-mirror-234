import os
import pytest
from selenium import webdriver
from liveramp_automation.helpers.file import FileHelper
from liveramp_automation.utils.log import Logger
from typing import Generator
from playwright.sync_api import Playwright, BrowserContext


###########################
# Resource Prefix handle #
##########################

@pytest.fixture(scope="module")
def res():
    """Get the configuration for the test environment.

    :return: Configuration dictionary for the test environment.
    """
    Logger.info("It is going to import the envChoice.")
    if not os.environ.get('ENVCHOICE'):
        os.environ['ENVCHOICE'] = "prod"
    runEnv = os.environ['ENVCHOICE']
    Logger.info("The testing environment is {} ".format(runEnv))
    init_dict = FileHelper.read_init_file(os.getcwd(), 'pytest.ini')
    Logger.info(init_dict)
    try:
        if init_dict and init_dict['data']:
            resource_data = init_dict['data']
            if resource_data['resource_path']:
                resource_path = resource_data['resource_path']
            else:
                resource_path = 'resources'
                Logger.warning("Use the resource as the default resource_path.")
            if resource_data['resource_prefix']:
                resource_prefix = resource_data['resource_prefix']
            else:
                resource_prefix = 'res'
                Logger.warning("Use the res as the default resource_prefix.")
    except TypeError:
        resource_path = 'resources'
        resource_prefix = 'res'
        Logger.warning("Use the resource and res as the default resource_path and resource_prefix.")
    return FileHelper.load_env_yaml(resource_path, resource_prefix, runEnv)


###############################################################################################################
# API Prefix handle # We consider it's better to add the fixture methods to your own conftest.py
##############################################################################################################


################################################
# UI Automation Testing Prefix handle #
###############################################
@pytest.fixture(scope="module")
def driver():
    """Pytest fixture that provides a Selenium WebDriver instance for testing.
        Yields:
            WebDriver: A Selenium WebDriver instance for testing purposes.
    """
    if not os.environ.get('runEnv'):
        os.environ['runEnv'] = "remote"
    runEnv = os.environ['runEnv']
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    config_data = FileHelper.read_init_file(os.getcwd(), "pytest.ini", "r")
    Logger.info(config_data)
    download_dir = config_data.get('download', 'reports/download')
    default_directory = os.path.join(os.getcwd(), download_dir)
    prefs = {"download.default_directory": default_directory}
    chrome_options.add_experimental_option("prefs", prefs)
    Logger.info("The run Env is {}".format(runEnv))
    Logger.info("Run WEBDriver on lang=en ")
    chrome_options.add_argument('--lang=en')

    if runEnv == "remote":
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('window-size=1920x1480')
    else:
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('window-size=1920x1480')

    driver = webdriver.Chrome(options=chrome_options)

    driver.maximize_window()
    Logger.info("We are going to open a blank page.")
    driver.get("about:blank")
    driver.implicitly_wait(30)
    Logger.info("Started a ChromeDriver.")
    yield driver
    driver.close()
    Logger.info("Closed the ChromeDriver.Goodbye!")


@pytest.fixture(scope="module")
def page(playwright: Playwright) -> Generator[BrowserContext, None, None]:
    """ Pytest fixture that provides a Playwright BrowserContext for testing.
       Args:
           playwright (Playwright): Playwright instance.
       Yields:
           BrowserContext: A Playwright BrowserContext for testing purposes.
    """
    if not os.environ.get('runEnv'):
        os.environ['runEnv'] = "remote"
    config_data = FileHelper.read_init_file(os.getcwd(), "pytest.ini", "r")
    Logger.info(config_data)
    download_dir = config_data.get('download', 'reports/download')
    default_directory = os.path.join(os.getcwd(), download_dir)
    if os.environ['runEnv'] == "remote":
        context = playwright.chromium.launch_persistent_context("", headless=True, downloads_path=default_directory)
    else:
        context = playwright.chromium.launch_persistent_context("", headless=False, downloads_path=default_directory,
                                                                args=['--lang=en'])
    page = context.new_page()
    page.set_default_timeout(60000)
    yield page
    page.close()
    context.close()
