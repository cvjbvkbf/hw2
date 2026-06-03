from Recipe import Recipe

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
        for element in self._items[:]:
            if element[1] == title:
                self._items.remove(element)
    
    def get_list(self) -> list:
        pass
    
    def __add__(self, other: "ShoppingList"):
        united_items = ShoppingList()
        united_items = self._items + other._items
        return united_items