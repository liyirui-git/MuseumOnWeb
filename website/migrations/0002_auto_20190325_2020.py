# Generated by Django 2.1.7 on 2019-03-25 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('username', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=16)),
                ('limits', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Test',
        ),
    ]
