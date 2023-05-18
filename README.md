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

- Compatible with both Windows and Linux. Untested for Apple Mac
- Gather wire connection input with validation for each field
- Load existing wire connections from CSV files
- Save wire connections to CSV files
- Filter wire connections based on specified criteria
- Detect duplicate or reverse duplicate connections

## main.py

The `main.py` script contains the main function that initializes a `WireManager` instance, loads any existing CSV files, gathers wire connection input, filters wires, and saves the connections to a CSV file.

## To Do:

- Fix `int(input())` section where it increments the number to support non-numeric entries without erroring
- Make the wire manager its own minimal text editor
- Create an installer for Windows
- Add "undo" button
- Cable mode and non-destination mode tabs
