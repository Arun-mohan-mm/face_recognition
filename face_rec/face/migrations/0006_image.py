# Generated by Django 3.0.6 on 2020-05-18 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face', '0005_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='')),
            ],
        ),
    ]
