# Generated by Django 4.0 on 2021-12-27 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('calldata', models.CharField(max_length=50)),
                ('price', models.FloatField()),
            ],
            options={
                'verbose_name': 'Food',
                'verbose_name_plural': 'Foods',
            },
        ),
        migrations.CreateModel(
            name='FoodType',
            fields=[
                ('id', models.PositiveIntegerField(auto_created=True, primary_key=True, serialize=False, unique=True)),
                ('text', models.CharField(max_length=50)),
                ('calldata', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'FoodType',
                'verbose_name_plural': 'FoodTypes',
            },
        ),
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('chat_id', models.PositiveBigIntegerField(primary_key=True, serialize=False, unique=True, verbose_name='ID пользователя')),
                ('firstname', models.CharField(blank=True, max_length=64, null=True)),
                ('username', models.CharField(blank=True, max_length=32, null=True)),
                ('language', models.CharField(default='ru', max_length=3)),
                ('phone', models.CharField(blank=True, max_length=12, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('stage', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(default='in cart', max_length=50)),
                ('chat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgbot.tguser')),
                ('food', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tgbot.food')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tgbot.foodtype')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.AddField(
            model_name='food',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgbot.foodtype'),
        ),
    ]
