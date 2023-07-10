import logging

logger = logging.getLogger(__name__)


class Command:
    def execute(self):
        pass

    def undo(self):
        pass


class EditConnectionCommand(Command):
    def __init__(self, parent, source, destination, item) -> None:
        self.parent = parent
        self.source = source
        self.destination = destination
        self.item = item
        self.old_source = None
        self.old_destination = None

    def execute(self) -> None:
        print("Executing edit connection command")
        connection = self.parent.tree_item_to_connection[self.item]
        self.old_source = self.parent.connection_manager.get_connection_tuple(
            connection
        )[0]
        self.old_destination = self.parent.connection_manager.get_connection_tuple(
            connection
        )[1]

        self.parent.connection_manager.delete_connection(connection)
        connection = self.parent.connection_manager.add_connection(
            self.source["component"],
            self.source["terminal_block"],
            self.source["terminal"],
            self.destination["component"],
            self.destination["terminal_block"],
            self.destination["terminal"],
        )

        source, destination = self.parent.connection_manager.get_connection_tuple(
            connection
        )

        # Add to tree widget and get unique identifier
        self.item = self.parent.tree_widget.insert(
            "", "end", values=(source, destination)
        )

        # Add to the mapping dictionary
        self.parent.tree_item_to_connection[self.item] = connection

        # Print a message to the UI
        self.parent.display_status(
            self.parent.localizer.get("added_connection").format(
                source=source, destination=destination
            )
        )

        # Update the tree widget to reflect the new connection list
        self.parent.update_connection_list()

    def undo(self):
        pass


class AddConnectionCommand(Command):
    def __init__(self, parent, source, destination) -> None:
        self.parent = parent
        self.source = source
        self.destination = destination
        self.item = None

    def execute(self) -> None:
        connection = self.parent.connection_manager.add_connection(
            self.source["component"],
            self.source["terminal_block"],
            self.source["terminal"],
            self.destination["component"],
            self.destination["terminal_block"],
            self.destination["terminal"],
        )

        source, destination = self.parent.connection_manager.get_connection_tuple(
            connection
        )

        # Add to tree widget and get unique identifier
        self.item = self.parent.tree_widget.insert(
            "", "end", values=(source, destination)
        )

        # Add to the mapping dictionary
        self.parent.tree_item_to_connection[self.item] = connection

        # Print a message to the UI
        self.parent.display_status(
            self.parent.localizer.get("added_connection").format(
                source=source, destination=destination
            )
        )

        # Update the tree widget to reflect the new connection list
        self.parent.update_connection_list()

    def undo(self) -> None:
        connection = self.parent.tree_item_to_connection.pop(self.item)
        self.parent.connection_manager.delete_connection(connection)
        self.parent.tree_widget.delete(self.item)
        self.parent.display_status(
            self.parent.localizer.get("removed_connection").format(
                connection=connection
            )
        )
        self.parent.update_connection_list()


class DeleteConnectionCommand(Command):
    def __init__(self, parent) -> None:
        self.parent = parent
        self.deleted_items = []  # Store deleted items here

    def execute(self) -> None:
        for item in self.parent.tree_widget.selection():
            # Future: revise the deletion method to be more transactional, and only delete
            # from the lists if I can delete from all three, otherwise fail the operation
            # ... I'll need a mechanism to either revert the deletions that have already
            # occurred
            try:
                connection = self.parent.tree_item_to_connection[item]

                # Attempt to delete the connection
                try:
                    self.parent.connection_manager.delete_connection(connection)
                except Exception as e:
                    logger.warning(
                        f"Could not delete {connection} from connection manager: {e}"
                    )
                    continue  # Skip this connection

                # Attempt to delete from connections_dict
                try:
                    del self.parent.connections_dict[str(connection)]
                except KeyError:
                    logger.warning(
                        f"Connection {connection} not found in connections_dict"
                    )

                # Attempt to delete from tree_item_to_connection
                try:
                    del self.parent.tree_item_to_connection[item]
                except KeyError:
                    logger.warning(f"Item {item} not found in tree_item_to_connection")

                self.deleted_items.append(
                    {
                        "item": item,
                        "connection": connection,
                        "source_component": connection.source_component,
                        "source_terminal_block": connection.source_terminal_block,
                        "source_terminal": connection.source_terminal,
                        "destination_component": connection.destination_component,
                        "destination_terminal_block": connection.destination_terminal_block,
                        "destination_terminal": connection.destination_terminal,
                    }
                )
            except KeyError:
                logger.warning(f"Connection not found for item: {item}")
                continue

    def undo(self) -> None:
        for deleted_item in self.deleted_items:
            connection = deleted_item["connection"]
            item = deleted_item["item"]
            source_component = deleted_item["source_component"]
            source_terminal_block = deleted_item["source_terminal_block"]
            source_terminal = deleted_item["source_terminal"]
            destination_component = deleted_item["destination_component"]
            destination_terminal_block = deleted_item["destination_terminal_block"]
            destination_terminal = deleted_item["destination_terminal"]

            # Add the connection back to the connection manager
            self.parent.connection_manager.add_connection(
                source_component,
                source_terminal_block,
                source_terminal,
                destination_component,
                destination_terminal_block,
                destination_terminal,
            )

            # Add the connection back to the connections_dict
            self.parent.connections_dict[str(connection)] = connection

            # Add the connection back to tree_item_to_connection
            self.parent.tree_item_to_connection[item] = connection

            # Add the connection back to the tree widget
            source, destination = self.parent.connection_manager.get_connection_tuple(
                connection
            )
            new_item = self.parent.tree_widget.insert(
                "", "end", values=(source, destination)
            )
            self.parent.display_status(
                self.parent.localizer.get("added_connection").format(
                    source=source, destination=destination
                )
            )
        self.deleted_items.clear()
        self.parent.update_connection_list()
