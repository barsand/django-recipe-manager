from django.http import HttpResponse


def index(request):
    return HttpResponse('aloha!')

def ingredient_list(request):
    return HttpResponse('list!')

def ingredient_create(request):
    return HttpResponse('creating!')

def ingredient_view(request, ingredient_id):
    return HttpResponse('viewing %s' % ingredient_id)

def ingredient_edit(request, ingredient_id):
    return HttpResponse('editing %s' % ingredient_id)

def ingredient_delete(request, ingredient_id):
    return HttpResponse('deleting %s' % ingredient_id)

