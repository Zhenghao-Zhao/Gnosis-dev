# Generated by Django 2.0.4 on 2019-08-21 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20190821_2236'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='endorsemententry',
            options={'ordering': ['-created_at']},
        ),
    ]
