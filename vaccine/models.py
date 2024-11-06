from django.db import models


class Vaccine(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    manufacturer = models.CharField(max_length=250)
    image = models.ImageField(upload_to="vaccine/images", null=True)
    available_doses = models.IntegerField(null=True, blank=True)
    admin_route = models.CharField(max_length=50, null=True, blank=True)
    side_effects = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} by {self.manufacturer}"
