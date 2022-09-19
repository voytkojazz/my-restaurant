from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Ingridient(models.Model):
    KILOGRAM = 'KG'
    GRAM = 'G'
    MILIGRAM = 'MG'
    LITER = 'L'
    MILILITER = 'ML'
    PIECE = 'PC'
    TABLESPOON = 'TS'
    TEASPOON = 'TE'
    UNIT_CHOICES = [
        (KILOGRAM, 'kg'),
        (GRAM, 'g'),
        (LITER, 'l'),
        (MILILITER, 'ml'),
        (MILIGRAM, 'mg'),
        (PIECE, 'piece/s'),
        (TABLESPOON, 'table spoon'),
        (TEASPOON, 'tea spoon'),
    ]
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES)
    unit_price = models.FloatField()
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('ingridient-detail', kwargs={'pk': self.pk})    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    def __str__(self) -> str:
        return self.title

    def avalaible(self):
        return all(X.enough() for X in self.recipe_requirement_set.all())

class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingridient = models.ForeignKey(Ingridient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    def __str__(self) -> str:
        return f'{self.ingridient}_{self.quantity}'

    def enough(self):
        return self.quantity <= self.ingridient.quantity


class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    


