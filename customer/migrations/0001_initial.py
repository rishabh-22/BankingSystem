# Generated by Django 3.1.7 on 2021-04-08 22:10

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_number', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now=True)),
                ('balance', models.IntegerField(default=0)),
                ('branch', models.CharField(default='delhi', max_length=100)),
                ('micr_code', models.CharField(default='ABCD', max_length=20)),
                ('branch_code', models.CharField(default='XYZ', max_length=20)),
                ('ifsc_code', models.CharField(default='ICIC001234', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('age', models.IntegerField()),
                ('number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(code='nomatch', message='invalid mobile number!', regex='^[6-9]\\d{9}$')])),
                ('aadhaar', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(code='nomatch', message='invalid aadhaar number!', regex='^\\d{12}$')])),
                ('pan_card', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(code='nomatch', message='invalid pan card number!', regex='^[A-Z]{5}[0-9]{4}[A-Z]$')])),
                ('address', models.TextField()),
                ('date_of_birth', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Customers',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now=True)),
                ('amount', models.IntegerField()),
                ('balance', models.IntegerField()),
                ('transferee', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('DB', 'Debit'), ('CR', 'Credit')], max_length=20)),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('In Progress', 'In Progress'), ('Failed', 'Failed'), ('On Hold', 'On Hold')], max_length=20)),
                ('mode', models.CharField(choices=[('Cheque', 'Cheque'), ('NEFT', 'NEFT'), ('IMPS', 'IMPS'), ('UPI', 'UPI')], max_length=20)),
                ('location', models.CharField(max_length=100)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.account')),
            ],
        ),
    ]
