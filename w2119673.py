#Author : Disadhi Ranasinghe
#Date : 2024.12.01
#student ID : 20240002 / w2119673

#Task A : Input Validation
import csv

# Function to validate the date input
def validate_date_part(date_part):
    input_string = "Input date part: "

    if date_part not in {"d", "m", "y"}:
        raise Exception("Invalid date part input. Allowed values are 'd', 'm' or 'y'.")

    if date_part == "d":
        input_string = "Please enter the day of the survey in the format DD: "
    if date_part == "m":
        input_string = "Please enter the month of the survey in the format MM: "
    if date_part == "y":
        input_string = "Please enter the year of the survey in the format YYYY: "

    while True:
        try:
            input_value = int(input(input_string))
            if date_part == "d" and not (1 <= input_value <= 31):
                print(f"Invalid day - you entered {input_value}, which is out of range (1-31).")
                continue

            if date_part == "m" and not (1 <= input_value <= 12):
                print(f"Invalid month - you entered {input_value}, which is out of range (1-12).")
                continue

            if date_part == "y" and not (2000 <= input_value <= 2024):
                print(f"Invalid year - you entered {input_value}, which is out of range (2000-2024).")
                continue

            return f"{input_value:02}"  # Format to ensure two digits
        except ValueError as e:
            print(f"Invalid input - please enter integers only. Error: {e}")

def validate_date_input():
    day = validate_date_part("d")
    month = validate_date_part("m")
    year = validate_date_part("y")

    return f"{day}{month}{year}"

#Task B : Outcome

# Function to process CSV data
def process_csv_data(file_name):
    try:
        with open(file_name, 'r') as file:
            csv_reader = csv.DictReader(file)

            # Initialize variables for calculations
            data = {
                "total_vehicles": 0,
                "total_trucks": 0,
                "total_electric": 0,
                "total_two_wheeled": 0,
                "total_buses_elm": 0,
                "total_both_junctions": 0,
                "total_speeding": 0,
                "total_elm_only": 0,
                "total_hanley_only": 0,
                "scooters_percentage_elm": 0,
                "peak_hour": (0, 0),  # (hour, vehicle_count)
                "rain_hours": set(),
                "vehicles_per_hour": [0] * 24,
            }

            for row in csv_reader:
                vehicle_type = row['VehicleType'].lower()
                junction = row['JunctionName'].lower()
                hour = int(row['timeOfDay'].split(':')[0])
                speed = int(row['VehicleSpeed'])
                speed_limit = int(row['JunctionSpeedLimit'])
                is_raining = 'rain' in row['Weather_Conditions'].lower()
                is_electric = row['elctricHybrid'].lower() == 'true'

                # Update counts
                data["total_vehicles"] += 1
                data["total_trucks"] += "truck" in vehicle_type
                data["total_electric"] += is_electric
                data["total_two_wheeled"] += "bike" in vehicle_type or "motorbike" in vehicle_type or "scooter" in vehicle_type
                data["total_speeding"] += speed > speed_limit
                data["vehicles_per_hour"][hour] += 1
                if is_raining:
                    data["rain_hours"].add(hour)
                if "bus" in vehicle_type and "elm avenue" in junction:
                    data["total_buses_elm"] += 1
                if "elm avenue" in junction and "hanley highway" in junction:
                    data["total_both_junctions"] += 1
                elif "elm avenue" in junction:
                    data["total_elm_only"] += 1
                elif "hanley highway" in junction:
                    data["total_hanley_only"] += 1
                if "scooter" in vehicle_type and "elm avenue" in junction:
                    data["scooters_percentage_elm"] += 1

            # Calculate derived statistics
            total_hours = sum(1 for count in data["vehicles_per_hour"] if count > 0)
            peak_hour_count = max(data["vehicles_per_hour"])
            peak_hour = data["vehicles_per_hour"].index(peak_hour_count)
            truck_percentage = round((data["total_trucks"] / data["total_vehicles"]) * 100, 2) if data["total_vehicles"] > 0 else 0
            avg_bicycles_per_hour = round(data["total_two_wheeled"] / total_hours, 2) if total_hours > 0 else 0
            scooter_percentage_elm = round((data["scooters_percentage_elm"] / data["total_elm_only"]) * 100, 2) if data["total_elm_only"] > 0 else 0

            # Prepare the results for saving
            results = (
                f"Data file: {file_name}\n"
                f"Total Vehicles: {data['total_vehicles']}\n"
                f"Total Trucks: {data['total_trucks']}\n"
                f"Total Electric Vehicles: {data['total_electric']}\n"
                f"Total Two-Wheeled Vehicles: {data['total_two_wheeled']}\n"
                f"Percentage of Trucks: {truck_percentage}%\n"
                f"Average Bicycles per Hour: {avg_bicycles_per_hour}\n"
                f"Total Vehicles through Elm Avenue/Rabbit Road: {data['total_elm_only']}\n"
                f"Percentage of Scooters through Elm Avenue/Rabbit Road: {scooter_percentage_elm}%\n"
                f"Peak Hour: {peak_hour}:00 with {peak_hour_count} vehicles\n"
                f"Total Rain Hours: {len(data['rain_hours'])}\n"
            )

            return results

    except FileNotFoundError:
        print(f"File not found: {file_name}")
        return None
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

#Task C : Save results as a text file
    
# Function to save results to a text file
def save_results_to_file(results):
    try:
        with open("results.txt", "a") as file:
            file.write(results + "\n")
        print("Results saved to 'results.txt'")
    except Exception as e:
        print(f"Error saving results to file: {e}")

# Main function
def main():
    while True:
        selected_date = validate_date_input()
        file_name = f"traffic_data{selected_date}.csv"  # Construct the file name

        print(f"Processing file: {file_name}")
        results = process_csv_data(file_name)
        if results:
            print(results)
            save_results_to_file(results)

        # Ask if the user wants to process another file
        continue_prompt = input("Do you want to process another date? (y/n): ").strip().lower()
        if continue_prompt != 'y':
            print("Exiting program.")
            break

# Run the program
if __name__ == "__main__":
    main()
