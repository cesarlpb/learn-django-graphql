from django.db import models
from django.contrib.postgres.fields import ArrayField

class Categoria(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField()
    tags = ArrayField(
        models.CharField(max_length=100),
        size=5,
        blank=True,
        null=True,
        default=list,
    )

    def __str__(self):
        return f"Categoría: {self.name}"

class Ingrediente(models.Model):
    name        = models.CharField(max_length=100)
    notas       = models.TextField()
    categoria   = models.ForeignKey(
        Categoria, related_name="ingredientes", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Ingrediente: {self.name}"