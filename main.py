import prakse
import search
import salary

def show_menu():
    print("\nIzvēlies darbību:")
    print("1 - Lejupielādēt jaunas vakances (parsing 5–6 minūtes)")
    print("2 - Meklēt un filtrēt vakances (prakse.lv)")
    print("3 - Analizēt algu informāciju (cv.lv)")
    print("0 - Iziet")

def main():
    actions = {
        "1": prakse.run,
        "2": search.run,
        "3": salary.run,
    }

    while True:
        show_menu()
        choice = input("Ievadi savu izvēli: ").strip()

        if choice == "0":
            print("Programma pārtraukta.")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Nederīga izvēle. Mēģini vēlreiz.")

if __name__ == "__main__":
    main()
