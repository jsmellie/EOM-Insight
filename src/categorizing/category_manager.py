import os
import utils.constants as constants

from categorizing.category import Category

DEFAULT_CATEGORIES = ['Food', 'Utilities', 'Entertainment', 'Transportation', 'Healthcare', 'Housecare', 'Subscriptions', 'Personal Care', 'Gifts & Donations', 'Travel', 'Miscellaneous', 'Income', 'Retirement', 'Fun Money']

_categories = None | list[Category]

def get_category(name: str) -> Category | None:
    global _categories
    if _categories is None:
        return None
    for category in _categories:
        if category.name == name:
            return category
    return None

def load_categories():
    global _categories

    _categories = []
    for filename in os.listdir(constants.CATEGORY_PATH):
        if Category.is_category_file(filename):
            file_path = os.path.join(constants.CATEGORY_PATH, filename)
            category = Category.load_from_file(file_path)
            _categories.append(category)
                
    if len(_categories) == 0:
        for category_name in DEFAULT_CATEGORIES:
            category = Category.from_str_list(category_name, [])
            _categories.append(category)
            
        for category in _categories:
            category.save_to_file()
            
def save_categories():
    global _categories
    if _categories is None:
        return
    for category in _categories:
        category.save_to_file()

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