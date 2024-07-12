from django import forms

class InvestmentForm(forms.Form):

    # 1a-Deposit field
    starting_amount = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'id': 'starting_amount',
        })
    )
    # 1b-Deposit Range
    starting_amount_range = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': '0',
            'max': '1000000',
            'class': 'form-range',
            'id': 'starting_amount_range'
        })
    )
    # 2a-Year field
    number_of_years = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'id': 'number_of_years',
        })
    )
    # 2b-Year Range
    number_of_years_range = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': '0',
            'max': '1000',
            'class': 'form-range',
            'id': 'number_of_years_range'
        })
    )
    # 3-Expected return rate field
    return_rate = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'id': 'return_rate',
        })
    )

    # 4a-Additional deposit field
    annual_additional_contribution = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'id': 'annual_additional_contribution',
        })
    )
    # 4b-Additional deposit range
    annual_additional_contribution_range = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': '0',
            'max': '100000',
            'class': 'form-range',
            'id': 'annual_additional_contribution_range'
        })
    )
