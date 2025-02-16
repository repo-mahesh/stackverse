# Generated by Django 5.1.5 on 2025-02-01 19:48

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('author', models.CharField(max_length=100)),
                ('source', models.CharField(blank=True, max_length=100, null=True)),
                ('tags', models.ManyToManyField(blank=True, related_name='quotes', to='api.tag')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveredQuote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_date', models.DateField(default=django.utils.timezone.now)),
                ('delivery_order', models.SmallIntegerField(choices=[(1, 'First'), (2, 'Second'), (3, 'Third')], default=1)),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.quote')),
            ],
            options={
                'ordering': ['-delivery_date', 'delivery_order'],
                'constraints': [models.UniqueConstraint(fields=('quote', 'delivery_date'), name='unique_quote_per_day')],
            },
        ),
    ]
