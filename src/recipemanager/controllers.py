from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from .models import Ingredient, Recipe, RecipeListing
import collections
import json

def ingredient_already_exists(ean, name):
    if len(Ingredient.objects.filter(Q(ean=ean) | Q(name=name))):
        return True
    else:
        return False

def parse_valid_form_data(request, model):
    model_fields = [f.attname for f in model._meta.fields]
    parsed_form_data = dict()
    for field in request.POST:
        if field in model_fields:
            parsed_form_data[field] = request.POST[field]
    return parsed_form_data

class IngredientManager():
    def list(request):
        ingredients = Ingredient.objects.all()
        return render(request, 'recipemanager/ingredient_list.html', {'ingredients': ingredients})

    def create(request):
        if request.method == 'GET':
            return render(request, 'recipemanager/ingredient_create.html')
        elif request.method == 'POST':
            parsed_form_data = parse_valid_form_data(request, Ingredient)
            try:
                if ingredient_already_exists(parsed_form_data['ean'], parsed_form_data['name']):
                    return_payload = {
                        'error': 'name and/or ean already taken',
                        'form_data': parsed_form_data
                    }
                    return render(request, 'recipemanager/ingredient_create.html', return_payload)

                Ingredient(**parsed_form_data).save()
            except Exception as exp:
                return HttpResponse(status=500)

            success_msg = {'success': 'Ingredient created!'}
            return render(request, 'recipemanager/ingredient_create.html', success_msg)

    def edit(request, ingredient_id):
        if request.method == 'GET':
            ingredient = Ingredient.objects.filter(ean=ingredient_id)[0]
            return render(request, 'recipemanager/ingredient_edit.html', {'form_data': ingredient})
        elif request.method == 'POST':
            parsed_form_data = parse_valid_form_data(request, Ingredient)
            ingredient = Ingredient.objects.filter(ean=ingredient_id)[0]
            updated_fields = 0
            for field, form_value in parsed_form_data.items():
                if str(ingredient.__getattribute__(field)) != form_value:
                    setattr(ingredient, field, form_value)
                    updated_fields += 1
            ingredient.save()
            if updated_fields:
                return render(request, 'recipemanager/ingredient_edit.html', {'success': 'Ingredient updated!'})
            else:
                return render(request, 'recipemanager/ingredient_edit.html', {'success': 'Nothing changed!'})

    def delete(request, ingredient_id):
        try:
            Ingredient.objects.filter(ean=ingredient_id)[0].delete()
            return render(request, 'recipemanager/ingredient_delete.html', {
                'success': 'Sucessfully deleted ingredient #%s.' % ingredient_id})
        except Exception as exp:
            return render(request, 'recipemanager/ingredient_delete.html')


class RecipeManager():
    def list(request):
        return HttpResponse('list!')

    def create(request):
        if request.method == 'GET':
            ingredients = Ingredient.objects.all()
            return render(request, 'recipemanager/recipe_create.html', {'ingredients': ingredients})
        if request.method == 'POST':
            recipe_eans = list()
            for field in request.POST:
                if field[:20] == 'ingredient-selected-':
                    recipe_eans.append(field[20:])

            recipe_ingredients = list()
            ean2quantity = dict()
            recipe_cost = 0
            for ean in recipe_eans:
                ingredient = Ingredient.objects.filter(ean=ean)[0]
                recipe_ingredients.append(ingredient)
                curr_quantity = float(request.POST['%s-item-quantity' % ean])
                ean2quantity[ean] = curr_quantity

                recipe_cost += curr_quantity/float(ingredient.amount)*float(ingredient.price)

            recipe = Recipe(name=request.POST['name'], cost=recipe_cost)
            recipe.save()

            for ean in recipe_eans:
                listing = RecipeListing(recipe_id=recipe.id,
                                        ingredient_id=ean,
                                        ingredient_quantity=ean2quantity[ean])

            success_msg = 'Successfully created recipe #%s: %s.' % (recipe.id, recipe.name)
            return render(
                    request, 'recipemanager/recipe_create.html', {'success': success_msg})
