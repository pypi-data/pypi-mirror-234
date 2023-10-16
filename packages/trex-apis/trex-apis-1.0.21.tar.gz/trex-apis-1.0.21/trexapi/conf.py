'''
Created on 30 Jun 2021

@author: jacklok
'''
import os
APPLICATION_NAME                                                = os.environ.get('APPLICATION_NAME')
MOBILE_APP_NAME                                                 = os.environ.get('MOBILE_APP_NAME')
APPLICATION_BASE_URL                                            = os.environ.get('APPLICATION_BASE_URL')
SECRET_KEY                                                      = os.environ.get('SECRET_KEY')
VERSION                                                         = '0.0.1'
UPDATED_DATE                                                    = '5 July 2021'

API_TOKEN_EXPIRY_LENGTH_IN_MINUTE                               = os.environ.get('API_TOKEN_EXPIRY_LENGTH_IN_MINUTE') 

API_ERR_CODE_INVALID_ACTIVATION_CODE                            = 'invalid.activation.code';

EARN_INSTANT_REWARD_URL                                         = os.environ.get('EARN_INSTANT_REWARD_URL')

LUCKY_DRAW_URL                                                  = os.environ.get('LUCKY_DRAW_URL')
