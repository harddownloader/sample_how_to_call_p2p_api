from rest_framework import generics
from rest_framework.response import Response

from caller.create_new_order import create_new_order
from .models import Order


class CreateOrder(generics.CreateAPIView):
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        print('create new order')
        return Response(create_new_order(), status=201)


class CallbackUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()

    def update(self, request, *args, **kwargs):
        print('update')
        return Response(status=204)
