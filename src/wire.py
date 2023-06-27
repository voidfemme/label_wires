#!/usr/bin/env python3
# Workers of the world, Unite!
import json


class Wire:
    def __init__(
        self,
        source_component,
        source_terminal_block,
        source_terminal,
        destination_component,
        destination_terminal_block,
        destination_terminal,
    ):
        self.source_component = source_component
        self.source_terminal_block = source_terminal_block
        self.source_terminal = source_terminal
        self.destination_component = destination_component
        self.destination_terminal_block = destination_terminal_block
        self.destination_terminal = destination_terminal
        self.source_str = (
            f"{self.source_component}-{self.source_terminal_block}-{source_terminal}"
        )
        self.destination_str = f"{self.destination_component}-{self.destination_terminal_block}-{self.destination_terminal}"

    def __str__(self) -> str:
        return f"{self.source_component}-{self.source_terminal_block}-{self.source_terminal}".strip(
            "-"
        ).replace(
            "--", "-"
        ) + f", {self.destination_component}-{self.destination_terminal_block}-{self.destination_terminal}".strip(
            "-"
        ).replace(
            "--", "-"
        )

    def __eq__(self, other: "Wire") -> bool:
        if not isinstance(other, Wire):
            return NotImplemented
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

    def to_dict(self):
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
