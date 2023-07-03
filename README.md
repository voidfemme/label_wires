# Destination Wire Label Generator

Generates and maintains a list of wires and export them to CSV.

## Description
Provides a convenient GUI for managing and generating a list of wires. The user can export them to CSV while allowing you to input termination addresses in the format:
`{component}-{terminal block}-{terminal}, {component}-{terminal block}-{terminal}`
Or in the cable format variant
`{component}-{terminal block} [{terminal}], {component}-{terminal block} [{terminal}]`

Where the left side of the comma represents the source and the right side, the destination.
The program aims to provide an easy-to-use interface that is efficient.

## Getting Started

### Prerequisites
Must have Python 3 to install.
(Coming soon: installation script/Windows installation wizard)

## Features

- Tree view widget to display and interact with connections
- Localization support
- Settings window to adjust language, default save locations, and CSV delimiter
- Increment functionality for terminal number input fields
- JSON content validation
- Export data to CSV files
