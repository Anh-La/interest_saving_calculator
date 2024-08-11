from django.contrib import admin
from django.urls import path, include
from calculator.views import Index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('calculator/', include('calculator.urls')),  # Include calculator app URLs
    path('car_loan/', include('car_loan.urls'))  # Include car_loan app URLs
]
