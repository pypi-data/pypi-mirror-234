from django import forms


class RadioSelect(forms.RadioSelect):
    template_name = 'mediforms/widgets/radio_select.html'
