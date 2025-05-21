from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time, re

def run():
    # --------- INPUT SKILL ---------
    atslegvards = input("Ievadi atslēgvārdu (piemēram: Python): ")

    # --------- SETUP CHROME DRIVER ---------
    service = Service()
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=option)

    # --------- STEP 1: OPEN CV.LV ---------
    driver.get("https://www.cv.lv")
    time.sleep(2)

    # --------- STEP 2: ACCEPT COOKIES ---------
    try:
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    except:
        pass

    # --------- SELECT CATEGORY: Informācijas tehnoloģijas ---------
    try:
        kategorija_placeholder = driver.find_element(By.XPATH, "//div[contains(text(), 'Izvēlēties kategoriju')]")
        wrapper = kategorija_placeholder.find_element(By.XPATH, "./ancestor::div[contains(@class, 'react-select__control')]")
        wrapper.click()
        opcija = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'react-select__option') and contains(text(), 'Informācijas tehnoloģijas')]"))
        )
        opcija.click()
        print("✅ Kategorija izvēlēta: Informācijas tehnoloģijas")
    except Exception as e:
        print("⚠️ Neizdevās izvēlēties kategoriju:", str(e))

    # --------- STEP 3: ENTER ATSLĒGVĀRDS VIA PLACEHOLDER ---------
    try:
        placeholder = driver.find_element(By.XPATH, "//div[contains(text(), 'Pievienot atslēgvārdu')]")
        input_wrapper = placeholder.find_element(By.XPATH, "./ancestor::div[contains(@class, 'react-select__value-container')]")
        input_field = input_wrapper.find_element(By.TAG_NAME, "input")

        input_field.send_keys(atslegvards)
        time.sleep(0.5)
        input_field.send_keys(Keys.ENTER)

        print(f"✅ Atslēgvārds '{atslegvards}' pievienots")
    except Exception as e:
        print("❌ Neizdevās pievienot atslēgvārdu:", str(e))

    # --------- STEP 4: CLICK "Rādīt rezultātus" ---------
    try:
        poga = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Rādīt')]]"))
        )
        poga.click()
        print("🔍 Meklēšana sākta...\n")
    except:
        print("❌ Neizdevās nospiest 'Rādīt' pogu.")
        driver.quit()
        exit()

    # --------- STEP 5: PARSE SALARIES FROM ALL PAGES ---------
    salary_list = []
    page = 1

    while True:
        time.sleep(2)

        salaries = driver.find_elements(By.CLASS_NAME, "salary-label")
        for s in salaries:
            text = s.text.strip().replace("€", "").replace(" ", "")
            nums = re.findall(r'\d+', text)
            if len(nums) >= 2:
                avg = (int(nums[0]) + int(nums[1])) / 2
            elif len(nums) == 1:
                avg = int(nums[0])
            else:
                continue

            if avg < 100:
                print(f"   ⚠️ Zema alga (iespējams stundas likme): €{avg} — izlaižam")
                continue

            salary_list.append(avg)

        # Следующая страница
        try:
            next_btn = driver.find_element(By.XPATH, "//button[@aria-label='Next']")
            if "disabled" in next_btn.get_attribute("class") or not next_btn.is_enabled():
                break
            driver.execute_script("arguments[0].click();", next_btn)
            page += 1
        except:
            break

    # --------- STEP 6: STATS ---------
    print(f"\n📊 Atslēgvārds: {atslegvards}")
    print(f"🔢 Vakances ar pietiekamu algu: {len(salary_list)}")
    if salary_list:
        print(f"💰 Vidējā alga: €{round(sum(salary_list) / len(salary_list))}")
        print(f"🔽 Min: €{min(salary_list)}   🔼 Max: €{max(salary_list)}")
    else:
        print("❗ Neatradu nevienu derīgu algu.")

    driver.quit()

if __name__ == "__main__":
    run()