class Recipe:
    all_ingredients = set()

    def __init__(self, name, cooking_time):
        self.name = name
        self.ingredients = []
        self.cooking_time = cooking_time
        self.difficulty = None
        self.calculate_difficulty()
    
    # Getter and Setter for name
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
    
    # Getter and Setter for cooking_time
    def get_cooking_time(self):
        return self.cooking_time
    
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
        self.calculate_difficulty()
    
    # Method to add ingredients
    def add_ingredients(self, *ingredients):
        self.ingredients.extend(ingredients)
        self.update_all_ingredients()
        self.calculate_difficulty()
    
    # Getter for ingredients
    def get_ingredients(self):
        return self.ingredients
    
    # Method to calculate difficulty
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = "Hard"
    
    # Getter for difficulty
    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty
    
    # Method to search for an ingredient
    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients
    
    # Method to update all_ingredients class variable
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            Recipe.all_ingredients.add(ingredient)
    
    # String representation of the recipe
    def __str__(self):
        ingredients_str = ', '.join(self.ingredients)
        return (f"Recipe: {self.name}\n"
                f"Cooking Time (min): {self.cooking_time}\n"
                f"Ingredients: {ingredients_str}\n"
                f"Difficulty Level: {self.difficulty}\n")
    
    # Method to search for recipes based on multiple ingredients
    def recipe_search(data, search_terms):
        print(f"Recipes containing any of the ingredients: {', '.join(search_terms)}\n")
        found_recipes = []
        for recipe in data:
            if any(recipe.search_ingredient(term) for term in search_terms):
                found_recipes.append(recipe)
        
        if found_recipes:
            for recipe in found_recipes:
                print(recipe)
        else:
            print("No recipes found containing any of the search terms.")
        print("\n")

# Example recipes:
tea = Recipe("Tea", 5)
tea.add_ingredients("Tea Leaves", "Sugar", "Water")

coffee = Recipe("Coffee", 5)
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")

cake = Recipe("Cake", 50)
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")

banana_smoothie = Recipe("Banana Smoothie", 5)
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")

# List of all example recipes
recipes_list = [tea, coffee, cake, banana_smoothie]

# Use the recipe_search() method to search for recipes containing multiple ingredients
Recipe.recipe_search(recipes_list, ["Water", "Sugar", "Bananas"])
