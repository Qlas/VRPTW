# Generated by Django 3.2.11 on 2022-01-04 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vue_api', '0003_client_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='description',
            field=models.CharField(blank=True, default='a', max_length=255),
            preserve_default=False,
        ),
    ]
