# Generated by Django 4.2.5 on 2024-09-12 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_pagestate_search_phrase'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagestate',
            name='search_type',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
