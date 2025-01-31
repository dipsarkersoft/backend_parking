from django.db import models

# Create your models here.
class CategoryModel(models.Model):
    
    name=models.CharField(max_length=30)
    price_p_h=models.IntegerField()
    total_slots=models.IntegerField()
    available_slots=models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.total_slots} -{self.available_slots}"

