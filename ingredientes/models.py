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
    
class Pregunta(models.Model):
    texto       = models.TextField()
    creado_por  = models.CharField(max_length=100, default="Anónimo")
    top_secret  = models.CharField(max_length=255, default="No deberías ver esto desde el API")
    estado = models.CharField(
        max_length=100,
        choices=(("respondida", "Respondida"), ("no respondida", "No Respondida")),
        default="No Respondida")
    categoria   = models.ForeignKey(
        Categoria, related_name="preguntas", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Pregunta: {self.name}"