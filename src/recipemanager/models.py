from django.db import models


class Ingredient(models.Model):
    ean = models.CharField(max_length=13, primary_key=True)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    unit = models.CharField(max_length=10)

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=100, decimal_places=2)

class RecipeListing(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    ingredient_quantity = models.DecimalField(max_digits=100, decimal_places=2)

