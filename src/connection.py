# Love is love. Be yourself.
from abc import ABC, abstractmethod
from typing import Dict, Tuple

"""
Connection classes describe each connection in terms of the source and destination components,
terminal blocks, and terminals. This is used to create a unique identifier for each connection
that can be used to compare connections and to create a dictionary representation of the
connection.
"""

# This file has a high degree of coupling, and could really use some work from the ground up


class Connection(ABC):
    def __init__(
        self,
        source_component: str,
        source_terminal_block: str,
        source_terminal: str,
        destination_component: str,
        destination_terminal_block: str,
        destination_terminal: str,
    ) -> None:
        # Validate inputs
        attributes = [
            source_component,
            source_terminal_block,
            source_terminal,
            destination_component,
            destination_terminal_block,
            destination_terminal,
        ]
        if not all(isinstance(attribute, str) for attribute in attributes):
            raise ValueError("All inputs must be of type string")

        self.source_component = source_component
        self.source_terminal_block = source_terminal_block
        self.source_terminal = source_terminal
        self.destination_component = destination_component
        self.destination_terminal_block = destination_terminal_block
        self.destination_terminal = destination_terminal

    def __eq__(self, other: "Wire") -> bool:
        if not isinstance(other, Wire):
            return False
        is_normal_equal = (
            self.source_component == other.source_component
            and self.source_terminal_block == other.source_terminal_block
            and self.source_terminal == other.source_terminal
            and self.destination_component == other.destination_component
            and self.destination_terminal_block == other.destination_terminal_block
            and self.destination_terminal == other.destination_terminal
        )
        is_reverse_equal = (
            self.source_component == other.destination_component
            and self.source_terminal_block == other.destination_terminal_block
            and self.source_terminal == other.destination_terminal
            and self.destination_component == other.source_component
            and self.destination_terminal_block == other.source_terminal_block
            and self.destination_terminal == other.source_terminal
        )

        print(
            f"Comparing cables, normal: {is_normal_equal}, reverse: {is_reverse_equal}\n",
            f"Evaluates to {is_normal_equal or is_reverse_equal}"
        )

        return is_normal_equal or is_reverse_equal

    def to_dict(self) -> Dict[str, str]:
        return {
            "source_component": self.source_component,
            "source_terminal_block": self.source_terminal_block,
            "source_terminal": self.source_terminal,
            "destination_component": self.destination_component,
            "destination_terminal_block": self.destination_terminal_block,
            "destination_terminal": self.destination_terminal,
        }

    def is_empty(self) -> bool:
        return not any(
            getattr(self, attr)
            for attr in [
                "source_component",
                "source_terminal_block",
                "source_terminal",
                "destination_component",
                "destination_terminal_block",
                "destination_terminal",
            ]
        )

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def to_tuple(self):
        pass


class Wire(Connection):
    def __str__(self) -> str:
        source = f"{self.source_component}-{self.source_terminal_block}-{self.source_terminal}"
        destination = f"{self.destination_component}-{self.destination_terminal_block}-{self.destination_terminal}"
        return f"{source},{destination}"

    def to_tuple(self) -> Tuple[str, str]:
        return (
            f"{self.source_component}-{self.source_terminal_block}-{self.source_terminal}",
            f"{self.destination_component}-{self.destination_terminal_block}-{self.destination_terminal}",
        )
