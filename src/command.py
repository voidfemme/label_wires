import logging

logger = logging.getLogger(__name__)


class Command:
    def execute(self):
        pass

    def undo(self):
        pass


class AddConnectionCommand(Command):
    def __init__(self, app, source, destination):
        self.app = app
        self.source = source
        self.destination = destination
        self.item = None

    def execute(self):
        connection = self.app.connection_manager.add_connection(
            self.source["component"],
            self.source["terminal_block"],
            self.source["terminal"],
            self.destination["component"],
            self.destination["terminal_block"],
            self.destination["terminal"],
        )

        source, destination = self.app.connection_manager.get_connection_tuple(
            connection
        )

        # Add to tree widget and get unique identifier
        self.item = self.app.tree_widget.insert("", "end", values=(source, destination))

        # Add to the mapping dictionary
        self.app.tree_item_to_connection[self.item] = connection

        # Print a message to the UI
        self.app.display_status(
            self.app.localizer.get("added_connection").format(
                source=source, destination=destination
            )
        )

        # Update the listbox to reflect the new connection list
        self.app.update_connection_list()

    def undo(self):
        connection = self.app.tree_item_to_connection.pop(self.item)
        self.app.connection_manager.delete_connection(connection)
        self.app.tree_widget.delete(self.item)
        self.app.display_status(
            self.app.localizer.get("removed_connection").format(connection=connection)
        )
        self.app.update_connection_list()


class DeleteConnectionCommand(Command):
    def __init__(
        self, tree_widget, tree_item_to_connection, connections_dict, connection_manager
    ):
        self.tree_widget = tree_widget
        self.tree_item_to_connection = tree_item_to_connection
        self.connections_dict = connections_dict
        self.connection_manager = connection_manager
        self.item = None
        self.connection = None

    def execute(self):
        for item in self.tree_widget.selection():
            try:
                self.connection = self.tree_item_to_connection[item]
                self.item = item
            except KeyError:
                logger.warning(f"Connection not found for item: {item}")
                continue
            logger.info(f"Deleting connection: {self.connection}")

            # Attempt to delete the connection
            try:
                self.connection_manager.delete_connection(self.connection)
            except Exception as e:
                logger.warning(
                    f"Could not delete {self.connection} from connection manager: {e}"
                )
                continue  # Skip this connection

            # Attempt to delete from connections_dict
            try:
                del self.connections_dict[str(self.connection)]
            except KeyError:
                logger.warning(f"Connection {self.connection} not found in connections_dict")

            # Attempt to delete from tree_item_to_connection
            try:
                del self.tree_item_to_connection[item]
            except KeyError:
                logger.warning(f"Item {item} not found in tree_item_to_connection")
        pass

    def undo(self):
        # Add the connection back to the connection manager
        self.connection_manager.add_connection(self.connection)

        # Add the connection back to the connections_dict
        self.connections_dict[str(self.connection)] = self.connection

        # Add the connection back to tree_item_to_connection
        self.tree_item_to_connection[self.item] = self.connection
