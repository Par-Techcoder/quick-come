from django.urls import re_path
from .consumers import BookingConsumer, WorkerAssignmentConsumer,BookingListAllConsumer,PaymentConsumer,WorkerUpdateConsumer

websocket_urlpatterns = [
    re_path(r"ws/bookings/$", BookingListAllConsumer.as_asgi()),
    re_path(r"ws/booking_updates/$", BookingConsumer.as_asgi()),
    re_path(r"ws/worker-assignments/$", WorkerAssignmentConsumer.as_asgi()),
    re_path(r"ws/payments/$", PaymentConsumer.as_asgi()),# For payment updates
    re_path(r'ws/workers/$', WorkerUpdateConsumer.as_asgi()), 
]
