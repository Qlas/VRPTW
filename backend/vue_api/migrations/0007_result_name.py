# Generated by Django 3.2.11 on 2022-01-07 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vue_api', '0006_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='name',
            field=models.CharField(default='test', max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
