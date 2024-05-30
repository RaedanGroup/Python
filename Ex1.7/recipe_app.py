from sqlalchemy import create_engine, Column, String, Integer, or_
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Database Configuration
USERNAME = "cf-python"
PASSWORD = "password"
HOST = "localhost"
DATABASE = "task_database"

# Engine to connect to the database
engine = create_engine(f"mysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}")

# Define the base class for all models
Base = declarative_base()

# Session configuration
Session = sessionmaker(bind=engine)
session = Session()

class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"<Recipe(id={self.id}, name={self.name}, difficulty={self.difficulty})>"
    
    def __str__(self):
        ingredients_list = self.ingredients.split(", ")
        formatted_ingredients = "\n  - ".join(ingredient.title() for ingredient in ingredients_list)

        return (f"Recipe ID: {self.id}\n"
                f"\tName: {self.name.title()}\n"
                f"\tIngredients:\n\t\t- {formatted_ingredients}\n"
                f"\tCooking Time: {self.cooking_time} minutes\n"
                f"\tDifficulty: {self.difficulty}\n")
    
    def calculate_difficulty(self):
        num_ingredients = len(self.return_ingredients_as_list())
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        return self.ingredients.split(", ")

Base.metadata.create_all(engine)

def create_recipe():
    """Function to create new recipes and add them to the database."""
    print("Create New Recipes")

    while True:
        try:
            number_of_recipes = int(input("How many recipes would you like to enter? (Enter a number): "))
            if number_of_recipes < 1:
                print("Please enter a positive number.\n")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.\n")
    
    for i in range(number_of_recipes):
        print(f"\nRecipe #{i + 1}")

        while True:
            name = input("Enter the recipe name: ").strip()
            if 0 < len(name) <= 50:
                break
            else:
                print("Please enter a valid recipe name (1-50 characters).\n")

        while True:
            try:
                cooking_time = int(input("Enter the cooking time in minutes: "))
                if cooking_time > 0:
                    break
                else:
                    print("Please enter a positive number for cooking time.\n")
            except ValueError:
                print("Invalid input. Please enter a positive number for cooking time.\n")

        while True:
            ingredients_input = input("Enter the recipe's ingredients, separated by a comma: ").strip()
            if ingredients_input:
                break
            else:
                print("Please enter at least one ingredient.\n")

        new_recipe = Recipe(name=name, ingredients=ingredients_input, cooking_time=cooking_time)
        new_recipe.calculate_difficulty()

        session.add(new_recipe)
        try:
            session.commit()
            print("Added Successfully!")
        except SQLAlchemyError as err:
            session.rollback()
            print("Error occurred: ", err)

    final_message = "Recipe submitted." if number_of_recipes == 1 else "All recipes submitted."
    print("="*30)
    print(f"{final_message}\n\n")
    print("="*30)

def view_all_recipes():
    """Function to view all recipes from the database."""
    recipes = session.query(Recipe).all()

    if not recipes:
        print("There are no recipes.")
        return

    print("View All Recipes")
    recipe_count = len(recipes)
    recipe_word = "recipe" if recipe_count == 1 else "recipes"
    print(f"Displaying {recipe_count} {recipe_word}\n")

    for i, recipe in enumerate(recipes, start=1):
        print(f"Recipe #{i}")
        print("_"*40)
        print(format_recipe_for_search(recipe))
        print("-"*40)

def search_recipe():
    """Function to search for recipes by ingredient."""
    results = session.query(Recipe.ingredients).all()

    if not results:
        print("There are no recipes.")
        return

    all_ingredients = set()
    for result in results:
        ingredients_list = result[0].split(", ")
        all_ingredients.update(ingredient.strip() for ingredient in ingredients_list)

    print("Enter number to see recipes using that ingredient\n")
    sorted_ingredients = sorted(all_ingredients)
    for i, ingredient in enumerate(sorted_ingredients):
        print(f"{i+1}.) {ingredient.title()}")

    while True:
        try:
            choices = input("Enter ingredient numbers (separate multiple numbers with spaces): ").split()
            selected_indices = [int(choice) for choice in choices]
            if all(1 <= choice <= len(all_ingredients) for choice in selected_indices):
                break
            else:
                print("Please enter numbers within the list range.\n")
        except ValueError:
            print("Invalid input. Please enter valid numbers.\n")

    search_ingredients = [sorted_ingredients[index - 1] for index in selected_indices]
    search_conditions = [Recipe.ingredients.ilike(f"%{ingredient}%") for ingredient in search_ingredients]
    search_results = session.query(Recipe).filter(or_(*search_conditions)).all()

    if len(search_ingredients) > 1:
        selected_ingredients_str = ", ".join(ingredient.title() for ingredient in search_ingredients[:-1])
        selected_ingredients_str += ", or " + search_ingredients[-1].title()
    else:
        selected_ingredients_str = search_ingredients[0].title()

    if search_results:
        recipe_count = len(search_results)
        recipe_word = "recipe" if recipe_count == 1 else "recipes"
        print(f"\n{recipe_count} {recipe_word} found containing '{selected_ingredients_str}'\n")
        
        for i, recipe in enumerate(search_results, start=1):
            print(f"Recipe #{i}\n----------")
            print(format_recipe_for_search(recipe))
            print()

        print("^^^^^^^^^^^^^^^^^")
        print("^^^end of line^^^")
        print("^^^^^^^^^^^^^^^^^")
    else:
        print(f"No recipes found containing '{selected_ingredients_str}'\n")

def update_recipe():
    """Function to update a recipe in the database."""
    recipes = session.query(Recipe).all()

    if not recipes:
        print("No recipes found.")
        return
    
    print("Please enter ID number to update that recipe\n")
    print("Available Recipes\n")
    for recipe in recipes:
        print(format_recipe_for_update(recipe))

    while True:
        try:
            recipe_id = int(input("Enter the ID of the recipe to update: "))
            recipe_to_update = session.get(Recipe, recipe_id)
            if recipe_to_update:
                break
            else:
                print("No recipe found with the entered ID. Please try again.\n")
        except ValueError:
            print("Invalid input. Please enter a numeric value.\n")

    print(f"\nWhich field would you like to update for '{recipe_to_update.name}'?")
    print(" - Name")
    print(" - Time")
    print(" - Ingredients\n")

    field_updated = False
    while not field_updated:
        update_field = input("Enter your choice: ").lower()

        if update_field == "name":
            while True:
                new_value = input("\nEnter the new name (1-50 characters): ").strip()
                if 0 < len(new_value) <= 50:
                    recipe_to_update.name = new_value
                    field_updated = True
                    break
                else:
                    print("Invalid name. Please enter 1-50 characters.\n")
            break

        elif update_field in ["time", "cooking time"]:
            while True:
                try:
                    new_value = int(input("\nEnter the new cooking time (in minutes): "))
                    if new_value > 0:
                        recipe_to_update.cooking_time = new_value
                        recipe_to_update.calculate_difficulty()
                        field_updated = True
                        break
                    else:
                        print("Please enter a positive number for cooking time.")
                except ValueError:
                    print("Invalid input. Please enter a numeric value for cooking time.")
            break
                    
        elif update_field == "ingredients":
            while True:
                new_value = input("\nEnter the new ingredients, separated by a comma: ").strip()
                if new_value:
                    recipe_to_update.ingredients = new_value
                    recipe_to_update.calculate_difficulty()
                    field_updated = True
                    break
                else:
                    print("Please enter at least one ingredient.") 
            break
        else:
            print("Invalid choice. Please choose 'name', 'time', or 'ingredients'.")

    try:
        session.commit()
        print("Successfully updated the recipe!\n")
    except SQLAlchemyError as err:
        session.rollback()
        print(f"An error occurred: {err}")

def delete_recipe():
    """Function to delete a recipe from the database."""
    recipes = session.query(Recipe).all()

    if not recipes:
        print("There are no recipes to delete.")
        return
    
    print("Please enter the ID number of the recipe to remove")
    print("Available Recipes\n")
    for recipe in recipes:
        print(format_recipe_for_update(recipe))

    while True:
        try:
            recipe_id = int(input("\nEnter the ID of the recipe to delete: "))
            recipe_to_delete = session.get(Recipe, recipe_id)

            if recipe_to_delete:
                confirm = input(f"\nAre you sure you want to delete '{recipe_to_delete.name}'? (Yes/No): ").lower()
                if confirm == "yes":
                    break
                elif confirm == "no":
                    print("Deletion cancelled.\n")
                    return
                else:
                    print("Please answer with 'Yes' or 'No'.")
            else:
                print("No recipe found with that ID.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    try:
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe deleted")
    except SQLAlchemyError as err:
        session.rollback()
        print(f"An error occurred: {err}")

def format_recipe_for_search(recipe):
    """Format recipe for displaying search results."""
    formatted_ingredients = "\n\t\t".join(f"-> {ingredient.title()}" for ingredient in recipe.return_ingredients_as_list())
    return (f"Recipe Name: {recipe.name.title()}\n"
            f"\tCooking Time: {recipe.cooking_time} mins\n"
            f"\tIngredients:\n\t\t{formatted_ingredients}\n"
            f"\tDifficulty: {recipe.difficulty}")

def format_recipe_for_update(recipe):
    """Format recipe for displaying update options."""
    capitalized_ingredients = [ingredient.title() for ingredient in recipe.return_ingredients_as_list()]
    capitalized_ingredients_str = ", ".join(capitalized_ingredients)
    return (f"ID: {recipe.id} | Name: {recipe.name}\n"
            f"Ingredients: {capitalized_ingredients_str} | Cooking Time: {recipe.cooking_time} | Difficulty: {recipe.difficulty}\n")

def main_menu():
    """Main menu function to navigate through the application."""
    choice = ""
    while choice != "quit":
        print("\n\n")
        print("="*40)
        print(" "*10 + "Recipe App Main Menu")
        print("="*40)
        print("(1) Create a new recipe")
        print("(2) View all recipes")
        print("(3) Search for a recipe by ingredient")
        print("(4) Update an existing recipe")
        print("(5) Delete a recipe")
        print("-"*40)
        print("(!) Enter 'quit' to... quit.")
        print("="*40)
        print("\/"*20)
        choice = input("Your choice: ").strip().lower()

        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_recipe()
        elif choice == "4":
            update_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "quit":
            print("\n. . . Quitter.\n\n\t\tFine. As you \"command\", exiting the program...\n")
            break
        else:
            print("Wrong. Try again.\n")

    session.close()
    engine.dispose()

main_menu()
