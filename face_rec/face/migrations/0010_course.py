# Generated by Django 3.0.6 on 2020-05-18 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('face', '0009_requests'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Department', models.CharField(max_length=200)),
                ('Course', models.CharField(max_length=200)),
                ('Subject', models.CharField(max_length=200)),
                ('Cou_reg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='face.Registration')),
            ],
        ),
    ]
