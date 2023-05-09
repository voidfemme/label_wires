#!/usr/bin/env python3
import csv


def is_duplicate_or_reverse(wire, wires):
    reverse_wire = (wire[1], wire[0])
    return wire in wires or reverse_wire in wires


def gather_input():
    """
    Gather user input for components, terminal blocks, terminals, and destinations.

    Returns:
    list: A list of wire tuples containing the source and destination.
    """
    wires = []

    while True:
        component = input("Component: ").upper()
        if not component:
            print("Quitting...")
            break

        terminal_block = None
        while terminal_block != "":
            terminal_block = input(f"{component}-: ").upper()
            if not terminal_block:
                print("Skipping...")
                break

            terminal = None
            while terminal != "":
                terminal = input(f"{component}-{terminal_block}-: ").upper()
                if not terminal:
                    print("Skipping...")
                    break

                destination = input(
                    f"{component}-{terminal_block}-{terminal} destination: "
                ).upper()

                wire = (f"{component}-{terminal_block}-{terminal}", destination)

                if not is_duplicate_or_reverse(wire, wires):
                    wires.append(wire)
                    print(
                        f"Added: {component}-{terminal_block}-{terminal}, {destination}"
                    )
                else:
                    print("Duplicate or reverse duplicate detected. Skipping...")

    return wires


def save_to_csv(csv_file_name, wires):
    """
    Save the wires list as a CSV file.

    Args:
    csv_file_name (str): The name of the CSV file.
    wires (list): A list of wire tuples containing the source and destination.
    """
    try:
        with open(f"wirenums/{csv_file_name}.csv", "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            for wire in wires:
                print(wire)
                csv_writer.writerow(wire)
    except Exception as e:
        print(f"Error saving CSV file: {e}")


def main():
    """
    Main function to gather user input and save the wiring data as a CSV file.
    """
    csv_file_name = input("CSV file name: ")
    wires = gather_input()
    save_to_csv(csv_file_name, wires)


if __name__ == "__main__":
    main()
