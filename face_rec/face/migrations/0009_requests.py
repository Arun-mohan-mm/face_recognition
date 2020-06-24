# Generated by Django 3.0.6 on 2020-05-18 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('face', '0008_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Email', models.EmailField(max_length=254)),
                ('User_category', models.CharField(max_length=200)),
                ('Old_password', models.CharField(max_length=200)),
                ('New_password', models.CharField(max_length=200)),
                ('Req_reg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='face.Registration')),
            ],
        ),
    ]
