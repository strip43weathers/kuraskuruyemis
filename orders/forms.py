# orders/forms.py

from django import forms

class OrderExportForm(forms.Form):
    # 'datetime-local' tipi tarayıcıda takvim ve saat seçiciyi otomatik açar
    start_date = forms.DateTimeField(
        label="Başlangıç Tarihi ve Saati",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    end_date = forms.DateTimeField(
        label="Bitiş Tarihi ve Saati",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
