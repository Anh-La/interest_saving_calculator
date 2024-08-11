from django.shortcuts import render
from django.views.generic import TemplateView

class CarLoanIndex(TemplateView):
    template_name = 'car_loan/index.html'

def calculate_loan(request):
    # Logic to calculate car loan
    return render(request, 'index.html')
