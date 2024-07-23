import json
import csv
import os
from django.conf import settings
from django.shortcuts import render
from django.views import View
from .forms import InvestmentForm

## Library for generate pdf and csv file functions
from django.http import HttpResponse, JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import datetime

## library for convert markdown to html
import markdown

def read_markdown_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()

def convert_markdown_to_html(markdown_content):
    return markdown.markdown(markdown_content)

class Index(View):
    def get(self, request):
        form = InvestmentForm()
        
        # Get the absolute path to the README.md file
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        readme_path = os.path.join(project_root, 'README.md')
        markdown_content = read_markdown_file(readme_path)
        html_content = convert_markdown_to_html(markdown_content)

        context = {
            'form': form,
            'html_content': html_content
        }

        return render(request, 'calculator/index.html', context)

    def post(self, request):
        form = InvestmentForm(request.POST)

        # Get the absolute path to the README.md file
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        readme_path = os.path.join(project_root, 'README.md')
        markdown_content = read_markdown_file(readme_path)
        html_content = convert_markdown_to_html(markdown_content)

        if form.is_valid():
            # Set up default values
            number_of_years =form.cleaned_data['number_of_years']
            initial_deposit = form.cleaned_data['starting_amount']
            intereset_rate = form.cleaned_data['return_rate'] / 100
            total_deposit = initial_deposit
            total_result = total_deposit
            total_interest = 0
            total_additional_contribution = form.cleaned_data['annual_additional_contribution']
            yearly_results = {}  # range    

            for i in range(1, int(number_of_years + 1)):
                yearly_results[i] = {}

                # Calculate the interest
                interest_on_deposit = total_deposit * intereset_rate
                interest = total_result * intereset_rate  # Multiply the original investment with the required rate of return in percentage
                total_result += interest  # Add the newly calculated interest amount to the accumulated investment
                total_interest += interest  # Add the newly calculated interest amount to the accumulated interest

                # Add additional contribution
                total_deposit += total_additional_contribution
                total_result += total_additional_contribution

                # Set yearly_results
                yearly_results[i]['deposit'] = round(total_deposit+interest_on_deposit, 2)  # Round the figures to 2 decimals only
                yearly_results[i]['principle_interest'] = round(interest_on_deposit, 2)  # Round the figures to 2 decimals only
                yearly_results[i]['compound_interest'] = round(total_interest-interest_on_deposit, 2)  # Round the figures to 2 decimals only
                yearly_results[i]['interest'] = round(total_interest, 2)  # Round the figures to 2 decimals only
                yearly_results[i]['total'] = round(total_result, 2)  # Round the figures to 2 decimals only

                # Set data for JSON file
                data = {
                    # Input
                    'number_of_years': int(form.cleaned_data['number_of_years']),
                    'rate_of_return': float(form.cleaned_data['return_rate']),
                    'original_investment': float(form.cleaned_data['starting_amount']),
                    'additional_investment': float(form.cleaned_data['annual_additional_contribution']),
                    'total_interest': round(total_result-total_deposit, 2),
                    'total_deposit': float(form.cleaned_data['starting_amount']) + (float(form.cleaned_data['annual_additional_contribution'])*int(form.cleaned_data['number_of_years'])),
                    # Output 
                    'total_result': round(total_result, 2),
                    'interest': yearly_results,  # Outcomes from loop function
                }

                # Save data to session
                request.session['investment_data'] = data

                # Convert data to JSON
                json_data = json.dumps(data)    

                # Save JSON to a file
                with open('static/data.json', 'w') as json_file:
                    json_file.write(json_data)

                # Create context
                context = {
                    # README content
                    'html_content': html_content,
                    # input
                    'total_deposit': round(total_deposit+(interest_on_deposit*number_of_years),2),
                    'total_result': round(total_result, 2), 
                    'yearly_results': yearly_results,
                    'number_of_years': int(form.cleaned_data['number_of_years']),
                    'rate_of_return': float(form.cleaned_data['return_rate']),
                    'original_investment': float(form.cleaned_data['starting_amount']),
                    'additional_investment': float(form.cleaned_data['annual_additional_contribution']),
                    'total_additional_deposit':float(form.cleaned_data['annual_additional_contribution'])*int(form.cleaned_data['number_of_years']),
                    'form': form,
                    'total_interest': round(total_result-total_deposit, 2),
                    'interest_on_deposit':round(interest_on_deposit,2),
                    'total_interest_on_deposit':round(interest_on_deposit*number_of_years,2)
                }

            # Render the template
            return render(request, 'calculator/index.html', context)
        else:

            context = {
                'form': form,
                'html_content': html_content
            }

            return render(request, 'calculator/index.html', context)
        
def generate_pdf(request):
    # Read JSON data from a file
    json_file_path = os.path.join(settings.BASE_DIR, 'static', 'data.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Get the README content
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    readme_path = os.path.join(project_root, 'README.md')
    markdown_content = read_markdown_file(readme_path)
    html_content = convert_markdown_to_html(markdown_content)

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

    # Add Summary input
    story.append(Paragraph(f"Year: {data['number_of_years']}", normal_style))
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
    table_data = [['number_of_years', 'Interest', 'Total']]
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

    # Add general information
    story.append(Paragraph(f"General information: {html_content}", normal_style))
    story.append(Spacer(1, 12))
	
    # Build the PDF document with the defined story using the custom canvas
    doc.build(story)

    return response

def create_bar_chart(data):
    drawing = Drawing(400, 200)
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 300

    # Add data to the bar chart
    bc.data = [list(data['interest'][str(year)]['interest'] for year in range(1, data['number_of_years'] + 1))]
    bc.categoryAxis.categoryNames = [str(year) for year in range(1, data['number_of_years'] + 1)]

    # Set the value axis properties
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = max(bc.data[0]) * 1.1
    bc.valueAxis.valueStep = max(bc.data[0]) / 5

    # Change the color of the bars to green
    bc.bars.fillColor = colors.green

    drawing.add(bc)
    return drawing

def generate_csv(request):
    # Read JSON data from a file
    json_file_path = os.path.join(settings.BASE_DIR, 'static', 'data.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="interest_data.csv"'},
    )

    writer = csv.writer(response)

    # Write headers
    headers = ["Year", "Interest", "Total"]
    writer.writerow(headers)
    
    # Write data rows
    for year, values in data["interest"].items():
        writer.writerow([year, values["interest"], values["total"]])

    return response

