from Recipe import Recipe
from Ingredient import Ingredient

class ShoppingList:
    
    def __init__(self):
        self._items = []
        
    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количестов порций должно быть положительным")
        recipe_new = recipe.scale(portions)
        for ingredient in recipe_new.ingredients:
            self._items.append((ingredient, recipe.title))
            
    def remove_recipe(self, title: str):
        for element in self._items:
            if element[1] == title:
                self._items.remove(element)

    def get_list(self):
        totals = {}
        for ingredient, title in self._items:
            element = (ingredient.name, ingredient.unit)
            if element in totals:
                totals[element] += ingredient.quantity
            else:
                totals[element] = ingredient.quantity
        result = []
        for (name, unit), quantity in totals.items():
            result.append(Ingredient(name, quantity, unit))
        result.sort()
        return result
    
    def __add__(self, other: "ShoppingList"):
        united_items = ShoppingList()
        united_items = self._items + other._items
        return united_items