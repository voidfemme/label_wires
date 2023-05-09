# Wire Labeling Tool
This program is a wire labeling tool that allows users to input wire connections and store them in a CSV file. It provides filtering options to view specific wire connections based on user-defined criteria. The tool can also load previous wire connections from existing CSV files for further modifications.
## Installation
    1. Clone this repository or download the zip file containing the project.
    2. Navigate to the project directory in your terminal or command prompt.
    3. Ensure you have Python 3 installed. If not, download it from the official Python website.
## Usage
    1. Run the `main.py` script in your terminal or command prompt with the command `python main.py`.
    2. Enter the CSV file name when prompted. Make sure it doesn't contain any invalid characters.
    3. If any existing CSV files with matching names are found, select the file to load the existing wire connections.
    4. Enter the wire connection information in the following format: `Component`, `Terminal Block`, `Terminal`, and `Destination`. Leave fields empty to skip or type `quit` to stop inputting connections.
    5. Use the filtering options to view specific wire connections by entering the filter criteria and value.
    6. The program will save the wire connections to the specified CSV file.
## Features
    - Gather wire connection input with validation for each field
    - Load existing wire connections from CSV files
    - Save wire connections to CSV files
    - Filter wire connections based on specified criteria
    - Detect duplicate or reverse duplicate connections
## Functions
    - `is_valid_input(input_string: str) -> bool`: Checks if the input is alphanumeric.
    - `is_valid_destination(destination: str) -> bool`: Validates the destination input based on a regex pattern.
    - `is_valid_file_name(file_name: str) -> bool`: Checks for invalid characters in the file name.
    - `WireManager` class:
        - `__init__(self, csv_file_name: str, output_dir: str)`: Initializes the WireManager with the given CSV file name and output directory.
        - `is_duplicate_or_reverse(self, wire: Tuple[str, str]) -> bool`: Checks if the given wire is a duplicate or reverse duplicate in the list of wires.
        - `print_wires(self) -> None`: Prints the list of wires.
        - `gather_input(self) -> None`: Gathers wire connection input from the user.
        - `save_to_csv(self) -> None`: Saves the wire connections to a CSV file.
        - `load_from_csv(self) -> None`: Loads existing wire connections from a CSV file.
        - `filter_wires(self, filter_by: str, filter_value: str) -> List[Tuple[str, str]]`: Filters wires based on the given criteria and value.
## main.py
The `main.py` script contains the main function that initializes a `WireManager` instance, loads any existing CSV files, gathers wire connection input, filters wires, and saves the connections to a CSV file.
