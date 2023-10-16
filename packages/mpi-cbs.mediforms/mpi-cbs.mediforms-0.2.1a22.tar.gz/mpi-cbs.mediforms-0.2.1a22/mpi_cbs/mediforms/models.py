import re
import string
import unicodedata
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


def sanitize_string(_string):
    # replace umlauts
    _string = re.sub('[ä]', 'ae', _string)
    _string = re.sub('[Ä]', 'Ae', _string)
    _string = re.sub('[ö]', 'oe', _string)
    _string = re.sub('[Ö]', 'Oe', _string)
    _string = re.sub('[ü]', 'ue', _string)
    _string = re.sub('[Ü]', 'Ue', _string)
    _string = re.sub('[ß]', 'ss', _string)

    # remove accents
    _string = ''.join(c for c in unicodedata.normalize('NFKD', _string)
                      if not unicodedata.combining(c))

    # remove punctuation
    _string = _string.translate(str.maketrans('', '', string.punctuation))

    return _string


class YesNoField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 3
        kwargs['choices'] = (
            ('yes', _('yes')),
            ('no', _('no')),
        )
        super().__init__(*args, **kwargs)


class Method(models.Model):
    key = models.CharField(_('Key'), max_length=16, primary_key=True)
    name = models.CharField(_('Name'), max_length=64)
    color = models.CharField(_('Color'), max_length=8, default='#0070c0')

    def __str__(self):
        return self.name

    class Meta:
        ordering = 'name',


class Token(models.Model):
    id = models.UUIDField(_('ID'), default=uuid4, primary_key=True)
    method = models.ForeignKey(Method, on_delete=models.PROTECT, verbose_name=_('Method'))
    pseudonym = models.CharField(_('Pseudonym'), max_length=64)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                   verbose_name=_('Created by'))

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = '-created_at',
        unique_together = 'method', 'pseudonym'
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'


class PersonalData(models.Model):
    class Gender(models.TextChoices):
        FEMALE = 'f', _('Female')
        MALE = 'm', _('Male')
        DIVERSE = 'd', _('Diverse')

    last_name = models.CharField(_('Last name'), max_length=255)
    first_name = models.CharField(_('First name'), max_length=255)

    height = models.IntegerField(_('Height'), null=True, blank=True)
    weight = models.IntegerField(_('Weight'), null=True, blank=True)

    date_of_birth = models.DateField(_('Date of birth'))
    birthplace = models.CharField(_('Birthplace'), max_length=255, null=True, blank=True)

    gender = models.CharField(_('Gender'), max_length=1, choices=Gender.choices, null=True, blank=True)

    street = models.CharField(_('Street'), max_length=255, null=True, blank=True)
    zip_code = models.CharField(_('Zip code'), max_length=5, null=True, blank=True)
    city = models.CharField(_('City'), max_length=255, null=True, blank=True)

    phone_number = models.CharField(_('Phone number'), max_length=20, null=True, blank=True)
    mobile_number = models.CharField(_('Mobile number'), max_length=20, null=True, blank=True)
    email = models.EmailField(_('E-mail'), blank=True, default='')

    class Meta:
        abstract = True


class QuestionsWomen(models.Model):
    schwanger = YesNoField(_('schwanger'), null=True, blank=True)

    class Meta:
        abstract = True


class QuestionsWomenMRT(QuestionsWomen):
    spirale = YesNoField(_('spirale'), null=True, blank=True)

    class Meta:
        abstract = True


class QuestionsMRT(models.Model):
    fehlsicht = YesNoField(_('fehlsicht'))
    kontaktlinsen = YesNoField(_('kontaktlinsen'))
    brille = YesNoField(_('brille'))
    astigmatismus = YesNoField(_('astigmatismus'))
    klaustrophobie = YesNoField(_('klaustrophobie'))
    geraeusch = YesNoField(_('geraeusch'))
    tinnitus = YesNoField(_('tinnitus'))
    operationen = YesNoField(_('operationen'))
    operationenwelchewann = models.TextField(_('operationenwelchewann'), blank=True, default='')
    metallclips = YesNoField(_('metallclips'))
    metallplatten = YesNoField(_('metallplatten'))
    gelenkprothesen = YesNoField(_('gelenkprothesen'))
    stent = YesNoField(_('stent'))
    herzschrittmacher = YesNoField(_('herzschrittmacher'))
    herzklappen = YesNoField(_('herzklappen'))
    innenohrimplantate = YesNoField(_('innenohrimplantate'))
    shunt = YesNoField(_('shunt'))
    hirnschrittmacher = YesNoField(_('hirnschrittmacher'))
    medikamentenpumpe = YesNoField(_('medikamentenpumpe'))
    metallsplitter = YesNoField(_('metallsplitter'))
    metalljob = YesNoField(_('metalljob'))
    metalleintrag = YesNoField(_('metalleintrag'))
    metallteile = YesNoField(_('metallteile'))
    metallteilewas = models.TextField(_('metallteilewas'), blank=True, default='')
    tattoos = YesNoField(_('tattoos'))
    tattoosort = models.TextField(_('tattoosort'), blank=True, default='')
    nikotinpflaster = YesNoField(_('nikotinpflaster'))
    rueckenlage = YesNoField(_('rueckenlage'))
    medikamente = YesNoField(_('medikamente'))
    medikamentewelche = models.TextField(_('medikamentewelche'), blank=True, default='')
    neuro = YesNoField(_('neuro'))
    neurowelche = models.TextField(_('neurowelche'), blank=True, default='')
    kopfverletzung = YesNoField(_('kopfverletzung'))
    kopfwelche = models.TextField(_('kopfwelche'), blank=True, default='')
    epilepsie = YesNoField(_('epilepsie'))
    herzrhythmus = YesNoField(_('herzrhythmus'))
    herzkrank = YesNoField(_('herzkrank'))
    durchblutung = YesNoField(_('durchblutung'))
    atemwege = YesNoField(_('atemwege'))
    allergie = YesNoField(_('allergie'))
    allergiewelche = models.TextField(_('allergiewelche'), blank=True, default='')
    niere = YesNoField(_('niere'))
    mrt12 = YesNoField(_('mrt12'))
    mrtanzahl = models.PositiveIntegerField(_('mrtanzahl'))

    class Meta:
        abstract = True


class QuestionsTMS(models.Model):
    epilepsie = YesNoField(_('epilepsie'))
    fieberkrampf = YesNoField(_('fieberkrampf'))
    familieepilepsie = YesNoField(_('familieepilepsie'))
    bewusstlosigkeit = YesNoField(_('bewusstlosigkeit'))
    kopfschmerzen = YesNoField(_('kopfschmerzen'))
    migraene = YesNoField(_('migraene'))
    schlafstoerung = YesNoField(_('schlafstoerung'))
    drogen = YesNoField(_('drogen'))
    medikamente = YesNoField(_('medikamente'))
    medikamentewelche = models.TextField(_('medikamentewelche'), blank=True, default='')
    neuro = YesNoField(_('neuro'))
    neurowelche = models.TextField(_('neurowelche'), blank=True, default='')
    psycho = YesNoField(_('psycho'))
    psychowelche = models.TextField(_('psychowelche'), blank=True, default='')
    kopfverletzung = YesNoField(_('kopfverletzung'))
    kopfwelche = models.TextField(_('kopfwelche'), blank=True, default='')
    operationen = YesNoField(_('operationen'))
    operationenwelchewann = models.TextField(_('operationenwelchewann'), blank=True, default='')
    metallclips = YesNoField(_('metallclips'))
    metallplatten = YesNoField(_('metallplatten'))
    gelenkprothesen = YesNoField(_('gelenkprothesen'))
    stent = YesNoField(_('stent'))
    herzschrittmacher = YesNoField(_('herzschrittmacher'))
    herzklappen = YesNoField(_('herzklappen'))
    innenohrimplantate = YesNoField(_('innenohrimplantate'))
    shunt = YesNoField(_('shunt'))
    hirnschrittmacher = YesNoField(_('hirnschrittmacher'))
    medikamentenpumpe = YesNoField(_('medikamentenpumpe'))
    metallsplitter = YesNoField(_('metallsplitter'))
    metalljob = YesNoField(_('metalljob'))
    metalleintrag = YesNoField(_('metalleintrag'))
    herzrhythmus = YesNoField(_('herzrhythmus'))
    herzkrank = YesNoField(_('herzkrank'))
    durchblutung = YesNoField(_('durchblutung'))
    atemwege = YesNoField(_('atemwege'))
    hauterkrankungen = YesNoField(_('hauterkrankungen'), null=True)
    narben = YesNoField(_('narben'), null=True)

    class Meta:
        abstract = True


class FormData(models.Model):
    pseudonym = models.CharField(_('Pseudonym'), max_length=64, editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    token_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                         verbose_name=_('Token created by'))

    class Meta:
        abstract = True


class AbstractFormDataMRT(FormData, PersonalData, QuestionsMRT, QuestionsWomenMRT):
    class Meta:
        abstract = True


class FormDataMRT(AbstractFormDataMRT):
    class Meta:
        ordering = 'last_name', 'first_name', 'date_of_birth'
        verbose_name = _('Form data MRT')
        verbose_name_plural = _('Form data MRT')


class FormDataMRTBegleitung(AbstractFormDataMRT):
    class Meta:
        ordering = 'last_name', 'first_name', 'date_of_birth'
        verbose_name = _('Form data MRT Begleitung')
        verbose_name_plural = _('Form data MRT Begleitung')


class FormDataTMS(FormData, PersonalData, QuestionsTMS, QuestionsWomen):
    class Meta:
        ordering = 'last_name', 'first_name', 'date_of_birth'
        verbose_name = _('Form data TMS')
        verbose_name_plural = _('Form data TMS')


class PDF(models.Model):
    def get_upload_path(self, filename):
        pseudonym = sanitize_string(self.form_data.pseudonym)
        return f'consents/{pseudonym}/{filename}'

    file_handle = models.FileField(_('File handle'), upload_to=get_upload_path, max_length=128)

    class Meta:
        abstract = True


class PDFMRT(PDF):
    form_data = models.ForeignKey(FormDataMRT, on_delete=models.CASCADE,
                                  verbose_name=_('Form data MRT'))

    class Meta:
        verbose_name = _('PDF MRT')
        verbose_name_plural = _('PDFs MRT')


class PDFMRTBegleitung(PDF):
    form_data = models.ForeignKey(FormDataMRTBegleitung, on_delete=models.CASCADE,
                                  verbose_name=_('Form data MRT Begleitung'))

    class Meta:
        verbose_name = _('PDF MRT Begleitung')
        verbose_name_plural = _('PDFs MRT Begleitung')


class PDFTMS(PDF):
    form_data = models.ForeignKey(FormDataTMS, on_delete=models.CASCADE,
                                  verbose_name=_('Form data TMS'))

    class Meta:
        verbose_name = _('PDF TMS')
        verbose_name_plural = _('PDFs TMS')
