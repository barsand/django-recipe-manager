from django.db import models


class Ingredient(models.Model):
    ean = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    unit = models.CharField(max_length=10)

