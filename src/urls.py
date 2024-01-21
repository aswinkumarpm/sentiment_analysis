from django.urls import path
from .views import create_category, category_detail, category_list, add_sentence, download_category_csv

urlpatterns = [
    path('create/', create_category, name='create_category'),
    path('', category_list, name='category_list'),
    path('<int:category_id>/', category_detail, name='category_detail'),
    path('add_sentence/', add_sentence, name='add_sentence'),
    path('download_csv/<str:category_name>/', download_category_csv, name='download_category_csv'),

]