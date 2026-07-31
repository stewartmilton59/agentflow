import os
from pathlib import Path
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def get_env_var(key, default=None, mandatory=False):
    value = os.environ.get(key)
    if value is not None:
        return value
    if mandatory:
        raise ImproperlyConfigured(f"Required environment variable '{key}' is not set.")
    return default


# -----------------------------------------------------------------
# Security
# -----------------------------------------------------------------
SECRET_KEY = get_env_var('SECRET_KEY', mandatory=True)

DEBUG = get_env_var('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = get_env_var('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

CSRF_TRUSTED_ORIGINS = get_env_var('CSRF_TRUSTED_ORIGINS', 'http://localhost:8000,http://127.0.0.1:8000').split(',')

SECURE_SSL_REDIRECT = get_env_var('SECURE_SSL_REDIRECT', 'False') == 'True'
SESSION_COOKIE_SECURE = get_env_var('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = get_env_var('CSRF_COOKIE_SECURE', 'False') == 'True'
SECURE_HSTS_SECONDS = int(get_env_var('SECURE_HSTS_SECONDS', '0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = get_env_var('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'False') == 'True'
SECURE_HSTS_PRELOAD = get_env_var('SECURE_HSTS_PRELOAD', 'False') == 'True'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
X_FRAME_OPTIONS = 'DENY'

# Custom error handlers
handler400 = 'core.views.bad_request'
handler403 = 'core.views.permission_denied'
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'


# -----------------------------------------------------------------
# Application list
# -----------------------------------------------------------------
INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    'crispy_bootstrap5',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django.contrib.humanize',

    'accounts',
    'core',
    'inventory',
    'purchases',
    'sales',
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
    'accounts.middleware.ActivityLogMiddleware',
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
                'core.context_processors.user_permissions',
            ],
        },
    },
]

WSGI_APPLICATION = 'agentflow.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': get_env_var('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': get_env_var('DB_NAME', BASE_DIR / 'database' / 'data.sqlite3'),
        'USER': get_env_var('DB_USER', ''),
        'PASSWORD': get_env_var('DB_PASSWORD', ''),
        'HOST': get_env_var('DB_HOST', ''),
        'PORT': get_env_var('DB_PORT', ''),
        'OPTIONS': {
            'charset': 'utf8mb4',
        } if get_env_var('DB_ENGINE', '').endswith('mysql') else {},
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

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'sales:pos_table'
LOGOUT_REDIRECT_URL = 'accounts:login'

CACHES = {
    'default': {
        'BACKEND': get_env_var('CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache'),
        'LOCATION': get_env_var('CACHE_LOCATION', 'unique-snowflake'),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django_errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'sales': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Email settings
EMAIL_BACKEND = get_env_var('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = get_env_var('EMAIL_HOST', '')
EMAIL_PORT = int(get_env_var('EMAIL_PORT', '587'))
EMAIL_USE_TLS = get_env_var('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = get_env_var('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = get_env_var('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = get_env_var('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
SERVER_EMAIL = get_env_var('SERVER_EMAIL', 'root@localhost')
ADMINS = [('Admin', get_env_var('ADMIN_EMAIL', ''))] if get_env_var('ADMIN_EMAIL', '') else []

# Session settings
SESSION_COOKIE_AGE = 28800  # 8 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Django Jazzmin
JAZZMIN_SETTINGS = {
    "site_title": "AgentFlow Admin",
    "site_header": "AgentFlow",
    "site_brand": "AgentFlow",
    "welcome_sign": "Welcome to AgentFlow Admin",
    "copyright": "AgentFlow Ltd",
    "site_logo_classes": "img-circle",
    "links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "POS", "url": "sales:pos_table", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": [
        "auth",
        "accounts",
        "core",
        "inventory",
        "purchases",
        "sales",
    ],
    "icons": {
        "auth": "fas fa-shield-alt",
        "auth.Group": "fas fa-users",
        "accounts.User": "fas fa-user-shield",
        "accounts.UserProfile": "fas fa-id-card",
        "accounts.UserActivityLog": "fas fa-history",
        "accounts.LoginAttempt": "fas fa-lock",
        "core.Company": "fas fa-building",
        "core.Branch": "fas fa-code-branch",
        "core.SystemSetting": "fas fa-cog",
        "core.Notification": "fas fa-bell",
        "core.EmailTemplate": "fas fa-envelope",
        "core.Document": "fas fa-file-alt",
        "core.ActivityLog": "fas fa-clipboard-list",
        "core.Backup": "fas fa-database",
        "core.PaymentMethod": "fas fa-university",
        "inventory.Category": "fas fa-tags",
        "inventory.Product": "fas fa-pills",
        "inventory.StockMovement": "fas fa-exchange-alt",
        "inventory.StockAlert": "fas fa-exclamation-triangle",
        "inventory.InventoryAdjustment": "fas fa-sliders-h",
        "sales.Customer": "fas fa-user-friends",
        "sales.Sale": "fas fa-shopping-cart",
        "sales.SaleItem": "fas fa-cart-plus",
        "sales.Payment": "fas fa-credit-card",
        "sales.CreditRecord": "fas fa-hand-holding-usd",
        "sales.LoyaltyCard": "fas fa-star",
        "sales.LoyaltyTransaction": "fas fa-history",
        "purchases.PurchaseOrder": "fas fa-truck",
        "purchases.PurchaseOrderItem": "fas fa-box",
    },
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.User": "vertical_tabs",
        "accounts.User": "vertical_tabs",
        "sales.Sale": "horizontal_tabs",
    },
    "language_chooser": False,
    "default_theme_mode": "dark",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
    "actions_sticky_top": False,
}
