# Generated by Django 3.0.1 on 2020-01-07 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sidefone', '0002_contact_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='img',
            field=models.ImageField(default='', upload_to='sidefone'),
            preserve_default=False,
        ),
    ]
