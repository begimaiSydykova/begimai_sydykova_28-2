from django.db import models

# Create your models here.

class Product(models.Model):
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField(default=0)

    def __str__(self):
        return self.title

class Reviews(models.Model):
    text = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.title} - {self.text}'
