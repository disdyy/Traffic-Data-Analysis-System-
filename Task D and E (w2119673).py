#Author : Disadhi Ranasinghe
#Date : 2024.12.01
#student ID : 20240002 / w2119673

# Task D and E
import tkinter as tk
import csv

# Constants for the canvas and bars
CANVAS_WIDTH = 950 # width of canvas for histogram
CANVAS_HEIGHT = 400 # Height of the canvas for the histogram
BAR_WIDTH = 12 # Width of each bar in histogram
PADDING = 60 # Padding around the canvas
LEGEND_BOX = 20 # Size of the legend box

class HistogramApp:
    def __init__(self, histogram_data, date):
        self.histogram_data = histogram_data #Data for the histogram
        self.date = date # Date of the data
        self.root = tk.Tk() #Creating the main tkinter window
        self.root.title("Histogram") # Set the window title
        self.canvas = tk.Canvas(self.root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white") # create the canvas
        self.canvas.pack() # Add canvas to the winndow

    def setup_window(self):
        # Draw the X-axis line
        self.canvas.create_line(PADDING, CANVAS_HEIGHT - PADDING, 850, CANVAS_HEIGHT - PADDING, width=2)

        # Draw X-axis line
        self.canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT - PADDING // 2, 
                                text="Hours 00:00 to 24:00", font=["Arial", 8], fill="black")
        # Add title to the histogram
        self.canvas.create_text(PADDING, 20, 
                                text=f"Histogram of Vehicle Frequency per Hour ({self.date})", 
                                font=["Arial", 14, "bold"], fill="black", anchor="w")

    def draw_histogram(self):
        # combine data to find maxium value for scaling
        max_value = max(self.histogram_data["Elm Avenue/Rabbit Road"] + 
                        self.histogram_data["Hanley Highway/Westway"], default=1)
        scale = (CANVAS_HEIGHT - 2 * PADDING) / max_value
        
        for hour in range(24):
            # Draw green bar for Elm Avenue/Rabbit Road
            x_green = PADDING + hour * (BAR_WIDTH * 2 + 10)
            y_green = CANVAS_HEIGHT - PADDING - self.histogram_data["Elm Avenue/Rabbit Road"][hour] * scale
            self.draw_bar(x_green, y_green, BAR_WIDTH, "lightgreen", "green", 
                          self.histogram_data["Elm Avenue/Rabbit Road"][hour])
            
            # Draw red bar for Hanley Highway/Westway
            x_red = x_green + BAR_WIDTH
            y_red = CANVAS_HEIGHT - PADDING - self.histogram_data["Hanley Highway/Westway"][hour] * scale
            self.draw_bar(x_red, y_red, BAR_WIDTH, "lightcoral", "red", 
                          self.histogram_data["Hanley Highway/Westway"][hour])
            
            #Adding labels for X-axis
            self.canvas.create_text(x_green + BAR_WIDTH, CANVAS_HEIGHT - PADDING + 15, 
                                    text=f'{hour:02}', font=["Arial", 10], fill="black")

    def draw_bar(self, x, y, width, fill_color, outline_color, value):
        # Draw a single histogram bar
        self.canvas.create_rectangle(x, y, x + width, CANVAS_HEIGHT - PADDING,
                                     fill=fill_color, outline=outline_color)
        # Add value lebel above the bar
        self.canvas.create_text(x + width / 2, y - 10, text=str(value), font=["Arial", 8], fill=outline_color)

    def draw_legend(self):
        # Draw the legend explaining the color of each bar
        self.draw_legend_item(PADDING, 30, "lightgreen", "Elm Avenue/Rabbit Road")
        self.draw_legend_item(PADDING, 55, "lightcoral", "Hanley Highway/Westway")

    def draw_legend_item(self, x, y, color, text):
        # Draw a single item in the legend
        self.canvas.create_rectangle(x, y, x + LEGEND_BOX, y + LEGEND_BOX, fill=color, outline="white")
        self.canvas.create_text(x + LEGEND_BOX + 10, y + LEGEND_BOX // 2, text=text, anchor="w", font=["Arial", 10], fill="black")

    def run(self):
        # Setup and run the Tkinter window to display the histogram
        self.setup_window()
        self.draw_histogram()
        self.draw_legend()
        self.root.mainloop()

# Class to process multiple CSV files and generate histograms
class MultiCSVProcessor:
    def __init__(self):
        # Infinite loop to allow user to process multiple datasets
        while True:
            # Get a valid date from the user
            selected_date = self.get_valid_date()
            file_path = f"traffic_data{selected_date}.csv" # File path based on entered date
            formatted_date = self.format_date(selected_date) # Format the date for display
            histogram_data = {
                "Elm Avenue/Rabbit Road": [0] * 24,
                "Hanley Highway/Westway": [0] * 24
            }

            try:
                # Attempt to load the CSV file and create histogram
                self.load_csv_file(file_path, histogram_data)
                app = HistogramApp(histogram_data, formatted_date)
                app.run() # Run the app to display histogram
            except FileNotFoundError:
                print(f"File {file_path} not found. Please check the date and try again.") # Handle missing file
            # Ask if user needs to load another dataset
            if self.ask_to_continue() == "N":
                print("Exiting the program.")
                break

    def load_csv_file(self, file_path, histogram_data):
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                time_of_day = row.get("timeOfDay", "")
                try:
                    hour = int(time_of_day.split(':')[0])
                except (ValueError, IndexError):
                    continue
                junction_name = row.get("JunctionName", "")
                if junction_name in histogram_data:
                    histogram_data[junction_name][hour] += 1

   
    def get_valid_date(self):
        # Get a valid date from the user
        while True:
            try:
                day = int(input("Please enter the day of the survey in the format DD: "))
                if 1 <= day <= 31:
                    break
                print("Invalid day - which is out of range (1-31)")
            except ValueError:
                print("Invalid input - please enter integers only. Error:")
        while True:
            try:
                month = int(input("Please enter the month of the survey in the format MM: "))
                if 1 <= month <= 12:
                    break
                print("Invalid month - which is out of range (1-12)")
            except ValueError:
                print("Invalid input. Please enter a valid month.")
        while True:
            try:
                year = int(input("Please enter the year of the survey in the format YYYY: "))
                if 2000 <= year <= 2024:
                    break
                print("Invalid year - which is out of range (2000-2024)")
            except ValueError:
                print("Invalid input. Please enter a valid year.")
        return f"{day:02}{month:02}{year}"

    def format_date(self, date):
        return f"{date[:2]}-{date[2:4]}-{date[4:]}"

    def ask_to_continue(self):
        while True:
            user_input = input("Do you want to process another dataset (Y/N)? ").strip().upper()
            if user_input in ["Y", "N"]:
                return user_input
            print("Invalid input. Please enter 'Y' or 'N'.")
            
# Run the program
MultiCSVProcessor() # Start processing CSV file
