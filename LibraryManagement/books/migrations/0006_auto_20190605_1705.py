# Generated by Django 2.2.1 on 2019-06-05 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20190605_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuedetail',
            name='issued_on',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='issuedetail',
            name='returned_on',
            field=models.DateField(null=True),
        ),
    ]