# Generated by Django 5.1.6 on 2025-02-17 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_companyprofile_industry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='industry',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
