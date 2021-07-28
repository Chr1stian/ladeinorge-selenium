from flask import Flask, request
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def login(phone, password):
    print("Getting driver")
    driver = webdriver.Remote("http://host.docker.internal:4444/wd/hub", DesiredCapabilities.CHROME.copy())


    print("Using driver to login")
    driver.get("https://ladeinorge.no/logg-inn")
    assert "Logg inn" in driver.title
    phone_input = driver.find_element_by_id("loginName")
    phone_input.clear()
    phone_input.send_keys(phone)

    password_input = driver.find_element_by_name("password")
    password_input.clear()
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    return driver


def start_charging(driver, charger_id):
    print("Starting to charge")
    try:
        element = WebDriverWait(driver, 10).until(
            EC.title_contains("tilgang til")
        )
    except:
        print("Error login in")

    driver.get("https://ladeinorge.no/start-ladestasjonen/" + charger_id)

    wait = WebDriverWait(driver, 5)
    try:
        wait.until(EC.visibility_of(driver.find_element_by_class_name("current-state")))
    except StaleElementReferenceException:
        print("Failed")
    except TimeoutException:
        print("Timed out - already charging")
        return

    try:
        driver.find_element_by_css_selector(
            "#chargingPoint > div.template.flex-just-center.flex.flex-grow.flex-column > form > div.hidden.available > div > button > div.label.label-success.scheme-green-gradient > span > svg").click()
        print("Started charging")
    except:
        print("Couldn't click/start charging")



app = Flask(__name__)


@app.route('/startCharging', methods=['get'])
def main():
    phone = request.args.get('phone', type=str, default='')
    password = request.args.get('password', type=str, default='')
    charger_id = request.args.get('charger', type=str, default='')

    driver = login(phone, password)
    start_charging(driver, charger_id)
    driver.quit()
    return "Started charging on " + charger_id

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')