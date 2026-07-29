import os
from pathlib import Path
from dotenv import load_dotenv
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-&_4^2x8@qp*wq(&^8%ub&&=-!k^1(#mr0mqjmh+e9#x$4_vdbp')

if not DEBUG:
    # --- Cookie Security ---
    # CSRF_COOKIE_HTTPONLY prevents XSS from stealing the CSRF token.
    # _SECURE flags ensure cookies are only sent over encrypted HTTPS connections.
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

    # --- SSL/TLS & HSTS ---
    # Redirects all HTTP traffic to HTTPS and mandates secure connections via HSTS.
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year in seconds
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # --- Proxy/Load Balancer Configuration ---
    # Essential for platforms like PythonAnywhere to correctly identify HTTPS requests.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # --- Browser & Content Security ---
    # Prevents clickjacking (DENY) and forces browsers to respect MIME types.
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True


# Custom error handlers
handler400 = 'core.views.bad_request'
handler403 = 'core.views.permission_denied'
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'

ALLOWED_HOSTS = ['agentflow.pythonanywhere.com']


# ================== UNFOLD CALLBACK FUNCTIONS ==================
# We define these before the UNFOLD dict so they can be referenced
# directly as Python callables instead of problematic string paths.

def dashboard_callback(request, context):
    """
    Injects context data into index.html
    """
    context.update({
        "sample": "example",
    })
    return context


def environment_callback(request):
    """
    Displays current deployment tier
    """
    return ["Production", "danger"]


def environment_title_prefix_callback(request):
    """
    Prepends to the browser tab title
    """
    return "[PROD] "


def badge_callback(request):
    """
    Returns total badge notifications (dynamic count)
    """
    return 3


def permission_callback(request):
    """
    Determines user rights dynamically for tab structures
    """
    return request.user.has_perm("accounts.change_user")


# ===============================================================


# Application definition
INSTALLED_APPS = [
    # Unfold (Must be loaded before django.contrib.admin)
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "unfold.contrib.location_field",
    "unfold.contrib.constance",
    "unfold.contrib.hijack",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'crispy_forms',
    'crispy_bootstrap5',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django.contrib.humanize',
    'dj_urls_panel',
    'dj_signals_panel',
    "dj_control_room_base",
    "dj_control_room",

    # Local apps
    'accounts',
    'core',
    'inventory',
    'purchases',
    'sales',
    # 'chat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'accounts.middleware.ActivityLogMiddleware',  # Custom middleware
]

ROOT_URLCONF = 'agentflow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.user_permissions',  # Permissions handling
            ],
        },
    },
]

WSGI_APPLICATION = 'agentflow.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'database' / 'data.sqlite3',
    }
}

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Dar_es_Salaam'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
# Where collectstatic will put all static files for production
STATIC_ROOT = BASE_DIR / "staticfiles"

# Extra places Django will look for static files
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# see https://help.pythonanywhere.com/pages/DjangoStaticFiles for more info
MEDIA_ROOT = '/media/'
# MEDIA_URL = '/home/agentflow/agentflow/media/'
# STATIC_ROOT = '/home/agentflow/agentflow/staticfiles'


STORAGES = {
    "default":{
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

WHITENOISE_MANIFEST_STRICT = False


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Consolidated Authentication settings
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'sales:pos_table'
LOGOUT_REDIRECT_URL = 'accounts:login'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Email settings (for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Session settings
SESSION_COOKIE_AGE = 28800  # 8 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


#===================== UNFOLD-CONFIGURATIONS ============================
UNFOLD = {
    "SITE_TITLE": "AgentFlow System",
    "SITE_HEADER": "AgentFlow Secretariat",
    "SITE_URL": "/",
    "SITE_ICON": "/static/favicon.png",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
}
#========================================================================


##################
#   Dj-doom      #
##################

DJ_DOOM_PANEL_SETTINGS = {
    "ALLOWED_GROUPS": [],
    "REQUIRE_SUPERUSER": False,
    "LOAD_DEFAULT_CSS": True,
    "EXTRA_CSS": [],
}