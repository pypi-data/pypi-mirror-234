import csv
from datetime import date
from logging import getLogger
import requests
import time
from typing import Dict, List, Tuple

from selenium import webdriver
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


logger = getLogger(__name__)


def init_chromium(options):
    from selenium.webdriver.chrome.service import Service as ChromiumService
    from webdriver_manager.core.os_manager import ChromeType
    return webdriver.Chrome(
        service=ChromiumService(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        ),
        options=options
    )


def init_chrome(options):
    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )


def init_driver(driver_browser, user_agent):
    if driver_browser.startswith('chrom'):
        from selenium.webdriver import ChromeOptions

        options = ChromeOptions()

        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")  # Required for running in docker
        options.add_argument("--disable-setuid-sandbox")  # Required for docker
        options.add_argument('--disable-dev-shm-usage')  # attempt fix stability

        if driver_browser == 'chromium':
            return init_chromium(options=options)
        elif driver_browser == 'chrome':
            return init_chrome(options=options)

    raise ValueError(f'Unsupported Browser specified - {driver_browser}')


def initialize_service(
        user: str,
        password: str,
        driver_type: str,
        user_agent: str,
) -> webdriver:
    """If you disable 2FA it won't allow you to sign in,
    you need to have another email account for recovery.
    """
    driver = init_driver(driver_type, user_agent)
    time.sleep(2)
    login_google(driver, identifier=user, Passwd=password)
    time.sleep(1)

    return driver


def login_google(driver: ChromiumDriver, **kwargs) -> None:
    """Log in to Google services using Webdriver

    Using WebDriverWait() instead of time.sleep() as suggested by the docs.
    The password element has different terms for the input field and the button.

    Args:
        driver (webdriver): Selenium webdriver used to log in
        **kwargs: User and password
    """
    driver.get("https://accounts.google.com/ServiceLogin")
    driver_wait = WebDriverWait(driver, 30)

    for field, value in kwargs.items():
        driver_wait.until(
            EC.presence_of_element_located((By.NAME, field))
        ).send_keys(value)
        if str(field) == "Passwd":
            field = "password"
        parent_button = driver_wait.until(EC.element_to_be_clickable(
            (By.ID, str(field) + "Next"))
        )
        parent_button.find_element(By.TAG_NAME, "button").click()


def build_report_url(
        gb_account: str,
        start_date: str,
        end_date: str,
) -> Tuple[str, Dict]:
    """Cast the dates, build the url and params

    Args:
        gb_account (str): Numeric representation of the GB acc
        start_date (str): Start date for the report
        end_date (str): End date for the report

    Returns:
        (str, dict): url to download the report, params for the request
    """
    start = date.fromisoformat(start_date).strftime("%Y,%-m,%-d")
    end = date.fromisoformat(end_date).strftime("%Y,%-m,%-d")
    report_url = (
        f"https://play.google.com/books/publish/u/0/a/{gb_account}/"
        "downloadTrafficReport"
    )
    params = {"f.req": f"[[null,{start}],[null,{end}],2,0]"}

    return report_url, params


def get_report(report_url: str, driver: ChromiumDriver, params: Dict) -> str:
    """Once logged in Google, make a request to get the actual report.
    Gets the cookies from the selenium driver to allow you in.
    Sleep 5 seconds needed when you run the driver the first time as it's slow

    Args:
        report_url (str): url before the params
        driver (webdriver): driver needed to get the cookies
        params (dict): params for the request to Google Play Books
    Returns:
        str: decoded content csv from response
    """
    time.sleep(1)
    session = requests.Session()
    cookies = {
        cookie["name"]: cookie["value"]
        for cookie in driver.get_cookies()
        if cookie["domain"] == ".google.com"
    }

    response = session.get(report_url, cookies=cookies, params=params)
    response.raise_for_status()

    return response.content.decode("utf-16")


def required_fields_present(
        required_fields: list[str],
        all_fields: list[str],
) -> set[str]:
    """Return any values in required_fields that are missing from all_fields."""
    return set(required_fields) - set(all_fields)


def extract_report_content(report_content, expected_headers=None) -> List[Dict]:
    """Process Google Play Books report content, returning structured data.

    Args:
        report_content (str): Google Books Report content.
        expected_headers (list, optional): List of headers expected.
    Returns:
        list_results list[dict]: CSV content as list of dict objects.
    """
    reader = csv.DictReader(report_content.splitlines(), delimiter="\t")
    headers = reader.fieldnames

    expected_headers = expected_headers or []
    if missing_fields := required_fields_present(expected_headers, headers):
        raise ValueError(f"Required headers missing: {missing_fields}")

    return list(reader)


def fetch_report(
        gb_account: str,
        username: str,
        password: str,
        start_date: str,
        end_date: str,
        browser: str = 'chrome',  # default used by docker image
        user_agent: str = None,
) -> str:
    """Initialise Selenium, log in to Google, fetch the Google Books report.

    Args:
        gb_account (str): Numeric str representing the account.
        username (str): Username or email.
        password (str): Password.
        start_date (str): Start date for the report.
        end_date (str): End date for the report.
        browser (str): Browser for the driver - Chrome, Chromium, etc.
        user_agent (str): User-Agent HTTP header to use for requests.

    Returns:
        str: CSV response from Google Play Books.
    """
    agent = user_agent or (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    )
    report_url, params = build_report_url(gb_account, start_date, end_date)
    service = initialize_service(username, password, browser, agent)

    try:
        report_content = get_report(report_url, service, params)
        return report_content
    except (UnicodeDecodeError, ValueError, Exception) as err:
        logger.error(
            f"Failed to retrieve report {start_date}, {end_date}, "
            f"Error: {err}"
        )
        raise
    finally:
        service.close()
