from django import forms

class InvestmentForm(forms.Form):
	starting_amount = forms.FloatField(
		widget=forms.NumberInput(attrs={'id': 'starting_amount'})
	)
	starting_amount_range =forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'type': 'range', 
            'min': '0', 
            'max': '1000000', 
            'class': 'form-range',  # Bootstrap 5 class for range input
			'id': 'starting_amount_range'
        })
    )

	number_of_years = forms.FloatField(
		widget=forms.NumberInput(attrs={'id': 'number_of_years'})
	)
	number_of_years_range =forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'type': 'range', 
            'min': '0', 
            'max': '1000', 
            'class': 'form-range',  # Bootstrap 5 class for range input
			'id': 'number_of_years_range'
        })
    )

	return_rate = forms.FloatField(
		widget=forms.NumberInput(attrs={'id': 'return_rate'})
	)
	return_rate_range =forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'type': 'range', 
            'min': '0', 
            'max': '100', 
            'class': 'form-range',  # Bootstrap 5 class for range input
			'id': 'return_rate_range'
        })
    )

	annual_additional_contribution = forms.FloatField(
		widget=forms.NumberInput(attrs={'id': 'annual_additional_contribution'})
	)
	annual_additional_contribution_range =forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'type': 'range', 
            'min': '0', 
            'max': '100000', 
            'class': 'form-range',  # Bootstrap 5 class for range input
			'id': 'annual_additional_contribution_range'
        })
    )
