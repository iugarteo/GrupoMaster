from flask import request, jsonify, abort
from flask import current_app as app
from .models import Account, Payment
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from . import Session, checkJWT

# Payment Routes #######################################################################################################
from .payment_service import view_all_payments, view_payment_by_id, view_all_payments_by_client, view_account, \
    view_all_accounts, create_account, increment_balance, create_payment


@app.route('/payment/getPayment/<int:payment_id>', methods=['GET'])
def view_payment(payment_id):
    session = Session()
    token = request.headers["Authorization"].split(" ")
    permisions = checkJWT.checkPermissions("payment.getPayment", token[1])
    if permisions == True:
        payment = view_payment_by_id(session, payment_id)
        response = jsonify(payment.as_dict())
    else:
        abort(BadRequest.code)
    if not payment:
        abort(NotFound.code)
    session.close()
    return response


@app.route('/payment/getPaymentsbyClient', methods=['PATCH'])
def view_clients_payments():
    session = Session()
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    client_id = content['client_id']

    token = request.headers["Authorization"].split(" ")
    permisions = checkJWT.checkPermissions("payment.getPaymentsbyClient", token[1])
    if permisions == True:
        payments = view_all_payments_by_client(session, client_id)
        response = jsonify(Payment.list_as_dict(payments))
    else:
        abort(BadRequest.code)
    session.close()
    return response


@app.route('/payment/getPayments', methods=['GET'])
def view_payments():
    session = Session()
    token = request.headers["Authorization"].split(" ")
    permisions = checkJWT.checkPermissions("payment.getPayments", token[1])
    if permisions == True:
        payments = view_all_payments(session)
        response = jsonify(Payment.list_as_dict(payments))
    else:
        abort(BadRequest.code)
    session.close()
    return response


@app.route('/payment/createPayment', methods=['POST'])
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
        token = request.headers["Authorization"].split(" ")
        permissions = checkJWT.checkPermissions("payment.createPayment", token[1])
        if permissions:
            payment = create_payment(session, account, client_id, amount)
            response = jsonify(result=True, order_id=order_id)
        else:
            abort(BadRequest.code)
        if not payment:
            abort(BadRequest.code)
    session.close()
    return response


# Account Routes #######################################################################################################
@app.route('/payment/getAccounts', methods=['GET'])
def view_accounts():
    session = Session()
    token = request.headers["Authorization"].split(" ")
    permissions = checkJWT.checkPermissions("payment.getAccounts", token[1])
    if permissions:
        accounts = view_all_accounts(session)
        response = jsonify(Account.list_as_dict(accounts))
    else:
        abort(BadRequest.code)
    session.close()
    return response


@app.route('/payment/getAccount/<int:client_id>', methods=['GET'])
def view_balance(client_id):
    session = Session()
    token = request.headers["Authorization"].split(" ")
    permissions = checkJWT.checkPermissions("payment.getAccount", token[1])
    if permissions:
        account = view_account(session, client_id)
        response = jsonify(account.as_dict())
    else:
        abort(BadRequest.code)
    if not account:
        abort(NotFound.code)
    session.close()
    return response


@app.route('/payment/createAccount', methods=['POST'])
def add_money():
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    session = Session()
    content = request.json
    client_id = content['client']
    amount = content['amount']
    account = view_account(session, client_id)
    token = request.headers["Authorization"].split(" ")
    permissions = checkJWT.checkPermissions("payment.createAccount", token[1])
    if permissions:
        if not account:
            account = create_account(session, client_id, amount)
        else:
            account = increment_balance(session, account.id, amount)
        response = jsonify(account.as_dict())
    else:
        abort(BadRequest.code)

    if not account:
        abort(BadRequest.code)
    session.close()
    return response

# Health Check ################
@app.route('/health', methods=['HEAD', 'GET'])
def health_check():
 #abort(BadRequest)
#if(machine.state == "Free"):
    #messagge"The service Order is up and free, give it some work."
 #if(machine.state == "Working"):
    #messagge = "The service Order is up but currently working, wait a little." 
#if(machine.state == "Down"):
    #messagge = "The machine is down, we are working on it."
#return messagge
 return "OK"

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
