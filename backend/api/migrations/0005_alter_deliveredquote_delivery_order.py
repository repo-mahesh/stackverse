# Generated by Django 5.1.5 on 2025-01-31 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_deliveredquote_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveredquote',
            name='delivery_order',
            field=models.SmallIntegerField(choices=[(1, 'First'), (2, 'Second'), (3, 'Third')], default=1),
        ),
    ]
