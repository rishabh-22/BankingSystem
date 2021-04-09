from hashlib import blake2s

from .models import Transaction


def generate_transaction_number(count) -> str:
    """
    this method is used to generate a unique hash based on a counter approach.
    :param count:
    :return:
    """
    h = blake2s(digest_size=10)
    res = bytes(str(count), 'utf-8')
    h.update(res)
    return h.hexdigest().upper()


def get_db_counter() -> int:
    """
    this function is used to return a counter integer used to generate a unique hash everytime.
    ***
    when the application is set to scaled, this function here can be replaced with a zookeeper to keep track of
    numerous counters instead of relying on just one which could be a single point of failure.
    ***
    :return: int
    """
    return Transaction.objects.count()


def get_updated_balance(account, trans_type, amount):
    initial_balance = account.balance
    if trans_type == 'DB':
        updated_balance = initial_balance - amount
    else:
        updated_balance = initial_balance + amount

    return updated_balance
