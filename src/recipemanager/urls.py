from django.urls import path

from . import views

app_name = 'recipemanager'

urlpatterns = [
    path('', views.index, name='index'),
    path('ingredient/', views.ingredient_list, name='ingredient_list'),
    path('ingredient/list/', views.ingredient_list, name='ingredient_list'),
    path('ingredient/create/', views.ingredient_create, name='ingredient_create'),
    path('ingredient/<str:ingredient_id>/view/', views.ingredient_view,
         name='ingredient_view'),
    path('ingredient/<str:ingredient_id>/edit/', views.ingredient_edit,
         name='ingredient_edit'),
    path('ingredient/<str:ingredient_id>/delete/', views.ingredient_delete,
         name='ingredient_delete'),

    path('recipe/list/', views.recipe_list, name='recipe_list'),
    path('recipe/create/', views.recipe_create, name='recipe_create'),
]
