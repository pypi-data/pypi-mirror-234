'''
Created on 30 Jun 2021

@author: jacklok
'''

from flask import Blueprint, request, Response, session 
from flask_restful import Resource, abort
import logging
from trexlib.utils.log_util import get_tracelog
from flask_httpauth import HTTPBasicAuth
from trexapi import conf
from flask_restful import Api
from trexmodel.utils.model.model_util import create_db_client
from trexmodel.models.datastore.merchant_models import MerchantUser,\
    MerchantAcct
import hashlib
from random import random
from trexlib.utils.string_util import is_not_empty
from flask.json import jsonify
from trexapi import conf as api_conf
from trexapi.decorators.api_decorators import auth_token_required
from trexmodel.models.datastore.loyalty_models import LoyaltyDeviceSetting
from trexmodel.models.datastore.pos_models import POSSetting
from trexapi.controllers.api_routes import APIBaseResource
from trexmodel.models import merchant_helpers
from trexadmin.libs.http import create_rest_message, StatusCode
from trexmodel.models.datastore.customer_models import Customer

#logger = logging.getLogger('api')
logger = logging.getLogger('debug')

auth = HTTPBasicAuth()
#auth = HTTPBasicAuthWrapper()


merchant_api_bp = Blueprint('merchant_api_bp', __name__,
                                 template_folder='templates',
                                 static_folder='static',
                                 url_prefix='/api/v1/merchant')

merchant_api = Api(merchant_api_bp)



@merchant_api_bp.route('/ping', methods=['GET'])
def ping():
    return 'Pong', 200

@auth.verify_password
def verify_user_auth(username, password):
    if not (username and password):
        return False
    
    db_client   = create_db_client(caller_info="verify_user_auth")
    valid_auth  = False
    
    logger.debug('username=%s', username)
    logger.debug('password=%s', password)
    
    with db_client.context():
        merchant_user = MerchantUser.get_by_username(username)
        
        logger.debug('merchant_user=%s', merchant_user)
        
        if merchant_user:
            
            md5_hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
            
            logger.debug('verify_user_auth: md5_hashed_password=%s', md5_hashed_password)
            
            if merchant_user.is_valid_password(md5_hashed_password):
                valid_auth = True
            else:
                logger.warn('Invalid merchant password')
        else:
            logger.warn('Invalid merchant username=%s', username)    
        
    return valid_auth

@merchant_api_bp.route('/<merchant_acct_code>/details', methods=['GET'])
def read_merchant_acct(merchant_acct_code):
    
    merchant_acct           = None
    if is_not_empty(merchant_acct_code):
        db_client = create_db_client(caller_info="read_merchant_acct")
        with db_client.context():
            merchant_acct = MerchantAcct.get_by_account_code(merchant_acct_code)
            logger.debug('website=%s', merchant_acct.website)
            merchant_info = merchant_helpers.construct_merchant_acct_info(merchant_acct) 
            
        return create_rest_message(status_code=StatusCode.OK,
                                               **merchant_info
                                               )
    else:
        return create_rest_message("Missing merchant account key", status_code=StatusCode.BAD_REQUEST)

@merchant_api_bp.route('/<merchant_key>/customer-details/reference-code/<reference_code>', methods=['GET'])
def read_merchant_customer_details(merchant_key, reference_code):
    
    merchant_acct           = None
    customer_details_dict   = {} 
    
    if is_not_empty(merchant_key) and is_not_empty(reference_code):
        db_client = create_db_client(caller_info="read_merchant_customer_details")
        with db_client.context():
            merchant_acct = MerchantAcct.fetch(merchant_key)
            customer = Customer.get_by_reference_code(reference_code, merchant_acct) 
        
            if customer:
            
                user_details = customer.registered_user_acct
                customer_details_dict = customer.to_dict(date_format="%d-%m-%Y", datetime_format="%d-%m-%Y %H:%M:%S")
                customer_details_dict['customer_key']               = customer.key_in_str
                customer_details_dict['is_email_verified']          = user_details.is_email_verified
                customer_details_dict['is_mobile_phone_verified']   = user_details.is_mobile_phone_verified
                '''
                if 'entitled_voucher_summary' in customer_details_dict:
                    customer_details_dict['voucher_summary']            = customer.entitled_voucher_summary
                    del customer_details_dict['entitled_voucher_summary']
                '''
        return jsonify(customer_details_dict)
            
    
    else:
        return create_rest_message("Missing merchant account key or user reference code", status_code=StatusCode.BAD_REQUEST)


class AccountActivatedAPIResource(APIBaseResource):  
    
    @auth.login_required
    def post(self):
        username    = auth.current_user()
        
        acct_id     = request.headers.get('x-acct-id')
        api_key     = request.headers.get('x-api-key')
        outlet_key  = request.headers.get('x-outlet-key')
        
        logger.debug('username=%s', username)
        logger.debug('acct_id=%s', acct_id)    
        logger.debug('api_key=%s', api_key)
        logger.debug('outlet_key=%s', outlet_key)
        
        is_valid            = False
        is_authorized       = False
        output_json = {}
        
        if is_not_empty(acct_id) and is_not_empty(api_key):
            db_client = create_db_client(caller_info="AccountActivatedAPIResource.post")
            with db_client.context():
                merchant_acct = MerchantAcct.fetch(acct_id)
                
                #logger.debug('merchant_acct=%s', merchant_acct)
                
                if merchant_acct:
                    logger.debug('merchant_acct api key=%s', merchant_acct.api_key)
                    
                    if api_key == merchant_acct.api_key:
                        merchant_user               = MerchantUser.get_by_username(username)
                        
                        is_authorized = self.is_outlet_authorized(merchant_user, outlet_key)
                        if is_authorized:
                            (expiry_datetime, token)    = self.generate_token(acct_id, username)
                            logger.debug('outlet is_authorized=%s', is_authorized)
                            logger.debug('expiry_datetime=%s', expiry_datetime)
                            
                            output_json =  {
                                            'auth_token'        : token,
                                            'expires_in'        : int(api_conf.API_TOKEN_EXPIRY_LENGTH_IN_MINUTE) * 60,
                                            #'expiry_datetime'   : expiry_datetime.strftime('%d-%m-%Y %h:%M:$S'),
                                            'granted_outlet'    : merchant_user.granted_outlet_details_list,
                                            'username'          : merchant_user.username,
                                            'name'              : merchant_user.name,
                                            'is_admin'          : merchant_user.is_admin,
                                            'granted_access'    : merchant_user.permission.get('granted_access'),
                                            'gravatar_url'      : merchant_user.gravatar_url,
                                            }
                
                            logger.debug('output_json=%s', output_json)
                            
                            is_valid = True
                    
            if is_valid:
                return output_json
            
            elif is_authorized==False:
                abort(400, msg=["User is not authorized due to outlet is not granted"])
                    
        abort(400, msg=["Failed to authenticate"])
        
    
    def is_outlet_authorized(self, merchant_user, outlet_key):
        return True 
    
class AuthenticateAPIResource(APIBaseResource):  
    
    @auth.login_required
    def post(self):
        username    = auth.current_user()
        
        acct_id     = request.headers.get('x-acct-id')
        api_key     = request.headers.get('x-api-key')
        outlet_key  = request.headers.get('x-outlet-key')
        
        logger.debug('acct_id=%s', acct_id)    
        logger.debug('api_key=%s', api_key)
        logger.debug('outlet_key=%s', outlet_key)
        
        is_authenticated    = False
        is_authorized       = False
        output_json = {}
        
        if is_not_empty(acct_id) and is_not_empty(api_key):
            db_client = create_db_client(caller_info="AuthenticateAPIResource.post")
            with db_client.context():
                merchant_acct = MerchantAcct.fetch(acct_id)
            
                if merchant_acct:
                    if api_key == merchant_acct.api_key:
                        merchant_user               = MerchantUser.get_by_username(username)
                        
                        is_authorized = self.is_outlet_authorized(merchant_user, outlet_key)
                        logger.debug('outlet is_authorized=%s', is_authorized)
                        
                        if is_authorized:
                            (expiry_datetime, token)    = self.generate_token(acct_id, username)
                            #session['auth_username']    = username
                            #session['acct_id']          = acct_id
                            
                            logger.debug('token=%s', token)
                            logger.debug('expiry_datetime=%s', expiry_datetime)
                            logger.debug('auth_username=%s', username)
                
                            output_json =  {
                                            'auth_token'        : token,
                                            'expires_in'        : int(api_conf.API_TOKEN_EXPIRY_LENGTH_IN_MINUTE) * 60,
                                            #'expiry_datetime'   : expiry_datetime.strftime('%d-%m-%Y %h:%M:$S'),
                                            'granted_outlet'    : merchant_user.granted_outlet_details_list,
                                            'username'          : merchant_user.username,
                                            'name'              : merchant_user.name,
                                            'is_admin'          : merchant_user.is_admin,
                                            'granted_access'    : merchant_user.permission.get('granted_access'),
                                            'gravatar_url'      : merchant_user.gravatar_url,
                                            }
                
                            logger.debug('output_json=%s', output_json)
                            
                            is_authenticated = True
                    
            if is_authenticated:
                return output_json
            elif is_authorized==False:
                abort(400, msg=["User is not authorized due to outlet is not granted"])
                    
        abort(400, msg=["Failed to authenticate"])
        
    
    def is_outlet_authorized(self, merchant_user, outlet_key):
        return True    

class ProgramDeviceAuthenticate(AccountActivatedAPIResource):
    
    def is_outlet_authorized(self, merchant_user, outlet_key):
        if merchant_user.is_admin:
            logger.debug('it is merchant admin user, thus it is authorized for all outlet')
            return True
        else:
            data_in_json        = request.get_json()
            activation_code     = data_in_json.get('activation_code')
            device_setting      = LoyaltyDeviceSetting.get_by_activation_code(activation_code)
            assigned_outlet_key = device_setting.assigned_outlet_key
            
            logger.debug('device assigned outlet name=%s', device_setting.assigned_outlet_entity.name)
            
            if outlet_key == device_setting.assigned_outlet_key:
                logger.debug('login outlet is same as device setting assigned outlet')
                if outlet_key in merchant_user.granted_outlet:
                    logger.debug('login outlet is authorized by login merchant user granted outlet')
                    if assigned_outlet_key in merchant_user.granted_outlet:
                        logger.debug('device assigned outlet is authorized by login merchant user granted outlet')
                        return True
                    else:
                        logger.debug('device setting assigned outlet is not granted outlet')
                else:
                    logger.debug('login outlet is not granted outlet')    
            else:
                logger.debug('login outlet is not same as device setting assigned outlet')
                        
        return False
            
class POSDeviceAuthenticate(AccountActivatedAPIResource):
    def is_outlet_authorized(self, merchant_user, outlet_key):
        if merchant_user.is_admin:
            return True
        else:
            data_in_json        = request.get_json()
            activation_code     = data_in_json.get('activation_code')
            device_setting      = POSSetting.get_by_activation_code(activation_code)
            assigned_outlet_key = device_setting.assigned_outlet_key
            
            logger.debug('device assigned outlet name=%s', device_setting.assigned_outlet_entity.name)
            
            if outlet_key == device_setting.assigned_outlet_key:
                logger.debug('login outlet is same as device setting assigned outlet')
                if outlet_key in merchant_user.granted_outlet:
                    logger.debug('login outlet is authorized by login merchant user granted outlet')
                    if assigned_outlet_key in merchant_user.granted_outlet:
                        logger.debug('device assigned outlet is authorized by login merchant user granted outlet')
                        return True
                    else:
                        logger.debug('device setting assigned outlet is not granted outlet')
                else:
                    logger.debug('login outlet is not granted outlet')    
            else:
                logger.debug('login outlet is not same as device setting assigned outlet')
        
        return False            

class SecureAPIResource(AuthenticateAPIResource):  
    
    def __init__(self):
        super(SecureAPIResource, self).__init__()  
    
    
class CheckAuthTokenResource(SecureAPIResource):
    
    @auth_token_required
    def get(self):
        return 'Ping'             
    
     
merchant_api.add_resource(AuthenticateAPIResource,       '/auth')
merchant_api.add_resource(ProgramDeviceAuthenticate,     '/program-auth')
merchant_api.add_resource(POSDeviceAuthenticate,         '/pos-auth')      
    
        
        
        
        