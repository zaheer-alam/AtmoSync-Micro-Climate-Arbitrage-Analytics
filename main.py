from database import create_database, get_saved_climate_data
from data.weather_api import get_weather
from app.analytics import get_average_temperature


def main():
    print("==============================")
    print("        Welcome to AtmoSync")
    print("==============================")
    print("Micro-Climate Arbitrage Analytics")
    print()

    create_database()

    while True:
        print()
        print("========== MENU ==========")
        print("1. Get Weather")
        print("2. View Saved Climate Data")
        print("3. Calculate Average Temperature")
        print("4. Exit")
        print("==========================")

        choice = input("Enter your choice: ")

        if choice == "1":
            city = input("Enter city name: ")

            if city.strip():
                get_weather(city)
            else:
                print("Please enter a city name.")

        elif choice == "2":
            records = get_saved_climate_data()

            if not records:
                print("No climate data found.")
            else:
                print()
                print("===== Saved Climate Data =====")

                for record in records:
                    print(record)

        elif choice == "3":
            average_temperature = get_average_temperature()

            print()
            print("Average Temperature:", average_temperature, "°C")

        elif choice == "4":
            print()
            print("Thank you for using AtmoSync!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()


