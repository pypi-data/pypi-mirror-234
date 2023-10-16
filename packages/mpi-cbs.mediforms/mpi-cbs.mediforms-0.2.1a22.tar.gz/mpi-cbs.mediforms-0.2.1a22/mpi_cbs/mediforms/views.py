from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.utils.http import urlencode
from django.views import generic
from weasyprint import HTML

from mpi_cbs.mediforms.forms import (ConsentAgreementForm,
                                     MRTForm, MRTBegleitungForm, PersonalDataForm,
                                     QuestionsMRTForm, QuestionsTMSForm,
                                     QuestionsWomenForm, QuestionsWomenMRTForm,
                                     TMSForm, TokenForm)
from mpi_cbs.mediforms.models import Token
from mpi_cbs.mediforms import models


EMAIL_TEXT = """
Sehr geehrte/r {first_name} {last_name},

hiermit erhalten Sie den von Ihnen ausgefüllten Fragebogen als PDF im Anhang.
Bitte halten Sie diesen für das Gespräch zur Aufklärung mit einem unserer Ärzte bereit.
Hierfür erhalten Sie einen Termin oder haben bereits einen erhalten.
Bei Rückfragen zum Fragebogen schreiben Sie an unsere Ärzte: studienaerzte@cbs.mpg.de

Mit freundlichen Grüßen
Ihr Max-Planck-Institut für Kognitions- und Neurowissenschaften in Leipzig (MPI-CBS)
"""


def get_form_class(method):
    if method == 'mrt':
        return MRTForm
    elif method == 'mrtbegleitung':
        return MRTBegleitungForm
    elif method == 'tms':
        return TMSForm


def get_pdf_model(method):
    if method == 'mrt':
        return models.PDFMRT
    elif method == 'mrtbegleitung':
        return models.PDFMRTBegleitung
    elif method == 'tms':
        return models.PDFTMS


def get_questions_form_classes(method):
    if method.startswith('mrt'):
        return dict(general=QuestionsMRTForm, women=QuestionsWomenMRTForm)
    elif method == 'tms':
        return dict(general=QuestionsTMSForm, women=QuestionsWomenForm)


class Index(LoginRequiredMixin, generic.FormView):
    form_class = TokenForm
    template_name = 'mediforms/index.html'

    def get_context_data(self):
        context_data = super().get_context_data()
        context_data['method'] = self.request.GET.get('method', '')
        context_data['token'] = self.request.GET.get('token', '')
        return context_data

    def post(self, request, *args, **kwargs):
        token, _created = Token.objects.get_or_create(
            method_id=request.POST.get('method'),
            pseudonym=request.POST.get('pseudonym'),
            defaults=dict(created_by=self.request.user),
        )
        params = urlencode(dict(
            token=token.id,
            method=token.method,
        ))
        return HttpResponseRedirect('{}?{}'.format(reverse('index'), params))


class TokenListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'tokens'
    model = Token
    template_name = 'mediforms/token_list.html'


class FormView(generic.FormView):
    def dispatch(self, request, *args, **kwargs):
        self.token = get_object_or_404(Token, pk=kwargs.get('token'))
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return [f'mediforms/pages/form_{self.token.method.key}.html']

    def get_context_data(self, **kwargs):
        questions_form_classes = get_questions_form_classes(self.token.method.key)

        context = super().get_context_data(**kwargs)
        context['method'] = self.token.method
        form_data = None if self.request.method == 'GET' else self.request.POST
        context['personal_data_form'] = PersonalDataForm(form_data)
        context['questions_form'] = questions_form_classes['general'](form_data, initial={'mrtanzahl': 0})
        context['questions_form_women'] = questions_form_classes['women'](form_data)
        context['consent_agreement_form'] = ConsentAgreementForm()

        return context

    def get_form_class(self):
        return get_form_class(self.token.method.key)

    def form_valid(self, form):
        self.form_data = form.save(commit=False)
        self.form_data.pseudonym = self.token.pseudonym
        self.form_data.token_created_by = self.token.created_by
        self.form_data.save()
        self.token.delete()

        questions_form_classes = get_questions_form_classes(self.token.method.key)

        html_template = get_template(f'mediforms/pdfs/{self.token.method.key}.html')
        rendered_html = html_template.render({
            'method': self.token.method,
            'form': form,
            'personal_data_form': PersonalDataForm(instance=self.form_data),
            'questions_form': questions_form_classes['general'](instance=self.form_data),
            'questions_form_women': questions_form_classes['women'](instance=self.form_data),
        })
        content = HTML(string=rendered_html).write_pdf()

        filename = '_'.join([
            'consent',
            self.token.method.key,
            models.sanitize_string(self.form_data.last_name),
            models.sanitize_string(self.form_data.first_name),
            self.form_data.date_of_birth.strftime("%Y%m%d")
        ]) + '.pdf'
        file_handle = SimpleUploadedFile(name=filename, content=content,
                                         content_type='application/pdf')

        pdf = get_pdf_model(self.token.method.key).objects.create(form_data=self.form_data,
                                                                  file_handle=file_handle)

        email = EmailMessage(
            subject=settings.MEDIFORMS_EMAIL_SUBJECT,
            body=EMAIL_TEXT.format(first_name=self.form_data.first_name,
                                   last_name=self.form_data.last_name),
            from_email=settings.MEDIFORMS_EMAIL_FROM,
            to=settings.MEDIFORMS_EMAIL_RECIPIENTS_LIST_TO,
            bcc=settings.MEDIFORMS_EMAIL_RECIPIENTS_LIST_BCC,
            reply_to=settings.MEDIFORMS_EMAIL_RECIPIENTS_LIST_REPLY_TO,
        )
        email.attach_file(pdf.file_handle.path)
        email.send()

        return HttpResponse(file_handle, content_type='application/pdf')


class DataStorageConsentView(generic.TemplateView):
    template_name = 'mediforms/pages/data_storage_consent.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        method = self.kwargs.get('method')
        if method.startswith('mrt'):
            context['method'] = 'MRT'
        elif method == 'tms':
            context['method'] = 'TMS/tDCS'
        return context
