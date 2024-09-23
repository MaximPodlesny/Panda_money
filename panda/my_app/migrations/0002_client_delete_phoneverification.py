# Generated by Django 5.1.1 on 2024-09-20 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Фамилия')),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Отчество')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Электронная почта')),
                ('inn', models.CharField(blank=True, max_length=12, null=True, verbose_name='ИНН')),
                ('identity_document', models.CharField(blank=True, max_length=20, null=True, verbose_name='Удостоверение личности')),
                ('code', models.CharField(max_length=6)),
                ('phone_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата подачи заявки')),
            ],
            options={
                'verbose_name': 'Заявка на займ',
                'verbose_name_plural': 'Заявки на займ',
                'ordering': ['-created_at'],
            },
        ),
        migrations.DeleteModel(
            name='PhoneVerification',
        ),
    ]
