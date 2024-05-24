import pickle

# Display the recipe details
def display_recipe(recipe):
    print(f"Recipe: {recipe['name']}")
    print(f"Cooking Time (min): {recipe['cooking_time']}")
    print("Ingredients:")
    for ingredient in recipe['ingredients']:
        print(f"  {ingredient}")
    print(f"Difficulty Level: {recipe['difficulty']}\n")

def search_ingredient(data):
    # Display all available ingredients
    all_ingredients = data.get('all_ingredients', [])
    print("Available Ingredients:")
    for index, ingredient in enumerate(all_ingredients):
        print(f"{index}. {ingredient}")

    # Try to get user input and search for the ingredient
    try:
        choice = int(input("Input an ingredient number to search for recipes:"))
        ingredient_searched = all_ingredients[choice]
    except (ValueError, IndexError):
        print("Invalid. Please use a number from the list.")
    else:
        print(f"Showing recipes for the ingredient: {ingredient_searched}\n")
        for recipe in data.get('recipes_list', []):
            if ingredient_searched in recipe['ingredients']:
                display_recipe(recipe)

# Get filename from user that contains the recipe data
filename = input("Enter the filename that contains your recipe data: ")

# Load the data from the file
try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print(f"File '{filename}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")
else:
    search_ingredient(data)