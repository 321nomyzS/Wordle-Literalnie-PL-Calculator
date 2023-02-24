from django.urls import path
from . import views


urlpatterns = [
    path('', views.literalnie, name='literalnie'),
    path('instruction', views.literalnie_instruction, name='instruction'),
    path('delete/<word>', views.literalnie_delete_word, name='delete'),
    path('add/', views.literalnie_add_word, name='add'),
    path('add/<word>', views.literalnie_add_word, name='add')
]
