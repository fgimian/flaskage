import os
import logging

import click
from painter import paint

from .utils import valid_underscore_name

LOGGING_COLOR_MAPPING = {
    'identical': paint.light_blue,
    'exist': paint.light_blue,
    'conflict': paint.light_red,
    'create': paint.light_green,
    'update': paint.light_yellow
}

COLUMN_TYPE_MAPPING = {
    'integer': 'Integer',
    'decimal': 'Numeric',
    'float': 'Float',
    'boolean': 'Boolean',
    'date': 'Date',
    'time': 'Time',
    'datetime': 'DateTime',
    'binary': 'LargeBinary',
    'string': 'String',
    'text': 'Text'
}
COLUMN_TYPE_MAPPING.update({
    'int': COLUMN_TYPE_MAPPING['integer'],
    'bool': COLUMN_TYPE_MAPPING['boolean'],
    'bin': COLUMN_TYPE_MAPPING['binary'],
    'str': COLUMN_TYPE_MAPPING['string']
})

COLUMN_TYPE_DEFAULT = 'string'
COLUMN_TYPES_SUPPORTING_LENGTH = ['string', 'text', 'binary']

COLUMN_FACTORY_MAPPING = {
    'integer': {
        '*': 'fake.random_int()'
    },
    'decimal': {
        '*': 'fake.pyfloat()'
    },
    'float': {
        '*': 'fake.pyfloat()'
    },
    'boolean': {
        '*': 'fake.boolean()'
    },
    'date': {
        '*': 'fake.date_time().date()'
    },
    'time': {
        '*': 'fake.date_time().time()'
    },
    'datetime': {
        '*': 'fake.date_time()'
    },
    'binary': {
        '*': "'test binary data'"
    },
    'string': {
        '*': 'fake.word()',
        'user_name': 'fake.user_name()',
        'password': 'fake.password()',

        'first_name': 'fake.first_name()',
        'last_name': 'fake.last_name()',
        'name': 'fake.name()',
        'job': 'fake.job()',
        'email': 'fake.email()',

        'address': 'fake.address()',
        'secondary_address': 'fake.secondary_address()',
        'building_number': 'fake.building_number()',
        'street_name': 'fake.street_name()',
        'street_address': 'fake.street_address()',
        'city': 'fake.city()',
        'state': 'fake.state()',
        'state_abbr': 'fake.state_abbr()',
        'postcode': 'fake.postcode()',
        'country': 'fake.country()',
        'country_code': 'fake.country_code()',
        'phone_number': 'fake.phone_number()',

        'credit_card_number': 'fake.credit_card_number()',
        'credit_card_provider': 'fake.credit_card_provider()',
        'credit_card_expire': 'fake.credit_card_expire()',
        'credit_card_security_code': 'fake.credit_card_security_code()',

        'company': 'fake.company()',
        'company_email': 'fake.company_email()',

        'timezone': 'fake.timezone()',
        'locale': 'fake.locale()',
        'language_code': 'fake.language_code()',

        'uri': 'fake.uri()',
        'uri_path': 'fake.uri_path()',
        'url': 'fake.url()',
        'domain_name': 'fake.domain_name()'
    },
    'text': {
        '*': 'text'
    },
}
COLUMN_FACTORY_MAPPING['string'].update({
    'username': COLUMN_FACTORY_MAPPING['string']['user_name'],
    'full_name': COLUMN_FACTORY_MAPPING['string']['name'],
    'occupation': COLUMN_FACTORY_MAPPING['string']['job'],
    'email_address': COLUMN_FACTORY_MAPPING['string']['email'],

    'building_no': COLUMN_FACTORY_MAPPING['string']['building_number'],
    'street_number': COLUMN_FACTORY_MAPPING['string']['building_number'],
    'street_no': COLUMN_FACTORY_MAPPING['string']['building_number'],
    'state_abbreviation': COLUMN_FACTORY_MAPPING['string']['state_abbr'],
    'phone': COLUMN_FACTORY_MAPPING['string']['phone_number'],

    'credit_card': COLUMN_FACTORY_MAPPING['string']['credit_card_number'],

    'business_name': COLUMN_FACTORY_MAPPING['string']['company'],
    'business_email': COLUMN_FACTORY_MAPPING['string']['company_email'],
    'organisation_name': COLUMN_FACTORY_MAPPING['string']['company'],
    'organisation_email': COLUMN_FACTORY_MAPPING['string']['company_email'],
    'organization_name': COLUMN_FACTORY_MAPPING['string']['company'],
    'organization_email': COLUMN_FACTORY_MAPPING['string']['company_email'],

    'domain': COLUMN_FACTORY_MAPPING['string']['domain_name']
})

COLUMN_MODIFIER_MAPPING = {
    'index': 'index=True',
    'primary': 'primary_key=True',
    'required': 'nullable=False',
    'unique': 'unique=True'
}
COLUMN_MODIFIER_PRIMARY_KEY = 'primary'


def valid_project_directory(directory=os.getcwd()):
    return (
        os.path.isdir(os.path.join(directory, 'app')) and
        os.path.isdir(os.path.join(directory, 'app', 'models')) and
        os.path.isdir(os.path.join(directory, 'app', 'static')) and
        os.path.isdir(os.path.join(directory, 'app', 'templates')) and
        os.path.isdir(os.path.join(directory, 'app', 'views')) and
        os.path.isdir(os.path.join(directory, 'db', 'migrations')) and
        os.path.isdir(os.path.join(directory, 'test')) and
        os.path.isfile(os.path.join(directory, 'manage.py'))
    )


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        if self.use_color:
            color = LOGGING_COLOR_MAPPING[record.description]
            record.description = color(record.description)
        return logging.Formatter.format(self, record)


class ProjectNameParamType(click.ParamType):
    name = 'project_name'

    def convert(self, value, param, ctx):
        name = os.path.basename(value)
        directory = os.path.join(
            os.path.dirname(value), name.replace('_', '-')
        )
        if valid_underscore_name(name):
            return (name, directory)
        else:
            self.fail('%s is not a valid project name' % name, param, ctx)

    def __repr__(self):
        return 'PROJECT_NAME'


class ModelColumnParamType(click.ParamType):
    name = 'model_column'

    def convert(self, value, param, ctx):
        # Split the column definition up
        column_properties = value.split(':')

        # Extract and validate the column name
        name = column_properties[0]
        if not valid_underscore_name(name):
            ctx.fail('The name provided is not a valid variable name')

        # Extract and validate the column type and length
        try:
            type_properties = column_properties[1].split(',')
            type = type_properties[0].lower() or COLUMN_TYPE_DEFAULT
        except IndexError:
            type_properties = []
            type = COLUMN_TYPE_DEFAULT

        if type not in COLUMN_TYPE_MAPPING:
            ctx.fail('The type specified for column %s is invalid' % name)

        try:
            if type_properties[1]:
                length = int(type_properties[1])
            else:
                length = None
        except IndexError:
            length = None
        except ValueError:
            ctx.fail('The length specified for column %s is invalid' % name)

        if length and type not in COLUMN_TYPES_SUPPORTING_LENGTH:
            ctx.fail(
                'The length specified for column %s is not allowed for %s '
                'types' % (name, type)
            )

        # Extract and validate the column modifiers
        try:
            modifiers = column_properties[2].lower().split(',')
        except IndexError:
            modifiers = []

        for modifier in modifiers:
            if modifier not in COLUMN_MODIFIER_MAPPING:
                ctx.fail(
                    'The column modifier %s for column %s is invalid' %
                    (modifier, name)
                )

        return name, type, length, modifiers

    def __repr__(self):
        return 'MODEL_COLUMN'

PROJECT_NAME = ProjectNameParamType()
MODEL_COLUMN = ModelColumnParamType()
