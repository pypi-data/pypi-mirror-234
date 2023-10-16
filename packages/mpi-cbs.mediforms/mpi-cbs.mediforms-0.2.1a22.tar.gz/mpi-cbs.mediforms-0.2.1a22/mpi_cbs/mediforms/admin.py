from django import forms
from django.contrib import admin
from django.utils.html import format_html

from mpi_cbs.mediforms import models


class FormDataAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('pseudonym', 'last_name', 'first_name', 'date_of_birth',
                    'created_at', 'token_created_by')
    search_fields = 'pseudonym', 'last_name', 'first_name'


class MethodForm(forms.ModelForm):
    class Meta:
        model = models.Method
        fields = 'key', 'name', 'color'
        widgets = {
            'color': forms.widgets.TextInput(attrs={'type': 'color'}),
        }


class MethodAdmin(admin.ModelAdmin):
    form = MethodForm
    list_display = 'key', 'name', '_color'

    def _color(self, method):
        return format_html('<span style="color: {};">{}</span>', method.color, method.color)


class PDFAdmin(admin.ModelAdmin):
    list_display = 'pseudonym', 'last_name', 'first_name'

    def pseudonym(self, pdf):
        return pdf.form_data.pseudonym

    def last_name(self, pdf):
        return pdf.form_data.last_name

    def first_name(self, pdf):
        return pdf.form_data.first_name

    def has_change_permission(self, request, pdf=None):
        return False


class TokenAdmin(admin.ModelAdmin):
    list_display = 'pk', 'method', 'pseudonym', 'created_at', 'created_by'


admin.site.register(models.FormDataMRT, FormDataAdmin)
admin.site.register(models.FormDataMRTBegleitung, FormDataAdmin)
admin.site.register(models.FormDataTMS, FormDataAdmin)
admin.site.register(models.Method, MethodAdmin)
admin.site.register(models.PDFMRT, PDFAdmin)
admin.site.register(models.PDFMRTBegleitung, PDFAdmin)
admin.site.register(models.PDFTMS, PDFAdmin)
admin.site.register(models.Token, TokenAdmin)
