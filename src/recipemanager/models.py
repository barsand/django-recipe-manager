from django.db import models


class Ingredient(models.Model):
    ean = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    unit = models.CharField(max_length=10)

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=100, decimal_places=2)

class RecipeListing(models.Model):
    recipe_id = models.IntegerField()
    ingredient_id = models.IntegerField()
    ingredient_quantity = models.DecimalField(max_digits=100, decimal_places=2)

