import tkinter as tk
from tkinter import ttk


class LocalizedLabel(tk.Label):
    _all_instances = []

    def __init__(self, master, localizer, l10n_key, **kwargs):
        super().__init__(master, text=localizer.get(l10n_key), **kwargs)
        self.localizer = localizer
        self.l10n_key = l10n_key
        self._all_instances.append(self)
        print(f"Initialized {self.__class__.__name__} with key {self.l10n_key}")

    def update(self):
        new_text = self.localizer.get(self.l10n_key)
        print(f"Updating {type(self).__name__} with key {self.l10n_key}")
        print(f"new_text: {new_text}")
        self.config(text=new_text)

    def destroy(self):
        self._all_instances.remove(self)
        super().destroy()

    @classmethod
    def update_all(cls):
        print("Called LocalizedLabel.update_all()")
        print(f"Number of instances: {len(cls._all_instances)}")
        for instance in cls._all_instances:
            print(f"Updating instance: {instance}")
            instance.update()


class LocalizedButton(tk.Button):
    _all_instances = []

    def __init__(self, master, localizer, l10n_key, **kwargs):
        super().__init__(master, text=localizer.get(l10n_key), **kwargs)
        self.localizer = localizer
        self.l10n_key = l10n_key
        self._all_instances.append(self)

    def update(self):
        new_text = self.localizer.get(self.l10n_key)
        print(f"Updating {type(self).__name__} with key {self.l10n_key}")
        print(f"new_text: {new_text}")
        self.config(text=new_text)

    def destroy(self):
        self._all_instances.remove(self)
        super().destroy()

    @classmethod
    def update_all(cls):
        print("Called LocalizedButton.update_all()")
        for instance in cls._all_instances:
            instance.update()


class LocalizedCheckButton(tk.Checkbutton):
    _all_instances = []

    def __init__(self, master, localizer, l10n_key, **kwargs):
        super().__init__(master, text=localizer.get(l10n_key), **kwargs)
        self.localizer = localizer
        self.l10n_key = l10n_key
        self._all_instances.append(self)

    def update(self):
        new_text = self.localizer.get(self.l10n_key)
        print(f"Updating {type(self).__name__} with key {self.l10n_key}")
        print(f"new_text: {new_text}")
        self.config(text=new_text)

    def destroy(self):
        self._all_instances.remove(self)
        super().destroy()

    @classmethod
    def update_all(cls):
        print("Called LocalizedCheckButton.update_all()")
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

    def destroy(self):
        self._all_instances.remove(self)
        super().destroy()

    @classmethod
    def update_all(cls):
        print("Called LocalizedCombobox.update_all()")
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

    def destroy(self):
        self._all_instances.remove(self)
        super().destroy()

    @classmethod
    def update_all(cls):
        print("Called LocalizedTreeView.update_all()")
        for instance in cls._all_instances:
            instance.update()
