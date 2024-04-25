import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .forms import InvestmentForm

class Index(View):
	def get(self, request):
		form = InvestmentForm()
		return render(request, 'calculator/index.html', {'form': form})

	def post(self, request):
		form = InvestmentForm(request.POST)

		if form.is_valid():
			# set up default values
			total_result = form.cleaned_data['starting_amount']
			total_interest = 0
			yearly_results = {} #range

			for i in range(1, int(form.cleaned_data['number_of_years'] + 1)):
				yearly_results[i] = {}

				# calculate the interest
				interest = total_result * (form.cleaned_data['return_rate'] / 100) # multiple the original investment with the required rate of return in percentage
				total_result += interest # add the newly calculated interest amount to the accumulated investment
				total_interest += interest # add the newly calculated interest amount to the accumulated interest

				# add additional contribution
				total_result += form.cleaned_data['annual_additional_contribution']

				# set yearly_results
				yearly_results[i]['interest'] = round(total_interest, 2) #round the figures to 2 decimals only
				yearly_results[i]['total'] = round(total_result, 2) #round the figures to 2 decimals only

				# create context
				context = {
					'total_result': round(total_result, 2), 
					'yearly_results': yearly_results,
					'number_of_years': int(form.cleaned_data['number_of_years']),
					'rate_of_return': float(form.cleaned_data['return_rate']),
					'original_investment': float(form.cleaned_data['starting_amount']),
					'additional_investment': float(form.cleaned_data['annual_additional_contribution']),
					'form':form
				}

			# render the template
			return render(request, 'calculator/index.html', context)
		
