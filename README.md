# WireLab

WireLab is a Python application designed to handle wire label data for a specific format. It allows users to input wire label information, manipulate and view the data in a user-friendly interface, and export the wires into a CSV file.
Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [File Handling](#file-handling)
- [Exporting](#exporting)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Installation {#installation}

To use WireLab, follow these steps:
    - Clone the WireLab repository from GitHub: [link to repository]
    - Install the required dependencies. WireLab relies on the following Python libraries:
        tkinter
    - You can install the dependencies using pip:
    ```shell
    pip install tkinter
    ```

## Usage {#usage}

To run the WireLab application, execute the following command in your terminal:

```shell
python wirelab.py
```

The application will start and display the "New Project" window, where you can choose the mode of entry and either load an existing file or create a new file.
## Features {#features}

1. *Mode of Entry*: WireLab supports two modes of entry: "Wire" and "Cable." You can choose the desired mode in the "New Project" window. The mode determines the format of the wire label data.

2. *Wire Label Format*: Each wire or cable consists of six fields: three for the destination and three for the source. The fields include:
- Component
- Terminal Block
- Terminal

Wires follow the format: `component-terminal_block-terminal`, while cables follow the format: `component-terminal_block [terminal]`.

3. *User Interface*: WireLab utilizes the tkinter library to provide a graphical user interface (GUI). After creating or loading a file, the main window displays the wire objects in a tree widget with two columns: "Destination" and "Source." The tree widget allows for easy navigation and visualization of the wire data.

## File Handling {#file-handling}

WireLab allows you to create new wire label files or load existing ones. The file handling process is as follows:

1. *New Project*: When the application starts, the "New Project" window is presented. You can select the mode of entry and choose either to load an existing file or create a new file.

2. *Loading Files*: If you choose to load an existing file, use the "Browse" button to locate and select the desired file. The file should be in JSON format and contain the saved wire objects.

3. *Creating a New File*: To create a new file, specify the desired mode of entry and choose a suitable location to save the file. WireLab will save the wire objects in a JSON file format.

## Exporting {#exporting}

WireLab allows you to export wire data into a CSV file. The exporting process is as follows:

1. *Exporting*: In the WireLab main window, click on the "Export" button. A browse menu will appear, allowing you to choose the location to save the CSV file.

2. *CSV File Format*: The exported CSV file will follow the comma-separated values (CSV) format. By default, the fields will be separated by commas. In a future update, a setting will be added to allow customization of the separator.

## Configuration {#configuration}

WireLab supports some configuration options, like language, default wire and cable file directory and default CSV export directory

## Contributing {#contributing}

If you are interested in contributing to WireLab, feel free to fork the repository and submit pull requests with your proposed changes. Contributions are always welcome and appreciated.

## License {#license}

To be continued...
