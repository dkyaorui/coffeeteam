# Generated by Django 2.0.3 on 2018-04-11 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ActivityType', models.IntegerField(choices=[(1, 'ACM'), (2, '世界超算大赛'), (3, '大学生创新创业大赛'), (4, '微创杯'), (5, '蓝桥杯'), (6, '挑战杯')])),
                ('content', models.CharField(max_length=512)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('viewNum', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]