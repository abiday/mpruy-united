from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    JERSEY = 'JRS'
    BOOTS = 'BOT'
    BALL = 'BAL'
    ACCESSORIES = 'ACC'
    EQUIPMENT = 'EQP'
    
    CATEGORY_CHOICES = [
        (JERSEY, 'Jersey'),
        (BOOTS, 'Football Boots'),
        (BALL, 'Football Ball'),
        (ACCESSORIES, 'Accessories'),
        (EQUIPMENT, 'Training Equipment'),
    ]

    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    second_image = models.URLField(blank=True, null=True, help_text="Optional second image for hover effect")
    category = models.CharField(
        max_length=3,
        choices=CATEGORY_CHOICES,
        default=JERSEY,
    )
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name
