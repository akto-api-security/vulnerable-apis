# Generated by Django 4.2 on 2023-07-15 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mockvulnerableapis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampledata',
            name='url',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]