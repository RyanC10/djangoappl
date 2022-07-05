from django import forms
from django.template.defaultfilters import mark_safe
from datetime import datetime




class Raspon(forms.Form):
    import datetime
    from django.forms.widgets import SplitDateTimeWidget
    
 
    izaberite_početni_datum = forms.DateField(widget=forms.widgets.DateInput(format=('%Y%m%d'),attrs={'type': 'date'}), label=mark_safe('<strong>Početni datum</strong>'), help_text="Unesite datum za početnu točku vremenskog raspona mjerenja.")
    izaberite_završni_datum = forms.DateField(widget=forms.widgets.DateInput(format=('%Y%m%d'),attrs={'type': 'date'}), label=mark_safe('<strong>Završni datum</strong>'), help_text="Unesite datum za krajnju točku vremenskog raspona mjerenja.")


class igraci(forms.Form):
    ime = forms.CharField(initial='',max_length=20)
    sezona = forms.CharField()

    
