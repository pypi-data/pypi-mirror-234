from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediforms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formdatamrt',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='formdatamrt7tptx',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='formdatamrtbegleitung',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='formdatamrtconnectom',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='formdatatms',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, verbose_name='E-mail'),
        ),
    ]
