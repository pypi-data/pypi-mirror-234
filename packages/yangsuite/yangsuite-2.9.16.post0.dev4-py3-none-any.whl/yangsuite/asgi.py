# mysite/asgi.py
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from yangsuite.settings.base import prefs

django_asgi_application = get_asgi_application()

from .urls import websocket_urlpatterns     # noqa: E402

os.environ.setdefault("DJANGO_SETTINGS_MODULE", prefs.get('settings_module'))

application = ProtocolTypeRouter(
    {
        "http": django_asgi_application,
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
