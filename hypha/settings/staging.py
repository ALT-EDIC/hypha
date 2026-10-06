from .base import *  # noqa

DEBUG = True

# Alternatively, you can set these in a local.py file on the server
try:
    from .local import *  # noqa
except ImportError:
    pass

# Security settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
ELEVATE_COOKIE_SECURE = True

# Mailgun configuration.
if env.str("MAILGUN_API_KEY", None):
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    ANYMAIL = {
        "MAILGUN_API_KEY": env.str("MAILGUN_API_KEY"),
        "MAILGUN_SENDER_DOMAIN": env.str("EMAIL_HOST", None),
        "MAILGUN_API_URL": env.str("MAILGUN_API_URL", "https://api.mailgun.net/v3"),
        "WEBHOOK_SECRET": env.str("ANYMAIL_WEBHOOK_SECRET", None),
    }

# Heroku configuration.
# Set ON_HEROKU to true in Config Vars or via cli 'heroku config:set ON_HEROKU=true'.
if env.bool("ON_HEROKU", False):
    ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    *INSTALLED_APPS,
    "debug_toolbar",
]
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    *MIDDLEWARE,
]
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#configuring-internal-ips
INTERNAL_IPS = ["127.0.0.1"]

# We disable all panels by default here since some of them (SQL, Template,
# Profiling) can be very CPU intensive for this site.  However disabled panels
# can be easily toggled on in the UI.
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": {
        "debug_toolbar.panels.history.HistoryPanel",
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.alerts.AlertsPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.community.CommunityPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    },
    "SHOW_COLLAPSED": True,
}

SENTRY_DENY_URLS += ["__reload__", "/favicon.ico", "/media/", "/static/", "__debug__"]
