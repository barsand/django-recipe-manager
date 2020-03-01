from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from .models import Ingredient
import collections
import json


def index(request):
    return HttpResponse('aloha!')

def ingredient_list(request):
    return render(request, 'recipemanager/list.html')

def ingredient_create(request):
    if request.method == 'GET':
        return render(request, 'recipemanager/create.html')
    elif request.method == 'POST':
        model_fields = [f.get_attname() for f in Ingredient._meta.get_fields()]
        parsed_form_data = dict()
        for field in request.POST:
            if field in model_fields:
                parsed_form_data[field] = request.POST[field]
        try:
            if len(Ingredient.objects.filter(Q(name=parsed_form_data['name']) |\
                                             Q(ean=parsed_form_data['ean']))):
                return_payload = {
                    'error': 'name and/or ean already taken',
                    'form_data': parsed_form_data
                }
                return render(request, 'recipemanager/create.html', return_payload)

            Ingredient(**parsed_form_data).save()
        except:
            return HttpResponse(status=404)

        return render(
                request, 'recipemanager/create.html', {'success': 'Ingredient created!'})


def ingredient_view(request, ingredient_id):
    return HttpResponse('viewing %s' % ingredient_id)

def ingredient_edit(request, ingredient_id):
    return HttpResponse('editing %s' % ingredient_id)

def ingredient_delete(request, ingredient_id):
    return HttpResponse('deleting %s' % ingredient_id)

