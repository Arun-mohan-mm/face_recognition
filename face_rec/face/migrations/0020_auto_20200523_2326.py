# Generated by Django 3.0.6 on 2020-05-23 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face', '0019_auto_20200523_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='Class',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='Course',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='registration',
            name='Semester',
            field=models.IntegerField(blank=True),
        ),
    ]
