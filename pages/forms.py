from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class MealPlanGenerate(forms.Form):
    startdate = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
    enddate = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))