import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_example_title():
    opts = Options()
    if os.getenv("CI", "0") == "1":
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    try:
        driver.get("https://example.com")
        time.sleep(1)
        h1 = driver.find_element(By.TAG_NAME, "h1").text.lower()
        assert "example" in h1
    finally:
        driver.quit()
