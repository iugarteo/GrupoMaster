from flask import request, jsonify, abort
from flask import current_app as app
from .models import Account, Payment
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from . import Session

# Payment Routes #######################################################################################################
from .payment_service import view_all_payments, view_payment_by_id, view_all_payments_by_client, view_account, \
    view_all_accounts, create_account, increment_balance, create_payment


@app.route('/payment/<int:payment_id>', methods=['GET'])
def view_payment(payment_id):
    session = Session()
    payment = view_payment_by_id(session, payment_id)
    if not payment:
        abort(NotFound.code)
    response = jsonify(payment.as_dict())
    session.close()
    return response


@app.route('/payment', methods=['PATCH'])
@app.route('/payments', methods=['PATCH'])
def view_clients_payments():
    session = Session()
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    client_id = content['client_id']
    payments = view_all_payments_by_client(session, client_id)
    response = jsonify(Payment.list_as_dict(payments))
    session.close()
    return response


@app.route('/payment', methods=['GET'])
@app.route('/payments', methods=['GET'])
def view_payments():
    session = Session()
    payments = view_all_payments(session)
    response = jsonify(Payment.list_as_dict(payments))
    session.close()
    return response


@app.route('/payment', methods=['POST'])
def make_payment():
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    client_id = content['client']
    amount = content['amount']
    order_id = content['order']
    session = Session()
    account = view_account(session, client_id)

    if not account:
        abort(NotFound.code)
    if account.balance < amount:
        response = jsonify(result=False, order_id=order_id)
    else:
        payment = create_payment(session, account, client_id, amount)
        if not payment:
            abort(BadRequest.code)
        response = jsonify(result=True, order_id=order_id)
    session.close()
    return response


# Account Routes #######################################################################################################
@app.route('/account', methods=['GET'])
@app.route('/accounts', methods=['GET'])
def view_accounts():
    session = Session()
    accounts = view_all_accounts(session)
    response = jsonify(Account.list_as_dict(accounts))
    session.close()
    return response


@app.route('/account/<int:client_id>', methods=['GET'])
def view_balance(client_id):
    session = Session()
    account = view_account(session, client_id)
    if not account:
        abort(NotFound.code)
    response = jsonify(account.as_dict())
    session.close()
    return response


@app.route('/account', methods=['POST'])
def add_money():
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    session = Session()
    content = request.json
    client_id = content['client']
    amount = content['amount']
    account = view_account(session, client_id)
    if not account:
        account = create_account(session, client_id, amount)
    else:
        account = increment_balance(session, account.id, amount)
    if not account:
        abort(BadRequest.code)
    response = jsonify(account.as_dict())
    session.close()
    return response


# Error Handling #######################################################################################################
@app.errorhandler(UnsupportedMediaType)
def unsupported_media_type_handler(e):
    return get_jsonified_error(e)


@app.errorhandler(BadRequest)
def bad_request_handler(e):
    return get_jsonified_error(e)


@app.errorhandler(NotFound)
def resource_not_found_handler(e):
    return get_jsonified_error(e)


@app.errorhandler(InternalServerError)
def server_error_handler(e):
    return get_jsonified_error(e)


def get_jsonified_error(e):
    traceback.print_tb(e.__traceback__)
    return jsonify({"error_code": e.code, "error_message": e.description}), e.code
