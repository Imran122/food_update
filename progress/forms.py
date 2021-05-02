from django import forms

class DownloadForm(forms.Form):
    startdate = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
    enddate = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))