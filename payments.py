from flask import request
from access import access_required
from flask_jwt_extended import jwt_required
import razorpay
import hmac
import hashlib

razpay_key = '<your_test_key>'
razpay_secret = '<your_test_key_secret>'

rzpay = razorpay.Client(auth=(razpay_key, razpay_secret))
rzpay.set_app_details({"title" : "<your app name>", "version" : "<your app version>"})

def hmac_sha256(val):
    h = hmac.new(razpay_secret.encode("ASCII"), val.encode("ASCII"), digestmod=hashlib.sha256).hexdigest()
    print(h)
    return h

@api.route('/order', methods=['POST'])
@jwt_required
@access_required('TABLE')
def create_order():
    ...
    reqData = request.json()
    ...
    rzData = {}
    rzData['amount'] = reqData['amount']
    rzData['currency'] = reqData['currency']
    rzData['receipt'] = <Your Record ID from database or Receipt ID against which you will be able fetch the transaction record>
    rzData['payment_capture'] = 1 if capture should be done automatically or else 0
    rzresp = rzpay.order.create(data=rzData)  # Calling razorpay api to create order
    print(rzresp)
    ...



@api.route('/verify-txn', methods=['POST'])
@jwt_required
@access_required('TABLE')
def verify_txn():
    reqData = request.json()
    ...
    generated_signature = hmac_sha256(reqData["razorpay_order_id"] + "|" + reqData["razorpay_payment_id"])
    if (generated_signature == reqData["razorpay_signature"]):
       params_dict = { "razorpay_order_id": reqData["razorpay_order_id"], "razorpay_payment_id": reqData["razorpay_payment_id"], 
       "razorpay_signature": reqData["razorpay_signature"] }
       res = rzpay.payment.capture(reqData["razorpay_payment_id"], reqData["amount"], {"currency":"INR"})
    ...
                

@api.route('/failed-txn', methods=['POST'])
@jwt_required
@access_required('TABLE')
def remove_failed_order():
    ...
    # Your logic to handle the case when the user has closed the form and the transaction has now failed. 
    
