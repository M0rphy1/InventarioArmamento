from django.db import models

# Create your models here.
class BaseModel(models.Model):
    """
    Modelo base para todas las tablas del sistema.
    """

    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )

    class Meta:
        abstract = True