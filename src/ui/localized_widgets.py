import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from src.localizer import Localizer

logger = logging.getLogger(__name__)

"""
This file contains versions of Tkinter widgets that follow the Observer design pattern.
They each observe a localization key and update their displayed text whenever the
associated value in the localizer changes.

The Observer pattern allows me to decouple the localization logic from the UI logic.
"""


class LocalizedLabel(tk.Label):
    _all_instances = []

    def __init__(
        self,
        parent,
        localizer: Localizer,
        l10n_key: str,
        format_args=None,
        **kwargs,
    ) -> None:
        super().__init__(parent, text=self.get_localized_text(), **kwargs)
        self.localizer = localizer
        self.l10n_key = l10n_key
        self.format_args = format_args or {}
        self._all_instances.append(self)
        logger.info(f"Initialized {self.__class__.__name__} with key {self.l10n_key}")

    def get_localized_text(self) -> str:
        return self.localizer.get(self.l10n_key).format(**self.format_args)

    def update_format_args(self, new_format_args) -> None:
        self.format_args.update(new_format_args)
        self.update()

    def update(self) -> None:
        new_text = self.localizer.get(self.l10n_key).format(**self.format_args)
        logger.info(f"Updating {type(self).__name__} with key {self.l10n_key}")
        logger.info(f"new_text: {new_text}")
        self.config(text=new_text)

    def destroy(self) -> None:
        # Ensures that we free up the widgets when we're done
        self._all_instances.remove(self)
        super().destroy()

    @classmethod
    def update_all(cls) -> None:
        logger.info("Called LocalizedLabel.update_all()")
        logger.info(f"Number of instances: {len(cls._all_instances)}")
        for instance in cls._all_instances:
            logger.info(f"Updating instance: {instance}")
            instance.update()


class LocalizedButton(tk.Button):
    _all_instances = []

    def __init__(
        self, parent, localizer: Localizer, l10n_key: str, format_args=None, **kwargs
    ) -> None:
        super().__init__(parent, text=self.get_localized_text(), **kwargs)
        self.localizer = localizer
        self.l10n_key = l10n_key
        self.format_args = format_args or {}
        self._all_instances.append(self)

    def get_localized_text(self) -> str:
        return self.localizer.get(self.l10n_key)

    def update_format_args(self, new_format_args) -> None:
        self.format_args.update(new_format_args)
        self.update()

    def update(self) -> None:
        new_text = self.localizer.get(self.l10n_key).format(**self.format_args)
        self.config(text=new_text)

    def destroy(self) -> None:
        self._all_instances.remove(self)
        super().destroy()

    @classmethod
    def update_all(cls) -> None:
        print("Called LocalizedButton.update_all()")
        for instance in cls._all_instances:
            instance.update()


class LocalizedCheckButton(tk.Checkbutton):
    _all_instances = []

    def __init__(
        self, master, localizer: Localizer, l10n_key: str, format_args=None, **kwargs
    ) -> None:
        self.localizer = localizer
        self.l10n_key = l10n_key
        self.format_args = format_args or {}
        super().__init__(master, text=self.get_localized_text(), **kwargs)
        self._all_instances.append(self)

    def get_localized_text(self) -> str:
        return self.localizer.get(self.l10n_key).format(**self.format_args)

    def update_format_args(self, new_format_args) -> None:
        self.format_args.update(new_format_args)
        self.update()

    def update(self) -> None:
        new_text = self.localizer.get(self.l10n_key).format(**self.format_args)
        self.config(text=new_text)

    def destroy(self) -> None:
        self._all_instances.remove(self)
        super().destroy()

    @classmethod
    def update_all(cls) -> None:
        print("Called LocalizedCheckButton.update_all()")
        for instance in cls._all_instances:
            instance.update()


class LocalizedCombobox(ttk.Combobox):
    _all_instances = []

    def __init__(self, master, localizer: Localizer, values_key: str, **kwargs) -> None:
        self.localizer = localizer
        self.values_key = values_key
        values = localizer.get(self.values_key)
        super().__init__(master, values=values, **kwargs)
        self._all_instances.append(self)

    def update(self) -> None:
        new_values = self.localizer.get(self.values_key)
        self.config(values=new_values)

    def destroy(self) -> None:
        self._all_instances.remove(self)
        super().destroy()

    @classmethod
    def update_all(cls) -> None:
        print("Called LocalizedCombobox.update_all()")
        for instance in cls._all_instances:
            instance.update()


class LocalizedTreeview(ttk.Treeview):
    _all_instances = []

    def __init__(self, master, localizer, columns_keys_mapping, **kwargs) -> None:
        self.localizer = localizer
        self.columns_keys_mapping = columns_keys_mapping
        super().__init__(master, columns=columns_keys_mapping.keys(), **kwargs)
        self._all_instances.append(self)
        self.update()

    def update(self) -> None:
        for col_id, key in self.columns_keys_mapping.items():
            title = self.localizer.get(key)
            self.heading(col_id, text=title)

    def destroy(self) -> None:
        self._all_instances.remove(self)
        super().destroy()

    @classmethod
    def update_all(cls) -> None:
        print("Called LocalizedTreeview.update_all()")
        for instance in cls._all_instances:
            instance.update()
