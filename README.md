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

- _Interactive GUI_: Offers six input fields for defining the source and destination parameters of each wire.
- _Data Management_: Handles wire data efficiently by storing user input in JSON format.
- _CSV Output_: converts wire data into a structured CSV format for export
- _Localization support_: English, Russian, Spanish, French, Shakespearean English
- _Settings window_: Enables adjustment of language, default save locations, and CSV delimiter
- _Increment functionality_: Provides a checkbutton to automatically Increment the numbers in the terminal fields.
- _JSON content validation_: Ensures the integrity of the content within the application.
- Export data to CSV files

## Screenshots
*New Project Dialog Window*
![New Project Dialog Window](https://github.com/voidfemme/label_wires/blob/main/data/Screenshots/NewProjectDialogScreen.png)

*Main Application Window*
![Main Application Window](https://github.com/voidfemme/label_wires/blob/main/data/Screenshots/MainApplicationWindow.png)

*Settings Menu*
![Settings Window](https://github.com/voidfemme/label_wires/blob/main/data/Screenshots/SettingsWindow.png)
