# Destination Wire Label Generator

The Destination Wire Label Generator is a tool designed to generate and maintain a list of wires. It features a user-friendly GUI for easy management and exportation of these lists into CSV format

## Description

This application allows users to define and manage wire connections through a GUI. Each wire connection is defined by three source fields and three destination fields, namely: 'component', 'terminal block' and 'terminal'. The GUI provides separate fields for these input parameters, allowing the user to edit each field independently.

Once the user fills in these fields, the program stores the data in JSON format. During the export process, the application converts this data into a structured CSV format. The CSV output for each wire will follow this format:

`{component}-{terminal block}-{terminal}, {component}-{terminal block}-{terminal}`

Or in the cable format variant:

`{component}-{terminal block} [{terminal}], {component}-{terminal block} [{terminal}]`

In this format, the portion before the comma represents the source while the portion after the comma represents the destination.

## Getting Started

### Prerequisites

- This software requires Python 3 for installation

Note: An installation script/Windows installation wizard is currently under development and will be available soon

## Features

- **Interactive GUI**: Offers six input fields for defining the source and destination parameters of each wire.
- **OS Compatibility**: Compatible with Windows and Linux
- **Data Management**: Handles wire data efficiently by storing user input in JSON format.
- **CSV Output**: converts wire data into a structured CSV format for export
- **Localization support**: English, Russian, Spanish(to be checked for errors), French (to be checked for errors), Shakespearean English
- **Settings window**: Enables adjustment of language, default save locations, and CSV delimiter
- **Increment functionality**: Provides a checkbutton to automatically Increment the numbers in the terminal fields.
- **JSON content validation**: Ensures the integrity of the content within the application.
- **Export data to CSV files**: Use a custom delimiter. I recommend avoiding using a comma as the delimiter, since it can sometimes be advantageous to use commas in the text fields. I recommend using a pipe symbol: "|"

### Coming soon

- Installation wizard
- Auto-detect commas in label data and choose the pipe symbol if they exist.
- Full documentation panel for instructions on using the software and for importing to Brady LabelMark 6 software for printing.
- Traceback included in user-facing error message for easier debugging of user-tested features

## Screenshots

**New Project Dialog Window**

![New Project Dialog Window](https://github.com/voidfemme/label_wires/blob/main/data/Screenshots/NewProjectDialogScreen.png)

**Main Application Window**

![Main Application Window](https://github.com/voidfemme/label_wires/blob/main/data/Screenshots/MainApplicationWindow.png)

**Settings Menu**

![Settings Window](https://github.com/voidfemme/label_wires/blob/main/data/Screenshots/SettingsWindow.png)

## Known Bugs

- Various formatted strings are not displaying the correct data.
    - Specifically the formatted strings when adding a new connection.
- Missing "success" message when saving settings. There should be some kind of feedback about the updated state of all the settings.
- Quit button broken
