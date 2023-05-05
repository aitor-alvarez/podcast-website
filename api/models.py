from django.db import models
import uuid


class ExternalDevice(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    ip = models.IPAddressField(unique=True, blank=False)
    key = models.CharField(max_length=155,unique=True, default=uuid.uuid4(), blank=False)
    active = models.BooleanField()

    def __str__(self):
        return self.name


class Token(models.Model):
    device = models.ForeignKey(ExternalDevice)
    token = models.CharField(max_length=255, blank=False)
    valid_until = models.DateTimeField(blank=False)

    def __str__(self):
        return self.device.name

