from django.contrib import admin
from .models import Ingredient, Recipe, RecipeListing


admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeListing)
