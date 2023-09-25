from django.conf import settings

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Order(models.Model):
    date = models.DateTimeField(blank=False)
    orderId = models.CharField(max_length=255)
    card = models.CharField(null=False, max_length=16)
    payoutAmount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    callbackUrl = models.TextField()
    callbackMethod = models.CharField(max_length=8)
    callbackHeaders = models.TextField()
    callbackBody = models.TextField()

    status = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            # MaxValueValidator(5)
        ]
    )

    rowNum = models.PositiveIntegerField(
        default=None,
        blank=True,
        null=True
    )
    screenshot = models.CharField(
        max_length=255,
        blank=True,
        default='',
        # null=True # nullable value for CharField is not recommended in doc - https://stackoverflow.com/a/44272461
    )

    def __str(self):
        return self.orderId
