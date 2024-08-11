from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='calculator_index'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('generate-csv/', views.generate_csv, name='generate_csv'),
    path('save-json/', views.save_json, name='save_json')
]
