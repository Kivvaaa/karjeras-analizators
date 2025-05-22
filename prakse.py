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

    try:
        url = "https://www.prakse.lv/vacancy/list"
        driver.get(url)

        # Select "Internships" filter
        driver.find_element(By.CSS_SELECTOR, 'label[for="filter_type_1"]').click()
        time.sleep(2)

        # Click "Load more" multiple times
        for i in range(15):
            try:
                wait = WebDriverWait(driver, 5)
                find = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".load-more-link")))
                driver.execute_script("arguments[0].scrollIntoView(true);", find)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", find)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "item")))
            except:
                print("No more job cards to load")
                break

        # Get the HTML and close browser
        time.sleep(3)
        html = driver.page_source

    finally:
        driver.quit()

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("section", class_="item")

    all_vacancies = []

    for index, card in enumerate(cards):
        try:
            # Extract title
            title = card.find("h2").string
            if re.search(r"\d{3,}", title) or title.endswith("?"):
                continue  # Skip junk titles

            # Extract company
            company = card.find(class_="item-middle-subtitle").string

            # Parse metadata info block
            li_elements = card.find_all("li")
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

            # Extract link to full vacancy
            link_tag = card.find("a")
            link = "https://www.prakse.lv" + link_tag["href"]

            # Go into each vacancy and extract requirements
            if link:
                try:
                    page = requests.get(link)
                    if page.status_code == 200:
                        detail = BeautifulSoup(page.content, "html.parser")
                        req_block = detail.find("h4", string="Nepieciešams")
                        if req_block:
                            next_div = req_block.find_next_sibling("div")
                            if next_div:
                                requirements = next_div.get_text(strip=True)
                except Exception as e:
                    print("Error loading detail:", e)

            all_vacancies.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Deadline": deadline,
                "Link": link,
                "Requirements": requirements
            })

            print(f"\r{index + 1} / {len(cards)}", end="")

        except Exception as e:
            print("Error parsing card:", e)

    # Save all parsed data into JSON file
    with open("vakances.json", "w", encoding="utf-8") as f:
        json.dump(all_vacancies, f, ensure_ascii=False, indent=4)

    print(f"\nSaved {len(all_vacancies)} internship ads → vakances.json")

if __name__ == "__main__":
    run()
