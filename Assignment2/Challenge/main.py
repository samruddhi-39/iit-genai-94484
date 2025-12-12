import sys
from math_util import (
    area_rectangle,
    area_circle,
    area_triangle,
)
from jsonplaceholder import fetch_json_data
from weatherapp import get_current_weather, pretty_print_weather


def menu():
    print("\n=== MAIN MENU ===")
    print("1. Area Calculations (math_utils)")
    print("2. Fetch JSONPlaceholder Posts")
    print("3. Weather App (Enter city and get forecast)")
    print("4. Exit")
    print("====================")


def area_menu():
    print("\n--- AREA CALCULATIONS ---")
    print("1. Area of Rectangle")
    print("2. Area of Circle")
    print("3. Area of Triangle")
    print("4. Back to Menu")


def area_driver():
    while True:
        area_menu()
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                w = float(input("Width: "))
                h = float(input("Height: "))
                print("Area =", area_rectangle(w, h))

            elif choice == "2":
                r = float(input("Radius: "))
                print("Area =", area_circle(r))

            elif choice == "3":
                b = float(input("Base: "))
                h = float(input("Height: "))
                print("Area =", area_triangle(b, h))

            elif choice == "4":
                return  # Back to main menu

            else:
                print("Invalid choice!")

        except Exception as e:
            print("Error:", e)


def fetch_data_driver():
    print("\nFetching posts from JSONPlaceholder...")
    try:
        fetch_json_data()
    except Exception as e:
        print("Error fetching posts:", e)


def weather_driver():
    print("\n--- WEATHER APP ---")
    city = input("Enter city name: ").strip()

    try:
        data = get_current_weather(city)
        pretty_print_weather(data)
    except Exception as e:
        print("Error:", e)


def main():
    while True:
        menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            area_driver()

        elif choice == "2":
            fetch_data_driver()

        elif choice == "3":
            weather_driver()

        elif choice == "4":
            print("Exiting program...")
            sys.exit()

        else:
            print("Invalid choice, try again!")


if __name__ == "__main__":
    main()
