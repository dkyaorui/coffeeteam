# Generated by Django 2.0.2 on 2018-04-17 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20180417_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='tname',
            field=models.CharField(default='', max_length=10),
        ),
    ]
