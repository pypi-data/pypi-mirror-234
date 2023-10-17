import abc
import json
import time
from tempfile import mkdtemp
from typing import Optional

import pytz
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from dynamodb.dynamodb import DynamoDB

COLOMBIA_TZ = pytz.timezone('America/Bogota')


class AbstractAutomation(abc.ABC):

    def __init__(self, url: str, table: str, profile_id: str):
        self.url = url
        self.driver = self.__get_driver()
        self.db = DynamoDB(table=table)
        self.profile_id = profile_id

    def __get_driver(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        service = Service(executable_path='/opt/chromedriver')
        options.binary_location = '/opt/chrome/chrome'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9222")
        chrome = webdriver.Chrome(service=service, options=options)
        return chrome

    def login_task(self, *, user: str, pw: str) -> None:
        user_input = "/html/body/div[1]/div/div[1]/main/div/div/div/div/div[1]/div/div[1]/form/div/div[1]/div/input"
        pw_input = "/html/body/div[1]/div/div[1]/main/div/div/div/div/div[1]/div/div[1]/form/div/div[2]/div/input"
        login_button = "/html/body/div[1]/div/div[1]/main/div/div/div/div/div[1]/div/div[2]/button"
        self.driver.get(f"{self.url}/auth/login")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, login_button)))
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, login_button)))
        self.driver.find_element(by=By.XPATH, value=user_input).send_keys(user)
        self.driver.find_element(by=By.XPATH, value=pw_input).send_keys(pw)
        self.driver.find_element(by=By.XPATH, value=login_button).click()
        time.sleep(3)
        print("profile logged")

    def get_script(
        self, *, service: str, body: Optional[dict] = None
    ) -> str:
        url = f"{self.url}{service}"
        headers = {
            "accept": "application/json",
            "accept-language": "es-US,es-419;q=0.9,es;q=0.8",
            "content-type": "application/json",
            "sec-ch-ua": r'\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": r'\"Windows\"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }
        payload = {
            "headers": headers,
            "referrer": f"{self.url}/search/all",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "body": json.dumps(body) if body else {},
            "method": "POST",
            "mode": "cors",
            "credentials": "include"
        }
        script = """
            response = await fetch("{}", {});
            const string = await response.text();
            return string === "" ? response : JSON.parse(string);;
            """.format(url, payload)
        return script
