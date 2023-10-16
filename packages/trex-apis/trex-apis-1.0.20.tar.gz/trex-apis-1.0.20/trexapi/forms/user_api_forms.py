from wtforms import StringField, PasswordField, validators, DateField
from trexadmin.forms.base_forms import ValidationBaseForm
from trexadmin.libs.wtforms import validators as custom_validator
from flask_babel import gettext
from datetime import date
from wtforms.fields.core import FloatField

class UserMinForm(ValidationBaseForm):
    name                = StringField(gettext('Name'), validators=[
                                        validators.InputRequired(gettext('Name is required')),
                                        validators.Length(min=3, max=300, message='Name length must be within 3 and 300 characters'),
                                        
                                        ]
                                        )
    mobile_phone        = StringField('Mobile Phone', validators=[
                                        #validators.InputRequired(gettext('Mobile Phone is required')),
                                        ]
                                        )
    
    gender              = StringField('Gender', validators=[
                                        validators.InputRequired(gettext('Gender is required')),
                                        ]
                                        )
    
    birth_date          = StringField('Mobile Phone', validators=[
                                        validators.InputRequired(gettext('Birth date is required')),
                                        ]
                                        )
    
    
    
class UserRegistrationForm(UserMinForm):
    email               = StringField('Email Address', validators=[
                                        validators.Email(gettext("Please enter valid email address.")),
                                        validators.InputRequired(gettext('Email is required')),
                                        ]
                                        )
    
    password            = StringField(gettext('Password'), validators=[
                                        validators.InputRequired(gettext('Password is required')),
                                        
                                        ]
                                        )  
    
class UserUpdateForm(UserMinForm):
    reference_code      = StringField('User Reference Code', validators=[
                                        validators.InputRequired(gettext('User Reference Code is required')),
                                        ]
                                        )      
    
class OutletReviewsForm(ValidationBaseForm):
    outlet_key               = StringField('Outlet Key', validators=[
                                        validators.InputRequired(gettext('Outlet key is required')),
                                        ]
                                        )
    
    food_score               = FloatField('Food Score', validators=[
                                        validators.InputRequired(gettext('Food score is required')),
                                        ]
                                        )
    
    service_score               = FloatField('Service Score', validators=[
                                        validators.InputRequired(gettext('Service score is required')),
                                        ]
                                        )
    
    ambience_score          = FloatField('Ambience Score', validators=[
                                        validators.InputRequired(gettext('Ambience score is required')),
                                        ]
                                        )
    
    value_for_money_score   = FloatField('Value for money Score', validators=[
                                        validators.InputRequired(gettext('Value for money score is required')),
                                        ]
                                        )    