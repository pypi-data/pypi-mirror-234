'''
Created on 1 Jul 2021

@author: jacklok
'''
from functools import wraps
from flask import request, session, abort
from trexlib.utils.string_util import is_not_empty
from trexlib.utils.crypto_util import decrypt_json
import logging
from datetime import datetime
from trexlib.utils.log_util import get_tracelog
from trexadmin.libs.http import create_rest_message, StatusCode

logger = logging.getLogger('decorator')
#logger = logging.getLogger('debug')

def test_session_expired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return ("Authenticated token is expired", 401)
    
    return decorated_function

def auth_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token  = request.headers.get('x-auth-token')
        acct_id     = request.headers.get('x-acct-id')
            
        logger.debug('acct_id=%s', acct_id)
        logger.debug('auth_token=%s', auth_token)
        
        if is_not_empty(auth_token):
            try:
                auth_details_json = decrypt_json(auth_token)
            except:
                logger.error('Authenticated token is not valid')
                return ("Authenticated token is not valid", 401)
            
            logger.debug('auth_details_json=%s', auth_details_json)
            
            if auth_details_json:
                expiry_datetime     = auth_details_json.get('expiry_datetime')
                acct_id_from_token  = auth_details_json.get('acct_id')
                
                logger.debug('acct_id from decrypted token=%s', acct_id_from_token)
                logger.debug('expiry_datetime from decrypted token=%s', expiry_datetime)
                
                if is_not_empty(expiry_datetime) and is_not_empty(acct_id_from_token) and acct_id==acct_id_from_token:
                    expiry_datetime = datetime.strptime(expiry_datetime, '%d-%m-%Y %H:%M:%S')
                    logger.debug('expiry_datetime=%s', expiry_datetime)
                    
                    now             = datetime.now()
                    if now < expiry_datetime: 
                        logger.debug('auth token is still valid')
                        return f(*args, **kwargs)
                    else:
                        logger.debug('auth token is not logger valid')
                        
                        return ("Authenticated token is expired", 401)
                else:
                    return ("Authenticated token is invalid", 401)
        
        return ("Authenticated token is required", 401)

    return decorated_function

def user_auth_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_auth_token     = request.headers.get('x-auth-token')
        user_reference_code = request.headers.get('x-reference-code')
            
        logger.debug('user_auth_token=%s', user_auth_token)
        
        if is_not_empty(user_auth_token):
            logger.debug('user_auth_token is not empty, going to decrypt it')
            try:
                auth_details_json = decrypt_json(user_auth_token)
                logger.debug('auth_details_json=%s', auth_details_json)
                
            except:
                logger.error('Failed due to %s', get_tracelog())
                return ("Authenticated token is not valid", 401)
            
            
            
            if auth_details_json:
                expiry_datetime                 = auth_details_json.get('expiry_datetime')
                user_reference_code_from_token  = auth_details_json.get('reference_code')
                
                if is_not_empty(expiry_datetime) and is_not_empty(user_reference_code_from_token) and user_reference_code_from_token == user_reference_code:
                    expiry_datetime = datetime.strptime(expiry_datetime, '%d-%m-%Y %H:%M:%S')
                    logger.debug('expiry_datetime=%s', expiry_datetime)
                    
                    now             = datetime.now()
                    if now < expiry_datetime: 
                        logger.debug('auth token is still valid')
                        return f(*args, **kwargs)
                    else:
                        logger.debug('auth token is not logger valid')
                        
                        #return ("Authenticated token is expired", 401)
                        return create_rest_message('Authenticated token is expired', status_code=StatusCode.UNAUTHORIZED,)
            else:
                #return ("Authenticated token is invalid", 401)    
                return create_rest_message('Authenticated token is invalid', status_code=StatusCode.UNAUTHORIZED,)
        
        #return ("Authenticated token is required", 401)
        return create_rest_message('Authenticated token is required', status_code=StatusCode.UNAUTHORIZED,)

    return decorated_function

def outlet_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        outlet_key = request.headers.get('x-outlet-key')
            
        logger.debug('outlet_key=%s', outlet_key)
        
        if is_not_empty(outlet_key):
            logger.debug('Going to execute')
            return f(*args, **kwargs)
            
        
        return ("Outlet Key is required", 401)

    return decorated_function

def merchant_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        acct_id = request.headers.get('x-acct-id')
            
        logger.debug('acct_id=%s', acct_id)
        
        if is_not_empty(acct_id):
            logger.debug('Going to execute')
            return f(*args, **kwargs)
            
        
        return ("Merchant account id is required", 401)

    return decorated_function
