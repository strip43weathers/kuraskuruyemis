from django import forms

class OrderExportForm(forms.Form):
    start_date = forms.DateTimeField(
        label="Başlangıç Tarihi ve Saati",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    end_date = forms.DateTimeField(
        label="Bitiş Tarihi ve Saati",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
