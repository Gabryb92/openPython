from django.db import models

# Create your models here.

class Target(models.Model):
    ip_address = models.GenericIPAddressField()
    name = models.CharField(max_length=100, blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address
