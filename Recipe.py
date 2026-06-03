from Ingredient import Ingredient

class Recipe:
    
    def __init__(self, title, ingredients):
        self.title = title
        self.ingredients = []
        for ingredient in ingredients:
            self.add_ingredient(ingredient)
        
    def add_ingredient(self, ingredient: Ingredient):
        for ingred in self.ingredients:
            if ingred.__eq__(ingredient):
                ingred.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)
            
    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and ratio > 0
    
    def scale(self, ratio: float):
        if Recipe.is_valid_ratio(ratio):
            ingredients_new = []
            for ingredient in self.ingredients:
                ingredients_new.append(Ingredient(ingredient.name, ingredient.quantity * ratio, ingredient.unit))
            return Recipe(self.title, ingredients_new)
        raise ValueError("Коэффициент должен быть положительным")
    
    def __len__(self):
        return len(self.ingredients)
    
    def __str__(self):
        if not self.ingredients:
            return f"У {self.title} пока нет ингредиентов"
        ingredients_str = []
        for ingredient in self.ingredients:
            ingredients_str.append(str(ingredient))
        return f"{self.title}\n" + "\n".join(ingredients_str)