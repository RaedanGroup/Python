import pickle

# Initialize 2 empty lists
recipes_list = []
ingredients_list = []

def take_recipe():
    # Recipe name input
    name = input("Enter the name of the recipe: ")
    # Cooking time input
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    # Ingredients input which are separated by commas and stripped of any leading or trailing whitespaces
    ingredients = [ingredient.strip() for ingredient in input("Enter the ingredients (separated by commas): ").split(',')]
    # Calculate the difficulty of the recipe
    difficulty = calc_difficulty(cooking_time, len(ingredients))
    # Create a dictionary with the recipe details
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
        'difficulty': difficulty
    }
    
    # Return result as variable 'recipe'
    return recipe

# Determine the difficulty of each recipe
def calc_difficulty(cooking_time, num_ingredients):
    
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    elif cooking_time >= 10 and num_ingredients >= 4:
        return "Hard"
    
# Have the user enter a filename
save_filename = input("Enter the filename to load data from: ")

# Try-except-else-finally block
try:
    with open(save_filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print(f"File '{save_filename}' not found. Creating new data structure.")
    data = {
        'recipes_list': recipes_list,
        'all_ingredients': ingredients_list
    }
except Exception as e:
    print(f"An error occurred: {e}. Creating new data structure.")
    data = {
        'recipes_list': recipes_list,
        'all_ingredients': ingredients_list
    }
else:
    file.close()
finally:
    # Extract the values from the dictionary into two separate lists
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']

# Number of recipes to be input
n = int(input("How many recipes would you like to enter? "))

# Run loop 'n' times to gather recipes
for i in range(n):
    # Run take_recipe() and store its return output (a dictionary) in a variable called recipe
    recipe = take_recipe()
    
    # Iterate through recipe's ingredients list
    for ingredient in recipe['ingredients']:
        # If the ingredient is not in ingredients_list, add it to the list
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    
    # Append the recipe to recipes_list
    recipes_list.append(recipe)

# Gather the updated recipes_list and ingredients_list into the dictionary called data
data = {
    'recipes_list': recipes_list,
    'all_ingredients': ingredients_list
}

# Open a binary file with the user-defined filename and write data to it using the pickle module
with open(save_filename, 'wb') as file:
    pickle.dump(data, file)

print("Data successfully saved to", save_filename)
