import json
import os
from django.shortcuts import render
from django.views import View
from .forms import InvestmentForm

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageTemplate
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import datetime

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
                'total_result': round(total_result, 2),
                'interest': yearly_results,
                'year': int(form.cleaned_data['number_of_years']),
                'rate_of_return': float(form.cleaned_data['return_rate']),
                'original_investment': float(form.cleaned_data['starting_amount']),
                'additional_investment': float(form.cleaned_data['annual_additional_contribution']),
            }

				# Convert data to JSON
				json_data = json.dumps(data)	

				# Save JSON to a file
				with open('calculator/data.json', 'w') as json_file:
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

class NumberedPageCanvas(canvas.Canvas):
    """
    Custom canvas to add page numbers to PDF.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        """
        On a page break, add information to the list.
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """
        Add the page number to each page (page x of y).
        """
        page_count = len(self.pages)

        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            super().showPage()

        super().save()

    def draw_page_number(self, page_count):
        """
        Add the page number.
        """
        page = "Page %s of %s" % (self._pageNumber, page_count)
        self.setFont("Helvetica", 9)
        self.drawRightString(179 * mm, -280 * mm, page)
        
def generate_pdf(request):
    # Read JSON data from a file
    json_file_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Create a HttpResponse object and set the appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # Create the PDF object, using the response object as its "file."
    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=72,leftMargin=72,topMargin=72,bottomMargin=18)
    
    # Set up styles
    styles = getSampleStyleSheet()
    
    # Define title style
    title_style = ParagraphStyle(
        'title',
        parent=styles['Heading1'],
        alignment=1,  # Center alignment
        spaceAfter=20  # Space after the title
    )

    subtitle_style = styles['Heading2']
    normal_style = styles['BodyText']

    # Create story for the PDF
    story = []
	
	# date and time
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    story.append(Paragraph(f"Generated on: {date_time}", normal_style))

    # Add title
    story.append(Paragraph("Saving Report", title_style))
    story.append(Spacer(1, 12))

    # Add general information
    story.append(Paragraph(f"Year: {data['year']}", normal_style))
    story.append(Paragraph(f"Rate of Return: {data['rate_of_return']}%", normal_style))
    story.append(Paragraph(f"Original Investment: ${data['original_investment']:,.2f}", normal_style))
    story.append(Paragraph(f"Additional Investment: ${data['additional_investment']:,.2f}", normal_style))
    story.append(Paragraph(f"Total Result: ${data['total_result']:,.2f}", normal_style))
    story.append(Spacer(1, 12))

    # Add the bar chart
    story.append(Paragraph("Interest Over the Years", subtitle_style))
    story.append(create_bar_chart(data))

    # Add interest details as a table
    story.append(Paragraph("Interest Details", subtitle_style))
    table_data = [['Year', 'Interest', 'Total']]
    for year, details in data['interest'].items():
        table_data.append([year, f"${details['interest']:,.2f}", f"${details['total']:,.2f}"])

    # Calculate the width of each column to match the width of the page
    table_width = doc.width
    num_columns = len(table_data[0])
    column_width = table_width / num_columns
    col_widths = [column_width] * num_columns

    table = Table(table_data, colWidths=col_widths)
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
		('ALIGN', (0, 1), (-1, -1), 'RIGHT'),  # Right-align the data rows
		('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    story.append(table)
	
    # Build the PDF document with the defined story using the custom canvas
    doc.build(story, canvasmaker=NumberedPageCanvas)

    return response

def create_bar_chart(data):
    drawing = Drawing(400, 200)
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 300

    # Add data to the bar chart
    bc.data = [list(data['interest'][str(year)]['interest'] for year in range(1, data['year'] + 1))]
    bc.categoryAxis.categoryNames = [str(year) for year in range(1, data['year'] + 1)]

    # Set the value axis properties
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = max(bc.data[0]) * 1.1
    bc.valueAxis.valueStep = max(bc.data[0]) / 5

    # Change the color of the bars to green
    bc.bars.fillColor = colors.green

    drawing.add(bc)
    return drawing
