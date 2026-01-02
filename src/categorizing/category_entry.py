

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