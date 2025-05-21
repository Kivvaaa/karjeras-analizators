from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, requests, re, json

def run():
    
    service = Service()
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=option)

    url = "https://www.prakse.lv/vacancy/list"
    driver.get(url)

    # click the button and scrolling
    vakances_button = driver.find_element(By.CSS_SELECTOR, 'label[for="filter_type_1"]').click()
    time.sleep(2)
    for i in range(15):
        try:
            wait = WebDriverWait(driver, 5)
            find = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".load-more-link")))

            driver.execute_script("arguments[0].scrollIntoView(true);", find)
            time.sleep(0.5)

            driver.execute_script("arguments[0].click();", find)

            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "item")))
        except:
            print("Nav vairāk sludinājumu")
            break

    time.sleep(3)
    html = driver.page_source
    driver.quit()

    lapas_saturs = BeautifulSoup(html, "html.parser")
    cards = lapas_saturs.find_all("section", class_="item")

    all_vakances = []

    for index, vakance in enumerate(cards):
        try:

            title = vakance.find("h2").string
            if re.search(r"\d{3,}", title) or title.endswith("?"):
                continue

            company = vakance.find(class_="item-middle-subtitle").string

            li_elements = vakance.find_all("li")
            info = ""
            for li in li_elements:
                text = li.get_text(strip=True)
                if "līdz" in text or "•" in text:
                    info = text
                    break

            location = "Nav informācijas"
            deadline = "Nav informācijas"
            requirements = "Nav informācijas"

            parts = [part.strip() for part in info.split("•") if part.strip()]
            
            for part in reversed(parts):
                if "līdz" in part:
                    deadline = part
                    break
            
            for part in parts:
                if "," in part:
                    location = part.strip()
                    break
            
            if location == "Nav informācijas" and len(parts) > 0:
                last_part = parts[-1].strip()
                if "līdz" not in last_part:
                    location = last_part

            vakances_link = vakance.find("a")
            link = "https://www.prakse.lv" + vakances_link["href"]

            if link:
                try:
                    page = requests.get(link)
                    if page.status_code == 200:
                        soup = BeautifulSoup(page.content, "html.parser")

                        requirements = soup.find("h4", string="Nepieciešams")
                        if requirements:
                            next_div = requirements.find_next_sibling("div")
                            if next_div:
                                requirements = next_div.get_text(strip=True)
                            else:
                                requirements = "Nav informācijas"
                        else:
                            requirements = "Nav informācijas"
                except Exception as e:
                    print("Error", e)

            all_vakances.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Deadline": deadline,
                "Link": link,
                "Requirements": requirements
            })

            print(f"\r{index + 1} / {len(cards)}", end="")

        except Exception as e:
            print("Error", e)

    with open("vakances.json", "w", encoding="utf-8") as f:
        json.dump(all_vakances, f, ensure_ascii=False, indent=4)

    print(f"\n Saglabātas {len(all_vakances)} prakses vietas → vakances.json")

if __name__ == "__main__":
    run()