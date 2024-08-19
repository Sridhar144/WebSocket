from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import logviewer.routing
from django.core.asgi import get_asgi_application  # Make sure this import is included

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            logviewer.routing.websocket_urlpatterns
        )
    ),
})
