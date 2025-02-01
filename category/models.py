from django.db import models

# Create your models here.

class CategoryModel(models.Model):
    
    name=models.CharField(max_length=30)
    price_p_h=models.IntegerField()
    total_slots=models.IntegerField()
    available_slots=models.IntegerField()
    available_slots_list = models.JSONField(default=list)
    def save(self, *args, **kwargs):
        
        if not self.pk: 
            self.available_slots_list = {str(i): "f" for i in range(1, self.total_slots + 1)}
            self.available_slots = self.total_slots
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}"

