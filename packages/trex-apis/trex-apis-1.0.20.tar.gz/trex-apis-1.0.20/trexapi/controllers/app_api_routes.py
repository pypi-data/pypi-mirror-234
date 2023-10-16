from flask import Blueprint, request
import logging
from trexlib.utils.log_util import get_tracelog
from trexmodel.utils.model.model_util import create_db_client
from datetime import datetime
from trexlib.utils.string_util import is_not_empty
from trexmodel.models.datastore.user_models import User
from trexadmin.libs.http import create_rest_message
from trexadmin.libs.http import StatusCode
from werkzeug.datastructures import ImmutableMultiDict
from trexapi.forms.user_api_forms import UserRegistrationForm
from trexapi.conf import APPLICATION_NAME, APPLICATION_BASE_URL
from trexmail.email_helper import trigger_send_email
from trexmodel.models.datastore.app_models import AppPromotion, AppMessage
from trexmodel.models.datastore.admin_models import AppBannerFile
 
from trexlib.utils.common.common_util import sort_dict_list
from flask.json import jsonify

app_api_bp = Blueprint('app_api_bp', __name__,
                                 template_folder='templates',
                                 static_folder='static',
                                 url_prefix='/api/v1/app')

logger = logging.getLogger('debug')


@app_api_bp.route('/ping', methods=['GET'])
def ping():
    return 'pong', 200

@app_api_bp.route('/app-package-info/app/<app_name>/platform/<platform>', methods=['GET'])
def app_package_info(app_name, platform):
    logger.debug('---app_package_info---')
    
    logger.info('app_name=%s, plaform=%s', app_name, platform)
    package_info = {}
    
    if platform=='android':
        if app_name == 'memberasia':
            package_info =  {
                        'app_name'      : app_name,
                        'platform'      : platform,
                        'version'       : '1.0.0',
                        'can_update'    : False,
                        'update_url'    : '',    
        
                    }
        elif app_name == 'memberla':
            package_info =  {
                        'app_name'      : app_name,
                        'platform'      : platform,
                        'version'       : '1.0.1',
                        'can_update'    : True,
                        'update_url'    : 'https://play.google.com/store/apps/details?id=com.augmigo.memberla',
        
                    }
        
    elif platform=='ios':
        
        if app_name == 'memberasia':
            package_info =  {
                        'app_name'      : app_name,
                        'platform'      : platform,
                        'version'       : '1.0.0',
                        'can_update'    : False,
                        'update_url'    : '',
        
                    }
        elif app_name == 'memberla':
            package_info =  {
                        'app_name'      : app_name,
                        'platform'      : platform,
                        'version'       : '1.0.1',
                        'can_update'    : False,
                        'update_url'    : '',
        
                    }
            
    elif platform=='window':
        
        if app_name == 'memberasia':
            package_info =  {
                        'app_name'      : app_name,
                        'platform'      : platform,
                        'version'       : '1.0.0',
                        'can_update'    : False,
                        'update_url'    : '',
        
                    }
        elif app_name == 'memberla':
            package_info =  {
                        'app_name'      : app_name,
                        'platform'      : platform,
                        'version'       : '1.0.1',
                        'can_update'    : False,
                        'update_url'    : '',
        
                    }        
               
    return package_info

@app_api_bp.route('/settings', methods=['GET'])
def app_setting():
    logger.debug('---app_setting---')
    
    banner_file_list = []
    db_client = create_db_client(caller_info="app_setting")
    with db_client.context():
        
        result_listing = AppBannerFile.list()
        logger.debug('result_listing=%s', result_listing)
                
        if result_listing:
            for banner_file in result_listing:
                #banner_file_list.append(banner_file.to_dict(dict_properties=['banner_file_public_url','sequence'], show_key=False))
                banner_file_list.append({
                                        'image_url': banner_file.banner_file_public_url,
                                        'sequence': banner_file.sequence,
                                        })
                
    ##sorted_banner_file_list = sort_dict_list(banner_file_list, sort_attr_name='sequence')
    
    app_settings =  {
                        'banners': banner_file_list,
        
                    }
    '''
    return create_rest_message(status_code=StatusCode.OK,
                                               **app_settings,
                                               )
    '''
    return app_settings

@app_api_bp.route('/promotions', methods=['GET'])
def list_app_promotions():
    logger.debug('---list_app_promotions---')
    result_listing = [
            
            {
                'title':'GoodTaste',
                'content':'10% Discount for member during June 2023',
            },
            {
                'title':'Anviet',
                'content':'Entitled RM10 cash voucher for miniumum RM50 spending per receipt during June 2023',
            }
            
        
        ]
    '''
    db_client = create_db_client(caller_info="list_app_promotions")
    with db_client.context():
        
        result_listing = AppPromotion.list()
        logger.debug('result_listing=%s', result_listing)
    '''
    
        
    return jsonify({
            'promotions': result_listing,
            })
    
@app_api_bp.route('/messages', methods=['GET'])
def list_app_messages():
    logger.debug('---list_app_messages---')
    result_listing = [
            {
                'title':'Welcome',
                'content':'Welcome on board',
            }
        ]
    '''
    db_client = create_db_client(caller_info="list_app_highlights")
    with db_client.context():
        
        result_listing = AppMessage.list()
        logger.debug('result_listing=%s', result_listing)
    '''
    
        
    return jsonify({
            'messages': result_listing,
            })    
