# Generated by Django 5.1.4 on 2025-01-18 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CharaimageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('charaimage', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='ChatModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_dialogue', models.CharField(default='', max_length=255)),
                ('name', models.CharField(default='', max_length=50)),
            ],
        ),
    ]
