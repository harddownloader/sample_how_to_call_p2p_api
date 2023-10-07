import pprint
import json
import os
import base64
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from rest_framework import generics
from rest_framework.response import Response

from caller.create_new_order import create_new_order
from .models import Order


class CreateOrder(generics.CreateAPIView):
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        print('create new order')
        return Response(
            create_new_order(),
            status=201
        )


class CallbackUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()

    def update(self, request, *args, **kwargs):
        current_file_path = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(current_file_path))

        # Get the full path to the public_key.pem file from the root dir of the project
        private_key_path = os.path.join(project_root, 'private_key.pem')

        with open(private_key_path, 'rb') as key_file:
            private_key_pem = key_file.read()

        # Load the private key from .pem file
        private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())

        received_encrypted_data_base64 = request.data['data']
        received_encrypted_data = base64.b64decode(received_encrypted_data_base64)

        # Check signature
        try:
            decrypted_data = private_key.decrypt(
                received_encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            received_data = json.loads(decrypted_data.decode('utf-8'))
            print('received_data data:')
            pprint.pprint(received_data)
            # The signature is correct, we got and decrypted the data
        except InvalidSignature:
            # The signature isn't correct
            print('digital signature is not valid!!!')

        return Response(status=204)
