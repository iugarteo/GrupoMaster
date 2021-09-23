from flask import request, jsonify, abort
from flask import current_app as app
from .models import Account, Payment
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from . import Session


# Payment Routes #######################################################################################################
@app.route('/payment', methods=['GET'])
@app.route('/payments', methods=['GET'])
def view_payments():
    session = Session()
    client_id = request.args.get('client_id')
    if client_id:
        print("GET All Payments of Account {}".format(client_id))
        payments = session.query(Payment).filter_by(id=client_id).all()
    else:
        print("GET All Payments")
        payments = session.query(Payment).all()
    response = jsonify(Payment.list_as_dict(payments))
    session.close()
    return response


@app.route('/payment/<int:payment_id>', methods=['GET'])
def view_payment(payment_id):
    session = Session()
    payment = session.query(Payment).get(payment_id)
    if not payment:
        abort(NotFound.code)
    print("GET Order {}: {}".format(payment_id, payment))
    response = jsonify(payment.as_dict())
    session.close()
    return response

#@app.rout('/can_make_payment', methods=['GET'])
#def can_make_payment:
    #session = Session()


@app.route('/payment', methods=['POST'])
def create_payment():
    session = Session()
    new_payment = None
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    client_id = content['client']
    amount = content['amount']
    account = session.query(Account).get(client_id)
    if not account:
        abort(NotFound.code)
    try:
        new_payment = Payment(
            client_id=client_id,
            amount=amount
        )
        session.add(new_payment)
        session.commit()
        account.balance -= amount
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    response = jsonify(new_payment.as_dict())
    session.close()
    return response


# Account Routes #######################################################################################################
@app.route('/account', methods=['GET'])
@app.route('/accounts', methods=['GET'])
def view_accounts():
    session = Session()
    print("GET All Accounts.")
    accounts = session.query(Account).all()
    response = jsonify(Account.list_as_dict(accounts))
    session.close()
    return response


@app.route('/account/<int:client_id>', methods=['GET'])
def view_balance(client_id):
    session = Session()
    account = session.query(Account).filter_by(client_id=client_id).first()
    if not account:
        abort(NotFound.code)
    print("GET Client {}: {}".format(client_id, account))
    response = jsonify(account.as_dict())
    session.close()
    return response


@app.route('/account', methods=['POST'])
def add_money_to_account():
    session = Session()
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    try:
        client_id = content['client']
        balance = content['amount']
        account = session.query(Account).filter_by(client_id=client_id).first()
        if not account:
            new_account = Account(
                client_id=client_id,
                balance=balance
            )
            session.add(new_account)
            session.commit()
            response = jsonify(new_account.as_dict())
        else:
            account.balance += balance
            session.commit()
            response = jsonify((account.as_dict()))
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
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
