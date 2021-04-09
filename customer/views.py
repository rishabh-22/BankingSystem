import logging
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from customer.models import Transaction, Account
from customer.serializers import RegistrationSerializer
from customer.utils import generate_transaction_number, get_db_counter, get_updated_balance

transaction_modes = {'Cheque', 'NEFT', 'IMPS', 'UPI'}
transaction_types = {'DB', 'CR'}


@api_view(['GET', 'POST'])
@permission_classes([])
def registration_view(request):
    """
    this function is used for registering a user into the system.
    :param request:
    :return:
    """
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user).key
        response = dict(message='successfully registered.', token=token)
        return Response(response, status=status.HTTP_200_OK)
    else:
        response = serializer.errors
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_transaction(request):
    """
    this function is used for adding new transactions
    :param request:
    :return:
    """
    try:  # todo: fix min balance condition
        amount = int(request.data.get('amount'))
        transferee = request.data.get('transferee')
        trans_type = request.data.get('trans_type')
        trans_mode = request.data.get('trans_mode')
        location = request.data.get('location')

        if trans_mode not in transaction_modes or trans_type not in transaction_types:
            raise Exception

        trans_num = generate_transaction_number(get_db_counter())
        account = Account.objects.get(user=request.user)
        balance = get_updated_balance(account, trans_type, amount)
        if balance > 1000:  # minimum balance check
            trans_status = 'Completed'
            updated_balance = balance
            message = 'Transaction successful!'
        else:
            trans_status = 'Failed'
            updated_balance = account.balance
            message = 'Transaction failed due to low balance.'

        Transaction.objects.create(transaction_number=trans_num, account=account, created=datetime.now(),
                                   amount=amount, balance=updated_balance, transferee=transferee, type=trans_type,
                                   status=trans_status, mode=trans_mode, location=location)
        account.balance = updated_balance
        account.save()

        return Response({
            'message': message,
            'transaction_id': trans_num,
            'updated_balance': updated_balance
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logging.error(e)
        return Response({
            'message': 'Please make sure the key value pairs entered are correct.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def view_transaction(request):
    """
    this function is used to view a single transaction
    :param request:
    :return:
    """
    try:
        trans_id = request.data.get('transaction_id')
        transaction = Transaction.objects.get(transaction_number=trans_id)
        return Response(model_to_dict(transaction), status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return Response({
            'message': "No Transaction with such id exists."
        }, status=status.HTTP_404_NOT_FOUND)
