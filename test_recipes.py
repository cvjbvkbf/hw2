import pytest
from Ingredient import Ingredient
from Recipe import Recipe
from ShoppingList import ShoppingList


class TestIngredient:

    def test_init(self):
        ing = Ingredient("Мука", 500, "г")
        assert ing.name == "Мука"
        assert ing.quantity == 500.0
        assert ing.unit == "г"

    def test_str(self):
        ing = Ingredient("Мука", 500, "г")
        assert str(ing) == "Мука: 500.0 г"

    def test_eq_same_name_and_unit(self):
        ing1 = Ingredient("Мука", 500, "г")
        ing2 = Ingredient("Мука", 200, "г")
        assert ing1 == ing2

    def test_eq_different_name(self):
        ing1 = Ingredient("Мука", 500, "г")
        ing2 = Ingredient("Сахар", 500, "г")
        assert ing1 != ing2

    def test_eq_different_unit(self):
        ing1 = Ingredient("Мука", 500, "г")
        ing2 = Ingredient("Мука", 500, "кг")
        assert ing1 != ing2


class TestRecipe:

    def test_init(self):
        recipe = Recipe("Пицца")
        assert recipe.title == "Пицца"
        assert recipe.ingredients == []

    def test_add_ingredient_new(self):
        recipe = Recipe("Пицца")
        recipe.add_ingredient(Ingredient("Мука", 500, "г"))
        assert len(recipe) == 1

    def test_add_ingredient_duplicate_sums_quantity(self):
        recipe = Recipe("Пицца")
        recipe.add_ingredient(Ingredient("Мука", 500, "г"))
        recipe.add_ingredient(Ingredient("Мука", 200, "г"))
        assert len(recipe) == 1
        assert recipe.ingredients[0].quantity == 700.0

    def test_scale_returns_new_object(self):
        recipe = Recipe("Пицца")
        recipe.add_ingredient(Ingredient("Мука", 500, "г"))
        new_recipe = recipe.scale(2)
        assert new_recipe is not recipe

    def test_scale_multiplies_quantities(self):
        recipe = Recipe("Пицца")
        recipe.add_ingredient(Ingredient("Мука", 500, "г"))
        new_recipe = recipe.scale(2)
        assert new_recipe.ingredients[0].quantity == 1000.0

    def test_scale_invalid_ratio_raises(self):
        recipe = Recipe("Пицца")
        with pytest.raises(ValueError):
            recipe.scale(-1)

    def test_len(self):
        recipe = Recipe("Пицца")
        recipe.add_ingredient(Ingredient("Мука", 500, "г"))
        recipe.add_ingredient(Ingredient("Яйца", 2, "шт"))
        assert len(recipe) == 2