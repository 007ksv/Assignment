# Generated by Django 3.1.1 on 2020-09-06 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_applicationforleave'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationforleave',
            name='total_leave_given',
        ),
        migrations.AlterField(
            model_name='applicationforleave',
            name='leave_pending',
            field=models.PositiveSmallIntegerField(default=10),
        ),
    ]
