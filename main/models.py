from django.db import models

class Shop(models.Model):
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
    category = models.CharField(
        max_length=3,
        choices=CATEGORY_CHOICES,
        default=JERSEY,
    )
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name
