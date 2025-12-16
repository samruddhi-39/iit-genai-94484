from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(5)


driver.get("https://duckduckgo.com/")

search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("sunbeam internship")
search_box.send_keys(Keys.RETURN)
time.sleep(3)


driver.get("https://www.sunbeaminfo.in/internship")
print("Sunbeam Page Title:", driver.title)
time.sleep(3)


driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)


try:
    plus_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
    time.sleep(1)
    plus_button.click()
    time.sleep(3)
except Exception as e:
    print("Toggle button issue:", e)

print("\n__________ Internship Information __________\n")
para = driver.find_elements(By.CSS_SELECTOR, ".main_info.wow.fadeInUp")
for p in para:
    print(p.text)


print("\n______________ Internship Batches ______________")

table_rows = driver.find_elements(By.TAG_NAME, "tr")
batches = []

for row in table_rows:
    cols = row.find_elements(By.TAG_NAME, "td")

    if len(cols) < 8:
        continue

    info = {
        "sr": cols[0].text,
        "batch": cols[1].text,
        "batch_duration": cols[2].text,
        "start_date": cols[3].text,
        "end_date": cols[4].text,
        "time": cols[5].text,
        "fees": cols[6].text,
        "download": cols[7].text
    }

    batches.append(info)

print(json.dumps(batches, indent=4))


time.sleep(5)
driver.quit()
