from django.contrib import admin
from django.urls import path
from calculator.views import Index, generate_pdf, generate_csv
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('generate-pdf/', generate_pdf, name='generate_pdf'),
    path('generate-csv/', generate_csv, name='generate_csv'),
    #path('data.json', TemplateView.as_view(template_name='data.json', content_type='application/json')),
]
