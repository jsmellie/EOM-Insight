from categorizing.category import Category

_categories = None | list[Category]

def get_category(name: str) -> Category | None:
    global _categories
    if _categories is None:
        return None
    for category in _categories:
        if category.name == name:
            return category
    return None

def test_categories():
    global _categories
    _categories = []
    food_entries = ['grocery store', 'restaurant', 'cafe']
    utilities_entries = ['electricity', 'water', 'internet']
    food_category = Category.from_str_list('Food', food_entries)
    utilities_category = Category.from_str_list('Utilities', utilities_entries)
    _categories.append(food_category)
    _categories.append(utilities_category)

    for category in _categories:
        category.save_to_file()
if __name__ == '__main__':   
    test_categories()