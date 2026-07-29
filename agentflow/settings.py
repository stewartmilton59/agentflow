import os
from pathlib import Path
from dotenv import load_dotenv

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

def get_env_var(key, default=None, mandatory=False):
    value = os.environ.get(key)
    if value is not None:
        return value
    if mandatory:
        raise ImproperlyConfigured(f"Required environment variable '{key}' is not set.")
    return default

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&_4^2x8@qp*wq(&^8%ub&&=-!k^1(#mr0mqjmh+e9#x$4_vdbp'

DEBUG = True

# Custom error handlers
handler400 = 'core.views.bad_request'
handler403 = 'core.views.permission_denied'
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'

ALLOWED_HOSTS = ['agentflow.pythonanywhere.com']


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
    'dj_urls_panel',
    'dj_signals_panel',
    "dj_control_room_base",
    "dj_control_room",

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

# Email settings (for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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
