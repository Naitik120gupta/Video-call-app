from django.urls import re_path
from agora.consumers import ChatConsumer


websocket_urlpatterns = [
    re_path(r"ws/Chat" , ChatConsumer.as_asgi()) , 
]