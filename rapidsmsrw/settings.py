# Django settings for rapidsmsrw1000 project.

import os
import sys

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            ''))
PROJECT_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))
### IMPORT FOR IMINSI-GIHUMBI OBJECTS TRANSLATION
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'scripts'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'packages'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, ''))


DEBUG = True
TEMPLATE_DEBUG = DEBUG
TRAINING_ENV = True
SHORTCODE = "3104"
PRIMARY_BACKEND = 'kannel-smpp'
SERVER_IP = '127.0.0.1'
SERVER_PORT = '5000'
POST_URL="http://%s:%s/backend/%s" % (SERVER_IP, SERVER_PORT, PRIMARY_BACKEND) 

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'thousanddays',
        'USER': 'thousanddays',
	'PASSWORD': 'thousanddays',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

###USE MEMCACHED

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#    }
#}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Africa/Kigali'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
LANGUAGES = (('rw', 'Kinyarwanda'), ('en', 'English'), ('fr', 'Francais'))

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'public', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'public', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
    
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'hei&amp;p)mzo_k(ydn&amp;1mt0i%d8f%li22wk^ka_d^(1h2o3@lg(n9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'django.middleware.cache.UpdateCacheMiddleware',
#    'django.middleware.common.CommonMiddleware',
#    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'urls'
#BASE_TEMPLATE = 'layout.html'
# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
    os.path.join(PROJECT_PATH, 'rapidsmsrw/webapp/templates'),
    
    
)

FIXTURE_DIRS = (
    os.path.join(PROJECT_PATH, 'fixtures'),
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'basic': {
            'format': '%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'basic',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'basic',
            'filename': os.path.join(PROJECT_PATH, 'logs/rapidsms.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'blockingrouter': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'flexselect',
    #'django.contrib.humanize',
    # External apps
    "django_nose",
    "djtables",
    "rapidsms",
    "rapidsms.contrib.handlers",
    "rapidsms.contrib.default",
    "rapidsms.contrib.export",
    #"rapidsms.contrib.httptester",
    #"rapidsms.contrib.locations",
    #"rapidsms.contrib.messagelog",
    #"rapidsms.contrib.messaging",
    #"rapidsms.contrib.registration",
    #"rapidsms.contrib.scheduler",
    #"rapidsms.contrib.echo",

	#DEVELOPED APPS
	"api",
	"api.messagelog",
	"api.chws",
	"api.messaging",
        "api.providers",
	"api.rwmigrator",
	
	
	
)

KANNEL_CONF = {'kannel_host':'127.0.0.1',
		 'kannel_port':13013, 
			'kannel_password':'kannel_smpp',
			 'kannel_username':'kannel_smpp'}

INSTALLED_BACKENDS = {
    #"message_tester": {
    #    "ENGINE": "rapidsms.contrib.httptester.backend",
    #},

    "kannel-smpp" : {
        "ENGINE":  "rapidsms.backends.kannel.outgoing",
        "sendsms_url": "http://127.0.0.1:13013/cgi-bin/sendsms",
        "sendsms_params": {"smsc": "smpp",
                           "from": SHORTCODE, # not set automatically by SMSC
                           "username": "moh_2015_kannel",
                           "password": "moh_2015_kannel_pwd"}, # or set in localsettings.py
        "coding": 0,
        "charset": "ascii",
        "encode_errors": "ignore", # strip out unknown (unicode) characters
    },

    "kannel-fake-smsc" : {
        "ENGINE":  "rapidsms.backends.kannel.outgoing",
        "sendsms_url": "http://127.0.0.1:13013/cgi-bin/sendsms",
        "sendsms_params": {"smsc": "FAKE",
                           "from": "123", # not set automatically by SMSC
                           "username": "kannel",
                           "password": "kannel"}, # or set in localsettings.py
        "coding": 0,
        "charset": "ascii",
        "encode_errors": "ignore", # strip out unknown (unicode) characters
    },
}

RHEA = {'api': { 	#'host' : '41.74.172.115', 
			'host': '197.243.18.22',
			'key_file' : 'mule.pem',
			'cer_file ': 'mule.cer',
			'port' : 5000,
			'level' : 'info',
			'file' : '/var/log/rheaapi.log',
			'timeout' : '10',
			'group' : 'RHEA',
			'user' : 'svr_rapidsms',
			'pass' : 'pCBv5r7MLYO3', }
}

# this rapidsms-specific setting defines which views are linked by the
# tabbed navigation. when adding an app to INSTALLED_APPS, you may wish
# to add it here, also, to expose it in the rapidsms ui.
RAPIDSMS_TABS = [
    #("rapidsms.contrib.messagelog.views.message_log",       "Message Log"),
    #("rapidsms.contrib.registration.views.registration",    "Registration"),
    #("rapidsms.contrib.messaging.views.messaging",          "Messaging"),
    #("rapidsms.contrib.locations.views.locations",          "Map"),
    #("rapidsms.contrib.scheduler.views.index",              "Event Scheduler"),
    #("rapidsms.contrib.httptester.views.generate_identity", "Message Tester"),
]


#### ALLOW DJANGO FLEXIBLE SELECTION OPTIONS

FLEXSELECT = {
    'include_jquery': True,
}


LOGIN_REDIRECT_URL = '/'

GESTATION       	     = 277
MOTHER_TRACK_GESTATION       = 350

TABLE_MAP = {
		  'PRE':  'pregmessage',
		  'REF':  'refmessage',
		  'ANC':  'ancmessage',
		  'DEP':  'depmessage',
		  'RISK': 'riskmessage',
		  'RED':  'redmessage',
		  'BIR':  'birmessage',
		  'CHI':  'childmessage',
		  'DTH':  'deathmessage',
		  'RES':  'resultmessage',
		  'RAR':  'redresultmessage',
		  'NBC':  'nbcmessage',
		  'PNC':  'pncmessage',
		  'CCM':  'ccmmessage',
		  'CMR':  'cmrmessage',
		  'CBN':  'cbnmessage',
		}
KEYS_MAP = {
		'nid' :	'indangamuntu',
		'md':	'death',
		'nd':	'death',
		'cd':	'death',
		'anc2': 'anc_visit',	
		'anc3': 'anc_visit',	
		'anc4': 'anc_visit',
		'pnc1': 'pnc_visit',	
		'pnc2': 'pnc_visit',	
		'pnc3': 'pnc_visit',
		'nbc1': 'nbc_visit',	
		'nbc2': 'nbc_visit',	
		'nbc3': 'nbc_visit',
		'nbc4': 'nbc_visit',	
		'nbc5': 'nbc_visit',
		'v1': 'vaccine',
		'v2': 'vaccine',
		'v3': 'vaccine',
		'v4': 'vaccine',
		'v5': 'vaccine',
		'v6': 'vaccine',
		'vc': 'vacc_completion',
		'vi': 'vacc_completion',
		'nv': 'vacc_completion',		
		}
NUMBER_KEYS_MAP = {
			'anc2': 2,	
			'anc3': 3,	
			'anc4': 4,
			'pnc1': 1,	
			'pnc2': 2,	
			'pnc3': 3,
			'nbc1': 1,	
			'nbc2': 2,	
			'nbc3': 3,
			'nbc4': 4,	
			'nbc5': 5,
			'v1': 1,
			'v2': 2,
			'v3': 3,
			'v4': 4,
			'v5': 5,
			'v6': 6,
			}

