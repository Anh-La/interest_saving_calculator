import json
from django.shortcuts import render
from django.views import View
from .forms import InvestmentForm

import io
from django.http import FileResponse, JsonResponse
from reportlab.pdfgen import canvas

class Index(View):
	def get(self, request):
		form = InvestmentForm()
		return render(request, 'calculator/index.html', {'form': form})

	def post(self, request):
		form = InvestmentForm(request.POST)
		labels =[]
		data1 =[]
		data2 =[]
		data3 = float
		data4 = float

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

				# add to dataset for charts
				labels.append(i)
				data1.append(total_interest)
				data2.append(total_result)		
				data4 = float(form.cleaned_data['starting_amount']) + float(form.cleaned_data['annual_additional_contribution'])
				data3 = float(total_result)- data4
				data = {
                'year': labels,
                'interest': data1,
				'total_saving': data2,
            	}

				# Convert data to JSON
				json_data = json.dumps(data)	

				# Save JSON to a file
				with open('static/data.json', 'w') as json_file:
					json_file.write(json_data)

				# create context
				context = {
					'total_result': round(total_result, 2), 
					'yearly_results': yearly_results,
					'number_of_years': int(form.cleaned_data['number_of_years']),
					'rate_of_return': float(form.cleaned_data['return_rate']),
					'original_investment': float(form.cleaned_data['starting_amount']),
					'additional_investment': float(form.cleaned_data['annual_additional_contribution']),
					'form':form,
					'labels':json.dumps(labels),
					'data1':json.dumps(data1),
					'data2':json.dumps(data2),
					'data3':json.dumps(round(data3,2)),
					'data4':json.dumps(data4)

				}

			# render the template
			return render(request, 'calculator/index.html', context)

def generate_pdf(request):
    response = FileResponse(generate_pdf_file(), 
                            as_attachment=True, 
                            filename='Your Saving Statement.pdf')
    return response
		
def generate_pdf_file():
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return buffer
