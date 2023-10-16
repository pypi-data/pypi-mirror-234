from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mediforms', '0002_alter_formdatamrt_email_alter_formdatamrt7tptx_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formdatamrtconnectom',
            name='token_created_by',
        ),
        migrations.RemoveField(
            model_name='pdfmrt7tptx',
            name='form_data',
        ),
        migrations.RemoveField(
            model_name='pdfmrtconnectom',
            name='form_data',
        ),
        migrations.DeleteModel(
            name='FormDataMRT7TpTx',
        ),
        migrations.DeleteModel(
            name='FormDataMRTConnectom',
        ),
        migrations.DeleteModel(
            name='PDFMRT7TpTx',
        ),
        migrations.DeleteModel(
            name='PDFMRTConnectom',
        ),
    ]
