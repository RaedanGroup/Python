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
    
    # Create a dictionary with the recipe details
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients
    }
    
    # Return result as variable 'recipe'
    return recipe

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

# Determine the difficulty of each recipe
for recipe in recipes_list:
    cooking_time = recipe['cooking_time']
    num_ingredients = len(recipe['ingredients'])
    
    if cooking_time < 10 and num_ingredients < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and num_ingredients >= 4:
        difficulty = "Hard"
    
    # Add the difficulty to the recipe dictionary
    recipe['difficulty'] = difficulty

# Display the recipes in the specified format
for recipe in recipes_list:
    print(f"Recipe: {recipe['name']}")
    print(f"Cooking Time (min): {recipe['cooking_time']}")
    print("Ingredients:")
    for ingredient in recipe['ingredients']:
        print(f"  {ingredient}")
    print(f"Difficulty Level: {recipe['difficulty']}\n")

# Print the ingredients list in alphabetical order and with a header
print("Ingredients available across all recipes")
print("----------------------------------------")
for ingredient in sorted(ingredients_list):
    print(ingredient)
