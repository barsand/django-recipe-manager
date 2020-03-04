from django.http import HttpResponse
from .controllers import IngredientManager, RecipeManager


def index(request):
    return HttpResponse('aloha!')


def ingredient_list(request):
    return IngredientManager.list(request)


def ingredient_create(request):
    return IngredientManager.create(request)


def ingredient_view(request, ingredient_id):
    return HttpResponse('viewing %s' % ingredient_id)


def ingredient_edit(request, ingredient_id):
    return IngredientManager.edit(request, ingredient_id)


def ingredient_delete(request, ingredient_id):
    return IngredientManager.delete(request, ingredient_id)


def recipe_list(request):
    return RecipeManager.list(request)


def recipe_create(request):
    return RecipeManager.create(request)
