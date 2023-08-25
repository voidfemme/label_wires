import logging
from src.connection import Connection

logger = logging.getLogger(__name__)


class Command:
    def execute(self):
        pass

    def undo(self):
        pass


class AddConnectionCommand(Command):
    def __init__(self, event_system, connection_manager, source, destination) -> None:
        self.connection_manager = connection_manager
        self.source = source
        self.destination = destination
        self.item = None
        self.event_system = event_system

    def __repr__(self):
        return "AddConnectionCommand"

    def execute(self) -> None:
        # Add the connection in the connection manager
        self.connection = self.connection_manager.add_connection(
            self.source["component"],
            self.source["terminal_block"],
            self.source["terminal"],
            self.destination["component"],
            self.destination["terminal_block"],
            self.destination["terminal"],
        )

        # Publish an event that a connection has been added
        self.event_system.publish("connection_added", self.connection)

    def undo(self) -> None:
        self.connection_manager.delete_connection(self.connection)

        # Publish an event that a connection has been removed
        self.event_system.publish("connection_removed", self.connection)


class DeleteConnectionCommand(Command):
    """
    Deletes a connection from the connection manager
    """

    def __init__(self, parent, view) -> None:
        self.parent = parent
        self.view = view
        self.deleted_items = []  # Store deleted items here

    def __repr__(self):
        return "DeleteConnectionCommand"

    def execute(self) -> None:
        for item_to_delete in self.view.tree_widget.selection():
            try:
                connection = self.view.tree_widget.tree_item_to_connection[
                    item_to_delete
                ]

                # Attempt to delete the connection from the connection manager
                try:
                    self.parent.connection_manager.delete_connection(connection)
                except Exception as e:
                    logger.warning(
                        f"Could not delete {connection} from connection manager: {e}"
                    )
                    continue  # Skip this connection

                # Attempt to delete from connections_dict
                try:
                    del self.view.tree_widget.connections_dict[str(connection)]
                except KeyError:
                    logger.warning(
                        f"Connection {connection} not found in connections_dict"
                    )

                # Attempt to delete from tree_item_to_connection
                try:
                    del self.view.tree_widget.tree_item_to_connection[item_to_delete]
                except KeyError:
                    logger.warning(
                        f"Item {item_to_delete} not found in tree_item_to_connection"
                    )

                self.deleted_items.append(
                    {
                        "item": item_to_delete,
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
                logger.warning(f"Connection not found for item: {item_to_delete}")
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
            self.view.tree_widget.connections_dict[str(connection)] = connection

            # Add the connection back to tree_item_to_connection
            self.view.tree_widget.tree_item_to_connection[item] = connection

            # Add the connection back to the tree widget
            source, destination = self.parent.connection_manager.get_connection_tuple(
                connection
            )
            self.view.tree_widget.insert("", "end", values=(source, destination))
            self.parent.display_status(
                self.parent.localizer.get("added_connection").format(
                    source=source, destination=destination
                )
            )
        self.deleted_items.clear()
        self.parent.update_connection_list()


class EditConnectionCommand(Command):
    # Rewrite the other two commands so that I can make this a composition of those two.
    def __init__(
        self,
        connection_manager,
        old_connection: Connection,
        new_values: dict[str, str],
    ) -> None:
        self.connection_manager = connection_manager
        self.old_connection = old_connection
        self.new_values = new_values
        self.connections_to_edit = []

    def __repr__(self) -> str:
        return "EditConnectionCommand"

    def execute(self) -> None:
        self.old_values = self.old_connection.to_dict()

        new_connection = Connection(**self.new_values)
        self.connection_manager.add_connection(**new_connection.to_dict())
        self.connection_manager.delete_connection(self.old_connection)

    def undo(self) -> None:
        new_connection = Connection(**self.new_values)

        self.connection_manager.add_connection(**self.old_connection.to_dict())
        self.connection_manager.delete_connection(new_connection)
