from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from mpi_cbs.mediforms.models import FormDataMRT, FormDataMRTBegleitung, FormDataTMS, Token
from mpi_cbs.mediforms.widgets import RadioSelect


class TokenForm(forms.ModelForm):
    class Meta:
        model = Token
        fields = 'method', 'pseudonym'
        help_texts = {
            'pseudonym': '(ID aus der Probandendatenbank)',
        }


class PersonalDataForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,
                                    label=_('Date of birth'),
                                    widget=forms.TextInput(attrs={'placeholder': _('DD/MM/YYYY')}))

    class Meta:
        model = FormDataMRT
        fields = (
            'last_name', 'first_name',
            'height', 'weight',
            'date_of_birth', 'birthplace',
            'gender',
            'street', 'zip_code', 'city',
            'phone_number', 'mobile_number', 'email',
        )
        widgets = {
            'height': forms.NumberInput(attrs={'placeholder': _('Height in cm')}),
            'street': forms.TextInput(attrs={'placeholder': _('Street and house number')}),
            'weight': forms.NumberInput(attrs={'placeholder': _('Weight in kg')}),
        }


class QuestionsMRTForm(forms.ModelForm):
    class Meta:
        model = FormDataMRT
        exclude = (
            'token_created_by',
            'last_name', 'first_name',
            'height', 'weight',
            'date_of_birth', 'birthplace',
            'gender',
            'street', 'zip_code', 'city',
            'phone_number', 'mobile_number', 'email',
            'schwanger', 'spirale',
        )
        widgets = {
            'fehlsicht': RadioSelect(attrs={'class': 'choices'}),
            'kontaktlinsen': RadioSelect(attrs={'class': 'choices'}),
            'brille': RadioSelect(attrs={'class': 'choices'}),
            'astigmatismus': RadioSelect(attrs={'class': 'choices'}),
            'klaustrophobie': RadioSelect(attrs={'class': 'choices'}),
            'geraeusch': RadioSelect(attrs={'class': 'choices'}),
            'tinnitus': RadioSelect(attrs={'class': 'choices'}),
            'operationen': RadioSelect(attrs={'class': 'choices'}),
            'metallclips': RadioSelect(attrs={'class': 'choices'}),
            'metallplatten': RadioSelect(attrs={'class': 'choices'}),
            'gelenkprothesen': RadioSelect(attrs={'class': 'choices'}),
            'stent': RadioSelect(attrs={'class': 'choices'}),
            'herzschrittmacher': RadioSelect(attrs={'class': 'choices'}),
            'herzklappen': RadioSelect(attrs={'class': 'choices'}),
            'innenohrimplantate': RadioSelect(attrs={'class': 'choices'}),
            'shunt': RadioSelect(attrs={'class': 'choices'}),
            'hirnschrittmacher': RadioSelect(attrs={'class': 'choices'}),
            'medikamentenpumpe': RadioSelect(attrs={'class': 'choices'}),
            'metallsplitter': RadioSelect(attrs={'class': 'choices'}),
            'metalljob': RadioSelect(attrs={'class': 'choices'}),
            'metalleintrag': RadioSelect(attrs={'class': 'choices'}),
            'metallteile': RadioSelect(attrs={'class': 'choices'}),
            'tattoos': RadioSelect(attrs={'class': 'choices'}),
            'nikotinpflaster': RadioSelect(attrs={'class': 'choices'}),
            'rueckenlage': RadioSelect(attrs={'class': 'choices'}),
            'medikamente': RadioSelect(attrs={'class': 'choices'}),
            'neuro': RadioSelect(attrs={'class': 'choices'}),
            'kopfverletzung': RadioSelect(attrs={'class': 'choices'}),
            'epilepsie': RadioSelect(attrs={'class': 'choices'}),
            'herzrhythmus': RadioSelect(attrs={'class': 'choices'}),
            'herzkrank': RadioSelect(attrs={'class': 'choices'}),
            'durchblutung': RadioSelect(attrs={'class': 'choices'}),
            'atemwege': RadioSelect(attrs={'class': 'choices'}),
            'allergie': RadioSelect(attrs={'class': 'choices'}),
            'niere': RadioSelect(attrs={'class': 'choices'}),
            'mrt12': RadioSelect(attrs={'class': 'choices'}),
        }


class QuestionsTMSForm(forms.ModelForm):
    class Meta:
        model = FormDataTMS
        exclude = (
            'token_created_by',
            'last_name', 'first_name',
            'height', 'weight',
            'date_of_birth', 'birthplace',
            'gender',
            'street', 'zip_code', 'city',
            'phone_number', 'mobile_number', 'email',
            'schwanger',
        )
        widgets = {
            'epilepsie': RadioSelect(attrs={'class': 'choices'}),
            'fieberkrampf': RadioSelect(attrs={'class': 'choices'}),
            'familieepilepsie': RadioSelect(attrs={'class': 'choices'}),
            'bewusstlosigkeit': RadioSelect(attrs={'class': 'choices'}),
            'kopfschmerzen': RadioSelect(attrs={'class': 'choices'}),
            'migraene': RadioSelect(attrs={'class': 'choices'}),
            'schlafstoerung': RadioSelect(attrs={'class': 'choices'}),
            'drogen': RadioSelect(attrs={'class': 'choices'}),
            'medikamente': RadioSelect(attrs={'class': 'choices'}),
            'neuro': RadioSelect(attrs={'class': 'choices'}),
            'psycho': RadioSelect(attrs={'class': 'choices'}),
            'kopfverletzung': RadioSelect(attrs={'class': 'choices'}),
            'operationen': RadioSelect(attrs={'class': 'choices'}),
            'metallclips': RadioSelect(attrs={'class': 'choices'}),
            'metallplatten': RadioSelect(attrs={'class': 'choices'}),
            'gelenkprothesen': RadioSelect(attrs={'class': 'choices'}),
            'stent': RadioSelect(attrs={'class': 'choices'}),
            'herzschrittmacher': RadioSelect(attrs={'class': 'choices'}),
            'herzklappen': RadioSelect(attrs={'class': 'choices'}),
            'innenohrimplantate': RadioSelect(attrs={'class': 'choices'}),
            'shunt': RadioSelect(attrs={'class': 'choices'}),
            'hirnschrittmacher': RadioSelect(attrs={'class': 'choices'}),
            'medikamentenpumpe': RadioSelect(attrs={'class': 'choices'}),
            'metallsplitter': RadioSelect(attrs={'class': 'choices'}),
            'metalljob': RadioSelect(attrs={'class': 'choices'}),
            'metalleintrag': RadioSelect(attrs={'class': 'choices'}),
            'herzrhythmus': RadioSelect(attrs={'class': 'choices'}),
            'herzkrank': RadioSelect(attrs={'class': 'choices'}),
            'durchblutung': RadioSelect(attrs={'class': 'choices'}),
            'atemwege': RadioSelect(attrs={'class': 'choices'}),
            'hauterkrankungen': RadioSelect(attrs={'class': 'choices'}),
            'narben': RadioSelect(attrs={'class': 'choices'}),
        }


class QuestionsWomenForm(forms.ModelForm):
    class Meta:
        model = FormDataMRT
        fields = 'schwanger',
        widgets = {
            'schwanger': RadioSelect(attrs={'class': 'choices'}),
        }


class QuestionsWomenMRTForm(forms.ModelForm):
    class Meta:
        model = FormDataMRT
        fields = 'schwanger', 'spirale'
        widgets = {
            'schwanger': RadioSelect(attrs={'class': 'choices'}),
            'spirale': RadioSelect(attrs={'class': 'choices'}),
        }


class ConsentAgreementForm(forms.Form):
    agreement_participation = forms.BooleanField()
    agreement_consents = forms.BooleanField()


class MRTForm(forms.ModelForm):
    class Meta:
        model = FormDataMRT
        exclude = 'token_created_by',


class MRTBegleitungForm(forms.ModelForm):
    class Meta:
        model = FormDataMRTBegleitung
        exclude = 'token_created_by',


class TMSForm(forms.ModelForm):
    class Meta:
        model = FormDataTMS
        exclude = 'token_created_by',
