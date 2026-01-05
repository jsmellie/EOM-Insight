import os
from categorizing.category_entry import CategoryEntry
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
            
        save_categories()
            
def save_categories():
    global _categories
    if _categories is None:
        return
    for category in _categories:
        category.save_to_file()
        
def prompt_category_selection(transaction) -> Category | None:
    global _categories
    if _categories is None:
        load_categories()
    print("-~- Manual transaction categorization required -~-")
    print(f"Transaction info: {transaction}")
    print("Please select a category for this transaction:")
    for i, category in enumerate(_categories):
        print(f"{i + 1}. {category.name}")
    print(f"{len(_categories) + 1}. Create a new category")
    selection = input("Enter the number of the category: ")
    try:
        selection_num = int(selection)
        if 1 <= selection_num <= len(_categories):
            return _categories[selection_num - 1]
        elif selection_num == len(_categories) + 1:
            new_category_name = input("Enter the name of the new category: ")
            new_category = Category.from_str_list(new_category_name, [])
            _categories.append(new_category)
            return new_category
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

def categorize_transaction(transaction) -> bool:
    if _categories is None:
        load_categories()
    if transaction.category is not None:
        raise ValueError("Transaction is already categorized.")
    
    found_category = None
    for category in _categories:
        if (category.is_valid_entry(transaction.sum)):
            found_category = category
            break
    if found_category is not None:
        transaction.category = found_category.name
        return True
    
    found_category = prompt_category_selection(transaction)
    if found_category is not None:
        transaction.category = found_category.name
        found_category.add_entry(CategoryEntry.from_prompt(transaction.sum))
        return True
    return False

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