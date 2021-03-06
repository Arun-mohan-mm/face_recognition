# Generated by Django 3.0.6 on 2020-05-22 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face', '0015_remove_exam_results_teacher_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='Address',
            field=models.TextField(),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registration',
            name='DOB',
            field=models.CharField(max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registration',
            name='DOJ_course',
            field=models.CharField(max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registration',
            name='Gender',
            field=models.CharField(max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registration',
            name='Phone',
            field=models.CharField(max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registration',
            name='Qualification',
            field=models.CharField(max_length=200),
            preserve_default=False,
        ),
    ]
