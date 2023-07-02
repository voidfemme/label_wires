import tkinter as tk
from tkinter import ttk


class LocalizedLabel(tk.Label):
    _all_instances = []

    def __init__(self, master, localizer, text_key, **kwargs):
        super().__init__(master, text=localizer.get(text_key), **kwargs)
        self.localizer = localizer
        self.text_key = text_key
        self._all_instances.append(self)

    def update(self):
        new_text = self.localizer.get(self.text_key)
        self.config(text=new_text)

    @classmethod
    def update_all(cls):
        for instance in cls._all_instances:
            instance.update()


class LocalizedButton(tk.Button):
    _all_instances = []

    def __init__(self, master, localizer, text_key, **kwargs):
        super().__init__(master, text=localizer.get(text_key), **kwargs)
        self.localizer = localizer
        self.text_key = text_key
        self._all_instances.append(self)

    def update(self):
        new_text = self.localizer.get(self.text_key)
        self.config(text=new_text)

    @classmethod
    def update_all(cls):
        for instance in cls._all_instances:
            instance.update()


class LocalizedCheckButton(tk.Checkbutton):
    _all_instances = []

    def __init__(self, master, localizer, text_key, **kwargs):
        super().__init__(master, text=localizer.get(text_key), **kwargs)
        self.localizer = localizer
        self.text_key = text_key
        self._all_instances.append(self)

    def update(self):
        new_text = self.localizer.get(self.text_key)
        self.config(text=new_text)

    @classmethod
    def update_all(cls):
        for instance in cls._all_instances:
            instance.update()


class LocalizedCombobox(ttk.Combobox):
    _all_instances = []

    def __init__(self, master, localizer, values_key, **kwargs):
        self.localizer = localizer
        self.values_key = values_key
        values = localizer.get(values_key)
        super().__init__(master, values=values, **kwargs)
        self._all_instances.append(self)

    def update(self):
        new_values = self.localizer.get(self.values_key)
        self.config(values=new_values)

    @classmethod
    def update_all(cls):
        for instance in cls._all_instances:
            instance.update()


class LocalizedTreeView(ttk.Treeview):
    _all_instances = []

    def __init__(self, master, localizer, columns_keys_mapping, **kwargs):
        self.localizer = localizer
        self.columns_keys_mapping = columns_keys_mapping
        super().__init__(master, columns=columns_keys_mapping.keys(), **kwargs)
        self._all_instances.append(self)
        self.update()

    def update(self):
        for col_id, key in self.columns_keys_mapping.items():
            title = self.localizer.get(key)
            self.heading(col_id, text=title)

    @classmethod
    def update_all(cls):
        for instance in cls._all_instances:
            instance.update()
