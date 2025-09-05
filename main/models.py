from django.db import models

class Shop(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=255)
    is_featured = models.BooleanField(default=False)

def __str__(self):
        return self.name
