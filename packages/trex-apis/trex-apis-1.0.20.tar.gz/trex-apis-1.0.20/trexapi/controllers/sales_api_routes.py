from flask import Blueprint, request, session, jsonify 
from flask_restful import abort
import logging
from trexlib.utils.log_util import get_tracelog
from flask_restful import Api
from trexmodel.utils.model.model_util import create_db_client
#from flask.json import jsonify
from datetime import datetime, timedelta
from trexapi.decorators.api_decorators import auth_token_required,\
    outlet_key_required, user_auth_token_required
from trexlib.utils.string_util import is_not_empty
from trexmodel.models.datastore.customer_models import Customer
from trexmodel.models.datastore.user_models import User
from trexadmin.libs.http import create_rest_message
from trexadmin.libs.http import StatusCode
from trexmodel.models.datastore.merchant_models import Outlet,\
    MerchantAcct, MerchantUser
from werkzeug.datastructures import ImmutableMultiDict
from trexmodel.models.datastore.transaction_models import SalesTransaction,\
    CustomerTransaction

from trexapi.utils.reward_transaction_helper import create_sales_transaction,\
    give_reward_from_sales_transaction
from trexapi.utils.api_helpers import get_logged_in_api_username
from trexmodel.models.datastore.voucher_models import MerchantVoucher
from trexapi import conf
from trexmodel.models.datastore.prepaid_models import PrepaidSettings
from trexadmin.libs.jinja.common_filters import format_currency_with_currency_label_filter
from trexadmin.libs.flask.utils.flask_helper import get_merchant_configured_currency_details
from trexmodel import program_conf
from trexapi.forms.sales_api_forms import SalesTransactionForm
from trexlib.utils.crypto_util import encrypt, decrypt, decrypt_json
from trexapi.conf import EARN_INSTANT_REWARD_URL
from trexmodel.models.datastore.model_decorators import model_transactional
from trexanalytics.bigquery_upstream_data_config import create_merchant_customer_transaction_upstream_for_merchant
from flask_babel import gettext



sales_api_bp = Blueprint('sales_api_bp', __name__,
                                 template_folder='templates',
                                 static_folder='static',
                                 url_prefix='/api/v1/sales')

logger = logging.getLogger('debug')


@sales_api_bp.route('/ping', methods=['GET'])
def ping():
    return 'pong', 200

@sales_api_bp.route('/create-sales-transaction', methods=['PUT'])
@auth_token_required
@outlet_key_required
def post_sales_transaction():
    
    logger.info('---post_sales_transaction---')
    
    transaction_data_in_json   = request.get_json()
        
    logger.info('transaction_data_in_json=%s', transaction_data_in_json)
    
    transaction_form = SalesTransactionForm(ImmutableMultiDict(transaction_data_in_json))
    
    if transaction_form.validate():
        logger.debug('reward transaction data is valid')
        
        sales_amount        = float(transaction_form.sales_amount.data)
        tax_amount          = transaction_form.tax_amount.data
        invoice_id          = transaction_form.invoice_id.data
        remarks             = transaction_form.remarks.data
        invoice_details     = transaction_data_in_json.get('invoice_details')
        
        transact_datetime   = None
        
        
        if tax_amount is None:
            tax_amount = .0
        else:
            tax_amount = float(tax_amount)
         
        logger.debug('sales_amount=%s', sales_amount)
        logger.debug('tax_amount=%s', tax_amount)
        logger.debug('invoice_id=%s', invoice_id)
        logger.debug('remarks=%s', remarks)
        logger.debug('invoice_details=%s', invoice_details)
        
        db_client = create_db_client(caller_info="post_sales_transaction")
        
        check_transaction_by_invoice_id = None
        
        if is_not_empty(invoice_id):
            with db_client.context():
                check_transaction_by_invoice_id = SalesTransaction.get_by_invoice_id(invoice_id)
        
        if check_transaction_by_invoice_id:
            return create_rest_message("The invoice id have been taken", status_code=StatusCode.BAD_REQUEST)
        else:
            transact_datetime_in_gmt    = transaction_form.transact_datetime.data
            merchant_username           = get_logged_in_api_username()
            
            
            if merchant_username:
                try:
                    with db_client.context():
                        transact_outlet         = Outlet.fetch(request.headers.get('x-outlet-key'))
                        merchant_acct           = transact_outlet.merchant_acct_entity
                        
                            
                        if transact_datetime_in_gmt:
                            transact_datetime    =  transact_datetime_in_gmt - timedelta(hours=merchant_acct.gmt_hour)
                            
                            now                  = datetime.utcnow()
                            if transact_datetime > now:
                                return create_rest_message('Transact datetime cannot be future', status_code=StatusCode.BAD_REQUEST)
                        
                        
                        
                        transact_merchant_user = MerchantUser.get_by_username(merchant_username)
                        
                        sales_transaction = create_sales_transaction( 
                                                                        transact_outlet     = transact_outlet, 
                                                                        sales_amount        = sales_amount,
                                                                        tax_amount          = tax_amount,
                                                                        invoice_id          = invoice_id,
                                                                        remarks             = remarks,
                                                                        transact_by         = transact_merchant_user,
                                                                        transact_datetime   = transact_datetime,
                                                                        invoice_details     = invoice_details,
                                                                    )
                        
                    if sales_transaction:
                        encrypted_transaction_id    = encrypt(sales_transaction.transaction_id)
                        logger.debug('EARN_INSTANT_REWARD_URL=%s', EARN_INSTANT_REWARD_URL)
                        entitled_url                = EARN_INSTANT_REWARD_URL.format(code=encrypted_transaction_id)
                        
                        transaction_details =  {
                                                "entitled_url"            : entitled_url,
                                                }
                            
                    return jsonify(transaction_details)
                except:
                    logger.error('Failed to proceed transaction due to %s', get_tracelog())
                    return create_rest_message('Failed to proceed transaction', status_code=StatusCode.BAD_REQUEST)
                            
            else:
                return create_rest_message('Missing transact user account', status_code=StatusCode.BAD_REQUEST)
        
    else:
        logger.warn('sales transaction data input is invalid')
        error_message = transaction_form.create_rest_return_error_message()
        
        return create_rest_message(error_message, status_code=StatusCode.BAD_REQUEST)

@sales_api_bp.route('/transaction/<encrypted_transaction_id>/read-instant-reward', methods=['GET'])
#@user_auth_token_required
def read_instant_reward_get(encrypted_transaction_id): 
    
    try:
        transaction_id    = decrypt(encrypted_transaction_id)
    except:
        logger.debug('Failed to decrypt transaction id')
        return create_rest_message(gettext('Invalid reward code'), status_code=StatusCode.BAD_REQUEST)    
        
    db_client = create_db_client(caller_info="read_instant_reward_get")
    
    with db_client.context():
        sales_transaction = SalesTransaction.get_by_transaction_id(transaction_id)
    
    if sales_transaction:
        with db_client.context():
            merchant_acct = sales_transaction.transact_merchant_acct
            
        instant_reward = {
                        #"entitled_url"     : EARN_INSTANT_REWARD_URL.format(code=encrypted_transaction_id),
                        'transaction_id'    : transaction_id,
                        'transact_datetime' : sales_transaction.transact_datetime.strftime("%d-%m-%Y %H:%M:%S"),
                        'transact_amount'   : sales_transaction.transact_amount,
                        'used'              : sales_transaction.used,
                        'currency'          : merchant_acct.currency_code,
                        'locale'            : merchant_acct.locale,
                        #'used'             : False,x
                        }
        logger.debug('instant_reward=%s', instant_reward)
        return jsonify(instant_reward) 
    else:
        logger.debug('Invalid transaction id')
        return create_rest_message(gettext('Invalid reward code'), status_code=StatusCode.BAD_REQUEST)
    
    
@sales_api_bp.route('/transaction/<transaction_id>/encrypt-instant-reward-code', methods=['GET'])
#@user_auth_token_required
def encrypt_instant_reward_code_get(transaction_id): 
    
    logger.debug('transaction_id=%s', transaction_id)
    
    encrypted_transaction_id    = encrypt(transaction_id)
    
    logger.debug('encrypted_transaction_id=%s', encrypted_transaction_id)
    
    db_client = create_db_client(caller_info="encrypt_instant_reward_code_get")
    
    with db_client.context():
        sales_transaction = SalesTransaction.get_by_transaction_id(transaction_id)
    
    if sales_transaction.used:
        return create_rest_message(encrypted_transaction_id=encrypted_transaction_id, status_code=StatusCode.BAD_REQUEST)
    else:
        return create_rest_message(encrypted_transaction_id=encrypted_transaction_id, status_code=StatusCode.OK)     
        
    
    
@sales_api_bp.route('/reference-code/<reference_code>/transaction/<encrypted_transaction_id>/customer-earn-instant-reward', methods=['POST'])
#@user_auth_token_required
def customer_earn_instant_reward(reference_code, encrypted_transaction_id): 
    
    db_client = create_db_client(caller_info="customer_earn_instant_reward")
        
    logger.debug('encrypted_transaction_id=%s', encrypted_transaction_id)
    
    transaction_id = decrypt(encrypted_transaction_id)
    
    logger.debug('transaction_id=%s', transaction_id)
        
    if is_not_empty(transaction_id):
        with db_client.context():
            sales_transaction = SalesTransaction.get_by_transaction_id(transaction_id)
            
        
        if sales_transaction:
            
            logger.debug('sales_transaction is found')
            if sales_transaction.used:
                with db_client.context():
                    customer_transaction = CustomerTransaction.get_by_transaction_id(transaction_id)
                    customer_transaction = customer_transaction.to_dict(date_format="%d-%m-%Y", datetime_format="%d-%m-%Y %H:%M:%S")
                
                return jsonify(customer_transaction)
            else:
                try:
                    with db_client.context():
                        merchant_acct = sales_transaction.transact_merchant_acct
                        customer = Customer.get_by_reference_code(reference_code, merchant_acct)
                        
                        if customer:
                            customer_transaction = give_reward_from_sales_transaction(customer, sales_transaction)
                            if customer_transaction:
                                customer_transaction = customer_transaction.to_dict(date_format="%d-%m-%Y", datetime_format="%d-%m-%Y %H:%M:%S")
                    if customer:
                        if customer_transaction:
                            return jsonify(customer_transaction)
                        else:
                            return create_rest_message('Failed to earn reward from transaction', status_code=StatusCode.BAD_REQUEST)
                    else:
                        return create_rest_message('Customer Account not found', status_code=StatusCode.BAD_REQUEST)
                except:
                    logger.error('Failed due to %s', get_tracelog())
                    return create_rest_message('Failed to process transaction', status_code=StatusCode.BAD_REQUEST)
            
        else:
            logger.debug('sales_transaction is not found')
            return create_rest_message('Invalid transaction', status_code=StatusCode.BAD_REQUEST)
    else:
        return create_rest_message('Transaction id is empty', status_code=StatusCode.BAD_REQUEST)
            
    
       
