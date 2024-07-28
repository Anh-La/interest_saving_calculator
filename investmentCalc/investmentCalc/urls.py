from django.contrib import admin
from django.urls import path
from calculator.views import Index, generate_pdf, generate_csv,save_json

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('save-json/', save_json, name='save_json'),
    path('generate-pdf/', generate_pdf, name='generate_pdf'),
    path('generate-csv/', generate_csv, name='generate_csv')
]
