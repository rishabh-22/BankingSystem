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


@api_view(['POST'])
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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def view_transaction(request):
    """
    this function is used to view transaction(s)
    :param request:
    :return:
    """
    try:
        trans_id = request.data.get('transaction_id')
        if trans_id:
            transaction = Transaction.objects.get(transaction_number=trans_id)
            return Response(model_to_dict(transaction), status=status.HTTP_200_OK)
        else:  # todo: implement pagination in this
            response = []
            transactions = Transaction.objects.filter(account=Account.objects.get(user=request.user))
            for transaction in transactions:
                response.append(model_to_dict(transaction))
            return Response(response, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return Response({
            'message': "No Transaction with such id exists."
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logging.debug(e)
        return Response({
            'message': "Some error occurred, please try again later."
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def filter_transactions(request):
    """
    this function is used to filter transactions based on certain conditions
    :param request:
    :return:
    """
    try:  # todo: implement using viewSets
        data = []
        flag = request.data.get('flag')
        if flag == 'mode':
            trans_mode = request.data.get('trans_mode')
            if trans_mode is None:
                raise Exception
            response = Transaction.objects.filter(account__user=request.user, mode=trans_mode)

        elif flag == 'type':
            trans_type = request.data.get('trans_type')
            if trans_type is None:
                raise Exception
            response = Transaction.objects.filter(account__user=request.user, type=trans_type)

        elif flag == 'status':
            trans_status = request.data.get('trans_status')
            if trans_status is None:
                raise Exception
            response = Transaction.objects.filter(account__user=request.user, status=trans_status)

        elif flag == 'upi_id':
            upi_id = request.data.get('upi_id')
            if upi_id is None:
                raise Exception
            response = Transaction.objects.filter(account__user=request.user, transferee=upi_id)

        elif flag == 'date':
            start_date = request.data.get('start_time')
            end_date = request.data.get('end_date')
            if start_date is None or end_date is None:
                raise Exception
            response = Transaction.objects.filter(account__user=request.user, created__gte=start_date,
                                                  created__lte=end_date)
        elif flag == 'multiple':
            trans_mode = request.data.get('trans_mode')
            trans_type = request.data.get('trans_type')
            trans_status = request.data.get('trans_status')
            upi_id = request.data.get('upi_id')
            start_date = request.data.get('start_time')
            end_date = request.data.get('end_date')
            args = {'account__user': request.user}
            if trans_mode:
                args['mode'] = trans_mode
            if trans_type:
                args['type'] = trans_type
            if trans_status:
                args['status'] = trans_status
            if upi_id:
                args['transferee'] = upi_id
            if start_date:
                args['created__gte'] = start_date
            if end_date:
                args['created__lte'] = end_date
            response = Transaction.objects.filter(**args)

        else:
            raise Exception

        for element in response:
            data.append(model_to_dict(element))
        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        logging.debug(e)
        return Response({
            'message': "Please make sure the key value pairs entered are correct."
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_account(request):
    """
    this function is used to view account details of the logged in user
    :param request:
    :return:
    """
    try:
        account = Account.objects.get(user=request.user)
        return Response(model_to_dict(account), status=status.HTTP_200_OK)

    except Exception as e:
        logging.debug(e)
        return Response({
            'message': "Some error occurred, please try again later."
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_balance(request):
    """
    this function is used to view account balance of the logged in user
    :param request:
    :return:
    """
    try:
        account = Account.objects.get(user=request.user)
        return Response({
            'account_number': account.account_number,
            'balance': account.balance
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logging.debug(e)
        return Response({
            'message': "Some error occurred, please try again later."
        }, status=status.HTTP_400_BAD_REQUEST)
