'''
Created on 8 Jul 2021

@author: jacklok
'''
from flask import request
import logging
from trexlib.utils.crypto_util import decrypt_json
from datetime import datetime, timedelta
from trexapi import conf as api_conf
from trexlib.utils.crypto_util import encrypt_json

logger = logging.getLogger('helper')


def get_logged_in_api_username():
    auth_token  = request.headers.get('x-auth-token')
    username    = None
    try:
        auth_details_json = decrypt_json(auth_token)
    except:
        logger.error('Failed to decrypt authenticated token')
        
    logger.debug('auth_details_json=%s', auth_details_json)
    
    if auth_details_json:
        username = auth_details_json.get('username')
        
    return username

def generate_user_auth_token(acct_id, reference_code):
    expiry_datetime = datetime.now() + timedelta(minutes = int(api_conf.API_TOKEN_EXPIRY_LENGTH_IN_MINUTE))
    
    logger.debug('expiry_datetime=%s', expiry_datetime)
    
    token_content =  {
                        'acct_id'           : acct_id,
                        'reference_code'    : reference_code,
                        'expiry_datetime'   : expiry_datetime.strftime('%d-%m-%Y %H:%M:%S'),
                        }
    
    logger.debug('token_content=%s', token_content)
    
    return (expiry_datetime, encrypt_json(token_content))
