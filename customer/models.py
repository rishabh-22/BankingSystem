from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


TRANSACTION_TYPE = (
    ('DB', 'Debit'),
    ('CR', 'Credit'),
)

TRANSACTION_STATUS = (
    ('Completed', 'Completed'),
    ('In Progress', 'In Progress'),
    ('Failed', 'Failed'),
    ('On Hold', 'On Hold'),
)

TRANSACTION_MODE = (
    ('Cheque', 'Cheque'),
    ('NEFT', 'NEFT'),
    ('IMPS', 'IMPS'),
    ('UPI', 'UPI'),
)


class Customer(User):
    age = models.IntegerField(null=False)
    number = models.CharField(max_length=10, null=False, validators=[RegexValidator(regex=r'^[6-9]\d{9}$',
                                                                     message='invalid mobile number!', code='nomatch')])
    aadhaar = models.CharField(max_length=12, null=False, validators=[RegexValidator(regex=r'^\d{12}$',
                                                                      message='invalid aadhaar number!',
                                                                                     code='nomatch')])
    pan_card = models.CharField(max_length=10, null=False, validators=[RegexValidator(regex=r'^[A-Z]{5}[0-9]{4}[A-Z]$',
                                                                       message='invalid pan card number!',
                                                                                      code='nomatch')])
    address = models.TextField(null=False)
    date_of_birth = models.DateField(null=False, )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Customers"


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, null=False, primary_key=True)
    created = models.DateTimeField(auto_now=True)
    balance = models.IntegerField(null=False, default=0)
    branch = models.CharField(max_length=100, null=False, default='delhi')
    micr_code = models.CharField(max_length=20, null=False, default='ABCD')
    branch_code = models.CharField(max_length=20, null=False, default='XYZ')
    ifsc_code = models.CharField(max_length=20, null=False, default='ICIC001234')

    def __str__(self):
        return self.account_number


class Transaction(models.Model):
    transaction_number = models.CharField(max_length=50, primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(null=False)
    balance = models.IntegerField(null=False)
    transferee = models.CharField(max_length=100, null=False)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPE, null=False)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, null=False)
    mode = models.CharField(max_length=20, choices=TRANSACTION_MODE, null=False)
    location = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.transaction_number


@receiver(post_save, sender=Customer)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Customer)
def create_customer_account(sender, instance, created, **kwargs):
    if created:
        count = Account.objects.count()
        number = '12340' + str(count+1).zfill(7)
        Account.objects.create(user=instance, account_number=number)
