import logging

from .LoggingHandler import LoggingHandler
from .models import Payment, Account

#logging.basicConfig(level=logging.DEBUG)  # Enables Debug and Info logs
logger = logging.getLogger('client')
handler = LoggingHandler()
logger.addHandler(handler)


def view_payment_by_id(session, payment_id):
    payment = session.query(Payment).get(payment_id)
    if not payment:
        # ApiClient.log("warning", "view_payment_by_id", "Payment {} not found".format(payment_id))
        session.close()
        return None
    logger.info("GET Payment {}: {}".format(payment_id, payment))
    return payment


def view_all_payments_by_client(session, client_id):
    logger.info("GET All Payments of Client {}".format(client_id))
    # ApiClient.log("warning", "view_all_payments_by_client", "View {} client's all payments".format(client_id))
    payments = session.query(Payment).filter_by(client_id=client_id).all()
    return payments


def view_all_payments(session):
    logger.info("GET All Payments")
    # ApiClient.log("information", "view_all_payments", "Get all payments")
    payments = session.query(Payment).all()
    return payments


def view_all_accounts(session):
    logger.info("GET All Accounts.")
    accounts = session.query(Account).all()
    return accounts


def view_account(session, client_id):
    account = session.query(Account).filter_by(client_id=client_id).first()
    if not account:
        session.close()
        return None
    logger.info("GET Client {}: {}".format(client_id, account))
    return account


def create_account(session, client_id, balance):
    try:
        account = Account(
            client_id=client_id,
            balance=balance
        )
        session.add(account)
        session.commit()
    except KeyError:
        session.rollback()
        account = None
    return account


def increment_balance(session, account_id, amount):
    try:
        account = session.query(Account).get(account_id)
        account.balance += amount
        session.commit()
    except KeyError:
        session.rollback()
        account = None
    return account


def payment_validation(session, client_id, price):
    account = view_account(session, client_id)
    if not account or account.balance < price:
        return False
    return True


def create_payment(session, account, client_id, amount):
    try:
        payment = Payment(
            client_id=client_id,
            amount=amount
        )
        session.add(payment)
        account.balance -= amount
        session.commit()
    except KeyError:
        session.rollback()
        payment = None
    return payment
