
from selenium.webdriver.chromium.options import ChromiumOptions

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    ask_for_taxi_button = (By.XPATH, '//div[@class="results-text"]//button[@class="button round"]')
    comfort_tariff = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')
    phone_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[1]/div')
    phone_field = (By.ID, 'phone')
    send_code_button = (By.XPATH, '// *[ @ id = "root"] / div / div[1] / div[2] / div[1] / form / div[2] / button')
    code_field = (By.ID, 'code')
    confirm_code_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')
    payment_method_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[2]')
    credit_card_button = (By.XPATH, '//div[@class="pp-selector"]//div[@class="pp-row disabled"]')
    card_number = (By.ID, 'number')
    card_code = (By.XPATH, '/html/body/div/div/div[2]/div[2]/div[2]/form/div[1]/div[2]/div[2]/div[2]/input')
    card_button_submit = (By.XPATH, '/html/body/div/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    credit_card_close = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    comments_order = (By.XPATH, '//*[@id="comment"]')
    checkbox_deliver = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div')
    ice_cream_counter = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    ask_taxi_service = (By.CLASS_NAME, 'smart-button')
    order_time = (By.CLASS_NAME, 'order-header-time')
    order_time_left = (By.XPATH, '//*[@id="root"]/div/div[5]/div[2]/div[1]/div/div[1]')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def wait_load(self, selector):
        WebDriverWait(self.driver, 3).until(expected_conditions.presence_of_element_located(selector))

    def taxi_click(self):
        self.driver.find_element(*self.ask_for_taxi_button).click()

    def tariff_click(self):
        self.driver.find_element(*self.comfort_tariff).click()

    def phone_click(self):
        self.driver.find_element(*self.phone_button).click()

    def fill_phone_number(self, phone_number):
        self.driver.find_element(*self.phone_field).send_keys(phone_number)

    def fill_code(self, code):
        self.driver.find_element(*self.code_field).send_keys(code)
        self.driver.find_element(*self.confirm_code_button).click()

    def get_phone_code(self):
        self.driver.find_element(*self.send_code_button).click()

    def set_phone_number(self, number):
        self.phone_click()
        self.fill_phone_number(number)
        self.get_phone_code()

    def payment_method_click(self):
        self.driver.find_element(*self.payment_method_button).click()

    def credit_card_click(self):
        self.driver.find_element(*self.credit_card_button).click()

    def set_card_number(self, user_card_number):
        self.driver.find_element(*self.card_number).send_keys(user_card_number)

    def set_card_code(self, user_card_code):
        self.driver.find_element(*self.card_code).send_keys(user_card_code)

    def card_data_submit(self):
        self.driver.find_element(*self.card_button_submit).click()

    def close_credit_card(self):
        self.driver.find_element(*self.credit_card_close).click()

    def add_credit_card(self, user_card_number, user_card_code):
        self.payment_method_click()
        self.credit_card_click()
        self.set_card_number(user_card_number)
        self.set_card_code(user_card_code)
        self.card_data_submit()
        self.close_credit_card()

    def add_comment(self, comment):
        self.driver.find_element(*self.comments_order).send_keys(comment)

    def checkbox_deliver_click(self):
        self.driver.find_element(*self.checkbox_deliver).click()

    def ice_cream_counter_click(self, counter):
        for i in range(counter):
            self.driver.find_element(*self.ice_cream_counter).click()

    def ask_taxi_click(self):
        self.driver.find_element(*self.ask_taxi_service).click()

    def scroll_page(self, selector):
        element = self.driver.find_element(*selector)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def wait_driver(self):
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div[5]/div[2]/div[2]/div[1]/div[1]/div[1]/img')))

    def get_order_time_left(self):
        return self.driver.find_element(*self.order_time_left).text

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        options.add_argument('--headless')
        cls.driver = webdriver.Chrome(options=options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_load((By.XPATH, '//div[@class="logo"]'))
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_tariff(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_load((By.XPATH, '//div[@class="logo"]'))
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.wait_load((By.XPATH, '//div[@class="results-text"]//button[@class="button round"]'))
        routes_page.taxi_click()
        routes_page.wait_load((By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]'))
        routes_page.tariff_click()

    def test_fill_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_load((By.XPATH, '//div[@class="logo"]'))
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.wait_load((By.XPATH, '//div[@class="results-text"]//button[@class="button round"]'))
        routes_page.taxi_click()
        routes_page.wait_load((By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]'))
        routes_page.tariff_click()
        routes_page.scroll_page((By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[1]/div'))
        routes_page.set_phone_number(data.phone_number)
        phone_code = retrieve_phone_code(self.driver)
        routes_page.fill_code(phone_code)

    def test_card_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_load((By.XPATH, '//div[@class="logo"]'))
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.wait_load((By.XPATH, '//div[@class="results-text"]//button[@class="button round"]'))
        routes_page.taxi_click()
        routes_page.wait_load((By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]'))
        routes_page.tariff_click()
        routes_page.scroll_page((By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[2]'))
        routes_page.add_credit_card(data.card_number, data.card_code)

    def test_taxi_service(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_load((By.XPATH, '//div[@class="logo"]'))
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.wait_load((By.XPATH, '//div[@class="results-text"]//button[@class="button round"]'))
        routes_page.taxi_click()
        routes_page.wait_load((By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]'))
        routes_page.tariff_click()
        routes_page.scroll_page((By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[1]/div'))
        routes_page.set_phone_number(data.phone_number)
        phone_code = retrieve_phone_code(self.driver)
        routes_page.fill_code(phone_code)
        routes_page.scroll_page((By.XPATH, '/html/body/div/div/div[3]/div[3]/div[2]/div[2]/div[2]'))
        routes_page.add_credit_card(data.card_number, data.card_code)
        routes_page.scroll_page((By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[3]/div'))
        routes_page.add_comment('Hola, guapo')
        routes_page.scroll_page((By.XPATH, '/html/body/div/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span'))
        routes_page.checkbox_deliver_click()
        routes_page.scroll_page((By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]'))
        routes_page.ice_cream_counter_click(2)
        routes_page.ask_taxi_click()
        routes_page.wait_driver()
        assert "El conductor llegará en" in routes_page.get_order_time_left()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
