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

def parse_ingredient_form_data(request, model):
    model_fields = [f.attname for f in model._meta.fields]
    parsed_form_data = dict()
    for field in request.POST:
        if field in model_fields:
            parsed_form_data[field] = request.POST[field]
    return parsed_form_data

def render_homepage(request):
    return render(request, 'recipemanager/home.html')


class IngredientManager():
    def list(request):
        ingredients = Ingredient.objects.all()
        return render(request, 'recipemanager/ingredient_list.html', {'ingredients': ingredients})

    def create(request):
        if request.method == 'GET':
            return render(request, 'recipemanager/ingredient_create.html')
        elif request.method == 'POST':
            parsed_form_data = parse_ingredient_form_data(request, Ingredient)
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
            parsed_form_data = parse_ingredient_form_data(request, Ingredient)
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

    def confirm_delete(request, ingredient_id):
        ingredient = Ingredient.objects.filter(ean=ingredient_id)[0]
        listings = RecipeListing.objects.filter(ingredient=ingredient)
        return render(request, 'recipemanager/ingredient_confirm_delete.html',
                {'ingredient': ingredient, 'listings': listings})

    def delete(request, ingredient_id):
        ingredient = Ingredient.objects.filter(ean=ingredient_id)[0]
        listings = RecipeListing.objects.filter(ingredient=ingredient)
        for l in listings:
            l.recipe.cost -= l.ingredient_quantity / l.ingredient.amount * l.ingredient.price
            l.recipe.save()
            l.delete()
        try:
            ingredient.delete()
            return render(request, 'recipemanager/ingredient_delete.html', {
                'success': 'Sucessfully deleted ingredient #%s.' % ingredient_id})
        except Exception as exp:
            return render(request, 'recipemanager/ingredient_delete.html')

def form2structured_data(posted_data):
    recipe_eans = list()
    for field in posted_data:
        if field[:20] == 'ingredient-selected-':
            recipe_eans.append(field[20:])

    recipe_ingredients = list()
    ean2quantity = dict()
    recipe_cost = 0
    for ean in recipe_eans:
        ingredient = Ingredient.objects.filter(ean=ean)[0]
        recipe_ingredients.append(ingredient)
        curr_quantity = float(posted_data['%s-item-quantity' % ean])
        ean2quantity[ean] = curr_quantity
        recipe_cost += curr_quantity/float(ingredient.amount)*float(ingredient.price)

    return {
        'recipe_ingredients': recipe_ingredients,
        'recipe_cost': recipe_cost,
        'ean2quantity': ean2quantity
    }

class RecipeManager():
    def list(request):
        recipes = Recipe.objects.all()
        return render(request, 'recipemanager/recipe_list.html', {'recipes': recipes})

    def create(request):
        if request.method == 'GET':
            ingredients = Ingredient.objects.all()
            return render(request, 'recipemanager/recipe_create.html', {'ingredients': ingredients})
        if request.method == 'POST':
            data = form2structured_data(request.POST)

            recipe = Recipe(name=request.POST['name'], cost=data['recipe_cost'])
            recipe.save()

            for ingredient in data['recipe_ingredients']:
                listing = RecipeListing(recipe=recipe,
                                        ingredient=ingredient,
                                        ingredient_quantity=data['ean2quantity'][ingredient.ean])
                listing.save()

            success_msg = 'Successfully created recipe #%s: %s.' % (recipe.id, recipe.name)
            return render(
                    request, 'recipemanager/recipe_create.html', {'success': success_msg})

    def view(request, recipe_id):
        recipe = Recipe.objects.filter(id=recipe_id)[0]
        listings = RecipeListing.objects.filter(recipe=recipe)
        for l in listings:
            l.unit_cost = l.ingredient_quantity / l.ingredient.amount * l.ingredient.price
        return render(request, 'recipemanager/recipe_view.html',
                      {'recipe': recipe, 'listings': listings})

    def edit(request, recipe_id):
        if request.method == 'GET':
            recipe = Recipe.objects.filter(id=recipe_id)[0]
            listings  = {
                l.ingredient.ean: l.ingredient_quantity
                for l in RecipeListing.objects.filter(recipe=recipe)
            }
            ingredients = Ingredient.objects.all()
            for i in ingredients:
                if i.ean in listings:
                    i.curr_recipe_quantity = listings[i.ean]
            payload =  {
                'form_data': recipe,
                'listings': listings,
                'ingredients': ingredients
            }
            return render(request, 'recipemanager/recipe_edit.html', payload)

        elif request.method == 'POST':
            data = form2structured_data(request.POST)
            ean2form_data = {i.ean: i for i in data['recipe_ingredients']}
            recipe = Recipe.objects.filter(id=recipe_id)[0]
            listings = RecipeListing.objects.filter(recipe=recipe)
            ean2listings = {l.ingredient.ean: l for l in listings}

            for ean in set(list(ean2form_data.keys()) + list(ean2listings.keys())):
                if ean in ean2form_data and ean in ean2listings:
                    form_quantity = data['ean2quantity'][ean]
                    db_quantity = ean2listings[ean].ingredient_quantity
                    if form_quantity != db_quantity:
                        ean2listings[ean].ingredient_quantity = form_quantity
                        ean2listings[ean].save()
                if ean in ean2form_data and ean not in ean2listings:
                    new_listing = RecipeListing(recipe=recipe,
                                        ingredient=ean2form_data[ean],
                                        ingredient_quantity=data['ean2quantity'][ean])
                    new_listing.save()
                if ean not in ean2form_data and ean in ean2listings:
                    ean2listings[ean].delete()
        msg = {'success': 'Sucessfully updated recipe #%s: %s.' % (recipe_id, recipe.name)}
        return render(request, 'recipemanager/recipe_edit.html', msg)

    def delete(request, recipe_id):
        recipe = Recipe.objects.filter(id=recipe_id)[0]
        for l in RecipeListing.objects.filter(recipe=recipe):
            l.delete()
        recipe.delete()
        msg = {'success': 'Sucessfully deleted recipe #%s: %s.' % (recipe_id, recipe.name)}
        return render(request, 'recipemanager/recipe_edit.html', msg)




