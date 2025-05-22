from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time, re

def run():
    atslegvards = input("Ievadi vienu vai vairākus atslēgvārdus (atdalītus ar atstarpēm, piemēram: Python SQL): ")

    service = Service()
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=option)

    try:
        driver.get("https://www.cv.lv")
        time.sleep(2)

        # Accept cookies if the popup appears
        try:
            driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        except:
            pass

        # Select job category: Informācijas tehnoloģijas
        try:
            kategorija_placeholder = driver.find_element(By.XPATH, "//div[contains(text(), 'Izvēlēties kategoriju')]")
            wrapper = kategorija_placeholder.find_element(By.XPATH, "./ancestor::div[contains(@class, 'react-select__control')]")
            wrapper.click()
            opcija = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'react-select__option') and contains(text(), 'Informācijas tehnoloģijas')]"))
            )
            opcija.click()
            print("Kategorija izvēlēta: Informācijas tehnoloģijas")
        except Exception as e:
            print("Neizdevās izvēlēties kategoriju:", str(e))

        # Enter the keyword into the input field and confirm
        try:
            placeholder = driver.find_element(By.XPATH, "//div[contains(text(), 'Pievienot atslēgvārdu')]")
            input_wrapper = placeholder.find_element(By.XPATH, "./ancestor::div[contains(@class, 'react-select__value-container')]")
            input_field = input_wrapper.find_element(By.TAG_NAME, "input")
            input_field.send_keys(atslegvards)
            time.sleep(0.5)
            input_field.send_keys(Keys.ENTER)
            print(f"Atslēgvārds '{atslegvards}' pievienots")
        except Exception as e:
            print("Neizdevās pievienot atslēgvārdu:", str(e))

        # Click on the "Rādīt" button
        try:
            poga = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Rādīt')]]"))
            )
            poga.click()
            print("Meklēšana sākta...\n")
        except:
            print("Neizdevās nospiest 'Rādīt' pogu.")
            return

        salary_list = []
        page = 1

        while True:
            time.sleep(2)

            # Find all salary labels on the current page
            salaries = driver.find_elements(By.CLASS_NAME, "salary-label")
            for s in salaries:
                text = s.text.strip().replace("€", "").replace(" ", "")
                nums = re.findall(r'\d+', text)

                # Calculate average salary from range or single value
                if len(nums) >= 2:
                    avg = (int(nums[0]) + int(nums[1])) / 2
                elif len(nums) == 1:
                    avg = int(nums[0])
                else:
                    continue

                # Skip low salaries (likely hourly)
                if avg < 100:
                    print(f"!!! Zema alga (iespējams stundas likme): €{avg} — izlaižam")
                    continue
                salary_list.append(avg)

            # Try to navigate to the next page if available
            try:
                next_btn = driver.find_element(By.XPATH, "//button[@aria-label='Next']")
                if "disabled" in next_btn.get_attribute("class") or not next_btn.is_enabled():
                    break
                driver.execute_script("arguments[0].click();", next_btn)
                page += 1
            except:
                break

        print(f"\nAtslēgvārds: {atslegvards}")
        print(f"Vakances ar pietiekamu algu: {len(salary_list)}")
        if salary_list:
            print(f"Vidējā alga: €{round(sum(salary_list) / len(salary_list))}")
            print(f"Min: €{min(salary_list)}   Max: €{max(salary_list)}")
        else:
            print("Neatradu nevienu derīgu algu.")

    finally:
        # Ensure the browser is closed even if an error occurs
        driver.quit()
        
if __name__ == "__main__":
    run()
