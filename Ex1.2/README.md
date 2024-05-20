# Exercise 1.2: Data Types in Python
---
# Task Answers:
## (Step 1) Decide what data structure you would use for this purpose, and in your README file in the repository for this task, describe in approx. 50-75 words why you’ve chosen to use it.

For this purpose, I would use a Python dictionary to create the structure named recipe_1. A dictionary is an ideal choice because it allows for the association of unique keys (like name, cooking_time, and ingredients) with specific values. This makes it easy to access and manipulate each piece of data individually. Dictionaries are also flexible and can store different data types, making them suitable for this use case.

## (Step 3) Figure out what type of structure you would consider for all_recipes, and briefly note down your justification in the README file. Ideally, this outer structure should be sequential in nature, where multiple recipes can be stored and modified as required.

For the all_recipes structure, I would use a list. A list is a sequential data structure that allows for the storage of multiple items in an ordered fashion. It supports adding, removing, and modifying elements, making it ideal for managing a collection of recipes. Lists also allow for easy iteration, which is useful for operations like displaying all recipes or searching for a specific one. The all_recipes list can easily be expanded to include more recipes by appending additional recipe dictionaries to it. This makes it a flexible and straightforward choice for managing multiple recipes.