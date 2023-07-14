# Love is love. Be yourself.
from typing import Dict, Tuple
from dataclasses import dataclass

"""
Connection class describes each connection in terms of the source and destination components,
terminal blocks, and terminals. This is used to create a unique identifier for each connection
that can be used to compare connections and to create a dictionary representation of the
connection.
"""


@dataclass
class Connection:
    source_component: str
    source_terminal_block: str
    source_terminal: str
    destination_component: str
    destination_terminal_block: str
    destination_terminal: str

    def __post_init__(self):
        attributes = [
            self.source_component,
            self.source_terminal_block,
            self.source_terminal,
            self.destination_component,
            self.destination_terminal_block,
            self.destination_terminal,
        ]
        if not all(isinstance(attribute, str) for attribute in attributes):
            raise ValueError("All inputs must be of type string")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Connection):
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
        return is_normal_equal or is_reverse_equal

    def __str__(self) -> str:
        source = f"{self.source_component}-{self.source_terminal_block}-{self.source_terminal}"
        destination = f"{self.destination_component}-{self.destination_terminal_block}-{self.destination_terminal}"
        return f"{source},{destination}"

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

    def to_tuple(self) -> Tuple[str, str]:
        return (
            f"{self.source_component}-{self.source_terminal_block}-{self.source_terminal}",
            f"{self.destination_component}-{self.destination_terminal_block}-{self.destination_terminal}",
        )
