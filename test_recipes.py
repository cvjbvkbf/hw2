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


class TestShoppingList:
    
    def _make_pizza(self):
        recipe = Recipe("Пицца")
        recipe.add_ingredient(Ingredient("Мука", 500, "г"))
        recipe.add_ingredient(Ingredient("Сыр", 150, "г"))
        return recipe

    def _make_salad(self):
        recipe = Recipe("Салат")
        recipe.add_ingredient(Ingredient("Мука", 100, "г"))
        recipe.add_ingredient(Ingredient("Огурцы", 200, "г"))
        return recipe

    def test_add_recipe(self):
        shop = ShoppingList()
        shop.add_recipe(self._make_pizza(), 1)
        assert len(shop._items) == 2

    def test_add_recipe_invalid_portions_raises(self):
        shop = ShoppingList()
        with pytest.raises(ValueError, match="Количество порций должно быть положительным"):
            shop.add_recipe(self._make_pizza(), 0)

    def test_remove_recipe(self):
        shop = ShoppingList()
        shop.add_recipe(self._make_pizza(), 1)
        shop.remove_recipe("Пицца")
        assert shop._items == []

    def test_remove_recipe_not_found_no_error(self):
        shop = ShoppingList()
        shop.add_recipe(self._make_pizza(), 1)
        shop.remove_recipe("Несуществующий рецепт")
        assert len(shop._items) == 2

    def test_get_list_sums_same_ingredients(self):
        shop = ShoppingList()
        shop.add_recipe(self._make_pizza(), 1)
        shop.add_recipe(self._make_salad(), 1)
        result = shop.get_list()
        flour = next(i for i in result if i.name == "Мука")
        assert flour.quantity == 600.0

    def test_get_list_sorted_by_name(self):
        shop = ShoppingList()
        shop.add_recipe(self._make_pizza(), 1)
        shop.add_recipe(self._make_salad(), 1)
        result = shop.get_list()
        names = [i.name for i in result]
        assert names == sorted(names)

    def test_add_combines_into_new_list(self):
        shop1 = ShoppingList()
        shop1.add_recipe(self._make_pizza(), 1)
        shop2 = ShoppingList()
        shop2.add_recipe(self._make_salad(), 1)
        combined = shop1 + shop2
        assert len(combined._items) == len(shop1._items) + len(shop2._items)

    def test_add_does_not_modify_originals(self):
        shop1 = ShoppingList()
        shop1.add_recipe(self._make_pizza(), 1)
        shop2 = ShoppingList()
        shop2.add_recipe(self._make_salad(), 1)
        original_len1 = len(shop1._items)
        original_len2 = len(shop2._items)
        shop1 + shop2
        assert len(shop1._items) == original_len1
        assert len(shop2._items) == original_len2