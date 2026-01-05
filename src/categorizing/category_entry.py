

class CategoryEntry:
    name = None | str
    description = None | str
    regex = None | str

    def __init__(self, name: str, description: str = None, regex: str = None):
        self.name = name
        self.description = description
        if regex is not None:
            self.regex = regex
        else:
            self.regex = name
            
    @classmethod
    def from_json(cls, json: dict):
        if json is None:
            return None
        name = json.get('name')
        description = json.get('description')
        regex = json.get('regex')
        return cls(name, description, regex)
    
    @classmethod
    def from_prompt(cls, name: str):
        description = input(f"Enter a description for the category entry '{name}' (or leave blank): ")
        regex = input(f"Enter a regex pattern for the category entry '{name}' (or leave blank to use the name): ")
        if regex.strip() == "":
            regex = None
        return cls(name, description if description.strip() != "" else None, regex)
    
    def compare(self, transaction) -> bool:
        import re
        pattern = re.compile(self.regex, re.IGNORECASE)
        return bool(pattern.search(transaction))