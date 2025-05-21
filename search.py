import json
from datetime import datetime
import re

def normalize(text):
    return text.lower().replace("ī", "i").replace("ā", "a").replace("ē", "e").replace("ū", "u") \
        .replace("š", "s").replace("č", "c").replace("ž", "z").replace("ļ", "l").replace("ņ", "n")

def count(items):
    freq = {}
    for item in items:
        if item in freq:
            freq[item] += 1
        else:
            freq[item] = 1
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)

def show_statistics(vakances):
    print("\n Kopējā statistika:")
    print(f" Kopā atrasto prakšu: {len(vakances)}")

    #Pilsētas
    locations = [v['Location'] for v in vakances if v.get("Location") and v["Location"] != "Nav informācijas"]
    loc_count = count(locations)
    print(f"Locations: {len(loc_count)}")
    print("Top 3 locations:")
    for city, cnt in loc_count[:3]:
        print(f"     - {city}: {cnt}")

    # Uzņēmumi
    companies = [v['Company'] for v in vakances if v.get("Company")]
    comp_count = count(companies)
    print(f"Uzņēmumi: {len(comp_count)}")
    print("Top 3 uzņēmumi:")
    for company, cnt in comp_count[:3]:
        print(f"     - {company}: {cnt}")

    # Termiņi
    deadlines = []
    for v in vakances:
        match = re.search(r"\d{2}\.\d{2}\.\d{4}", v.get("Deadline", ""))
        if match:
            try:
                deadlines.append(datetime.strptime(match.group(), "%d.%m.%Y"))
            except:
                continue

    if deadlines:
        min_date = min(deadlines).strftime("%d.%m.%Y")
        max_date = max(deadlines).strftime("%d.%m.%Y")
        avg_time = sum(d.timestamp() for d in deadlines) / len(deadlines)
        avg_date = datetime.fromtimestamp(avg_time).strftime("%d.%m.%Y")
        print("Termiņi:")
        print(f"   Min: {min_date}")
        print(f"   Max: {max_date}")
        print(f"   Vidējais: {avg_date}")
    else:
        print("Termiņi: Nav pieejami")

def validate_date(input_str):
    try:
        return datetime.strptime(input_str, "%d-%m-%Y")
    except ValueError:
        print("\nNepareizs datuma formāts. Pareizais formāts: dd-mm-yyyy (piemēram: 15-01-2023)")
        return None

def run():
    with open("vakances.json", "r", encoding="utf-8") as f:
        vakances = json.load(f)

    interest = input("Ievadi meklējamo vārdu (piemēram: python): ").lower()
    place = input("Ievadi meklējamo vietu (piemēram: Rīga): ").lower()
    deadline_till = input("Ievadi meklējamo termiņu (piemēram: 15-01-2023): ")
    company_name = input("Ievadi meklējamo uzņēmumu (piemēram: Rīgas lidosta): ").lower()

    user_date = validate_date(deadline_till) if deadline_till else None

    results = []

    for vakance in vakances:
        title = normalize(vakance.get("Title", ""))  # Normalize title
        location = normalize(vakance.get("Location", ""))  # Normalize location
        deadline = vakance.get("Deadline", "").lower()
        company = normalize(vakance.get("Company", ""))  # Normalize company
        requirements = normalize(vakance.get("Requirements", ""))  # Normalize requirements

        if interest:
            normalized_interes = normalize(interest)
            if (normalized_interes not in title) and (normalized_interes not in requirements):
                continue

        if place:
            normalized_place = normalize(place)
            if normalized_place not in location:
                continue
        
        if company_name:
            normalized_company_name = normalize(company_name)
            if normalized_company_name not in company:
                continue

        if deadline_till:
            try:
                deadline_date = datetime.strptime(deadline.split("līdz")[-1].strip(), "%d.%m.%Y")
                if deadline_date > user_date:
                    continue
            except:
                pass

        results.append(vakance)

    print(f"\n Atrastas {len(results)} vakances:")
    for vakance in results:
        print(f"\n{vakance['Title']}")
        print(f"\nUzņēmums: {vakance['Company']}")
        print(f"Atrašanās vieta: {vakance['Location']}")
        print(f"Termiņš: {vakance['Deadline']}")
        print(f"\nPrasības: {vakance['Requirements']}")
        print(f"\nSaite: {vakance['Link']}")

    show_stats = input("\nVai vēlies apskatīt prakse.lv kopējo statistiku? (yes/no): ").strip().lower()
    if show_stats == "yes":
        show_statistics(vakances)

if __name__ == "__main__":
    run()