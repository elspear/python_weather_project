import csv
from datetime import datetime

DEGREE_SYMBOL = u"\N{DEGREE SIGN}C"


def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees
        and Celcius symbols.

    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and "degrees Celsius."
    """
    return f"{temp}{DEGREE_SYMBOL}"


def convert_date(iso_string):
    """Converts an ISO formatted date into a human-readable format.

    Args:
        iso_string: An ISO date string.
    Returns:
        A date formatted like: Weekday Date Month Year e.g. Tuesday 06 July 2021
    """
    date_object = datetime.fromisoformat(iso_string)
    readable_date = date_object.strftime("%A %d %B %Y")

    return readable_date


def convert_f_to_c(temp_in_fahrenheit):
    """Converts a temperature from Fahrenheit to Celcius.

    Args:
        temp_in_fahrenheit: float representing a temperature.
    Returns:
        A float representing a temperature in degrees Celcius, rounded to 1 decimal place.
    """
    temp_in_fahrenheit = float(temp_in_fahrenheit)
    return round((temp_in_fahrenheit - 32) * 5 / 9, 1)


def calculate_mean(weather_data):
    """Calculates the mean value from a list of numbers.

    Args:
        weather_data: a list of numbers.
    Returns:
        A float representing the mean value.
    """
    numeric_data = [float(value) for value in weather_data]
    return sum(numeric_data) / len(numeric_data)


def load_data_from_csv(csv_file):
    """Reads a csv file and stores the data in a list.

    Args:
        csv_file: Path to the CSV file containing weather data
    Returns:
        A list of lists where each inner list contains [date, min_temp, max_temp]
    """
    data = []

    try:
        with open(csv_file, "r") as file:
            reading = csv.reader(file)
            next(reading)  # skips header row

            for row in reading:
                if row:

                    processed_row = [
                        row[0],  # date
                        int(row[1]),  # min temp
                        int(row[2])   # max temp
                    ]
                    data.append(processed_row)

        return data

    except FileNotFoundError:
        return []  # will return an empty list if file not found


def find_min(weather_data):
    """Calculates the minimum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The minimum value and it's position in the list. (In case of multiple matches, return the index of the *last* example in the list.)
    """
    if not weather_data:
        return ()

    weather_data = [float(value)
                    for value in weather_data]  # makes all values float
    min_value = weather_data[0]
    min_index = 0

    for index, value in enumerate(weather_data[1:], start=1):
        if value <= min_value:
            min_value = value
            min_index = index

    return (min_value, min_index)


def find_max(weather_data):
    """Calculates the maximum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The maximum value and it's position in the list. (In case of multiple matches, return the index of the *last* example in the list.)
    """
    if not weather_data:
        return ()

    weather_data = [float(value) for value in weather_data]
    max_value = weather_data[0]
    max_index = 0

    for index, value in enumerate(weather_data[1:], start=1):
        if value >= max_value:
            max_value = value
            max_index = index

    return (max_value, max_index)


def generate_summary(weather_data):
    """Outputs a summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """

    num_days = len(weather_data)
    min_temps = [row[1] for row in weather_data]
    max_temps = [row[2] for row in weather_data]

    min_temp, min_index = find_min(min_temps)
    min_date = weather_data[min_index][0]

    max_temp, max_index = find_max(max_temps)
    max_date = weather_data[max_index][0]

    avg_min = calculate_mean(min_temps)
    avg_max = calculate_mean(max_temps)

    min_temp_c = convert_f_to_c(min_temp)
    max_temp_c = convert_f_to_c(max_temp)
    avg_min_c = convert_f_to_c(avg_min)
    avg_max_c = convert_f_to_c(avg_max)

    return (
        f"{num_days} Day Overview\n"
        f"  The lowest temperature will be {format_temperature(min_temp_c)}, and will occur on {convert_date(min_date)}.\n"
        f"  The highest temperature will be {format_temperature(max_temp_c)}, and will occur on {convert_date(max_date)}.\n"
        f"  The average low this week is {format_temperature(avg_min_c)}.\n"
        f"  The average high this week is {format_temperature(avg_max_c)}.\n"
    )


def generate_daily_summary(weather_data):
    """Outputs a daily summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
    daily_summary = ""

    for day in weather_data:
        date = day[0]
        min_temp = convert_f_to_c(day[1])
        max_temp = convert_f_to_c(day[2])

        daily_summary += (
            f"---- {convert_date(date)} ----\n"
            f"  Minimum Temperature: {format_temperature(min_temp)}\n"
            f"  Maximum Temperature: {format_temperature(max_temp)}\n\n"
        )

    return daily_summary