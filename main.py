import undetected_chromedriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from faker import Faker
import time, re, requests, string, random

driver = webdriver.Chrome()

driver.get("https://www.facebook.com/")
id = re.findall(r'role="button" class="(.*?)" href="#" ajaxify="(.*?)" id="(.*?)" data-testid="open-registration-form-button"', driver.page_source)[0][2]
WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.ID, id))).click()
full_name = Faker().name().split(" ")
first_name = full_name[0].strip()
last_name = full_name[1].strip()
WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.NAME, "firstname"))).send_keys(first_name)
WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.NAME, "lastname"))).send_keys(last_name)
email = requests.post("https://api.internal.temp-mail.io/api/v3/email/new").json()["email"]
WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.NAME, "reg_email__"))).send_keys(email)
WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.NAME, "reg_email_confirmation__"))).send_keys(email)
password = "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(9))
WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.ID, "password_step_input"))).send_keys(password)
select = Select(WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.NAME, "birthday_day"))))
select.select_by_value(str(random.randrange(1, 28)))
select = Select(WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.NAME, "birthday_month"))))
select.select_by_value(str(random.randrange(1, 11)))
select = Select(WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.NAME, "birthday_year"))))
select.select_by_value(random.choice(["1995","1996","1997","1998","1999","2000","2001","2002"]))
WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.NAME, "sex"))).click()
WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.NAME, "websubmit"))).click()
time.sleep(35)
while True:
	messages = requests.get(f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages").json()
	if messages:
		print(messages[0]["subject"])
		break
	else:
		time.sleep(5)

input("[!] Enter To Exit: ")


print(email, password)

driver.close()