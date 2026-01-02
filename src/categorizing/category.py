import json
import os
import utils.constants as constants

from categorizing.category_entry import CategoryEntry

class Category:
    name = None | str
    entries = None | list[CategoryEntry]
    
    def __init__(self, name: str, entries: list[CategoryEntry] = None):
        self.name = name
        self.entries = entries if entries is not None else []
    
    @classmethod
    def from_str_list(cls, name: str, str_list: list[str]):
        entries = [CategoryEntry(name=entry) for entry in str_list]
        return cls(name, entries)
    
    @classmethod
    def from_json(cls, json: dict):
        name = json.get('name')
        entries_data = json.get('entries', [])
        entries = []
        for entry_data in entries_data:
            entry = CategoryEntry.from_json(entry_data)
            entries.append(entry)
        return cls(name, entries)

    def add_entry(self, entry: CategoryEntry):
        self.entries.append(entry)
        
    def remove_entry(self, entry: CategoryEntry):
        self.entries.remove(entry)
        
    def save_to_file(self):
        file_path = os.path.join(constants.CATEGORY_PATH,
                                 constants.CATEGORY_FILE_FORMAT.format(self.name))
        with open(file_path, 'w') as f:
            json.dump(self, f, default=lambda o: o.__dict__, indent=4)
        
    