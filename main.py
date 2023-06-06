#!/usr/bin/env python3
# Workers of the world, Unite!
from src.wire_manager import WireManager, WIRENUMS_DIR, is_valid_file_name


def main():
    csv_file_name = input("CSV file name: ")
    while not is_valid_file_name(csv_file_name):
        print("Invalid file name. Please try again")
        csv_file_name = input("CSV file name: ")
        if csv_file_name.lower() == "quit":
            return

    wire_manager = WireManager(csv_file_name, WIRENUMS_DIR)
    wire_manager.load_from_csv()
    wire_manager.gather_input()

    # Filtering wires
    filter_by = input(
        "Filter wires by (component, terminal_block, terminal, destination): "
    )
    if filter_by.lower() == "quit":
        wire_manager.save_to_csv()
        return
    filter_value = input(f"Enter the value to filter by {filter_by}: ")
    if filter_value.lower() == "quit":
        wire_manager.save_to_csv()
        return
    filtered_wires = wire_manager.filter_wires(filter_by, filter_value)

    print("Filtered wires")
    for i, wire in enumerate(filtered_wires):
        print(f"{i + 1}. {wire}")

    wire_manager.save_to_csv()


if __name__ == "__main__":
    main()
