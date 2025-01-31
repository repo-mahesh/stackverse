# Generated by Django 5.1.5 on 2025-01-31 12:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_tag_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveredQuote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_date', models.DateField()),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.quote')),
            ],
            options={
                'indexes': [models.Index(fields=['delivery_date'], name='api_deliver_deliver_26bf1f_idx'), models.Index(fields=['quote'], name='api_deliver_quote_i_956fa8_idx')],
                'unique_together': {('quote', 'delivery_date')},
            },
        ),
    ]
