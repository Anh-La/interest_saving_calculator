from django.urls import path
from . import views

urlpatterns = [
    path('', views.CarLoanIndex.as_view(), name='car_loan_index'),
    path('calculate/', views.calculate_loan, name='calculate_loan'),
]
