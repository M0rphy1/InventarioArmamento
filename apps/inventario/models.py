from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class TipoArmamento(models.Model):

    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )

    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )

    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Tipo de Armamento"
        verbose_name_plural = "Tipos de Armamento"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
#Ubicacion
class Ubicacion(models.Model):

    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    edificio = models.CharField(
        max_length=100,
        blank=True
    )

    piso = models.CharField(
        max_length=50,
        blank=True
    )

    descripcion = models.TextField(
        blank=True
    )

    activo = models.BooleanField(
        default=True
    )

    es_taller = models.BooleanField(
        default=False,
        verbose_name="Es taller de mantenimiento"
    )

    class Meta:
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

#Promocion
class Promocion(models.Model):

    nombre = models.CharField(
        max_length=50,
        unique=True
    )

    descripcion = models.CharField(
        max_length=150,
        blank=True
    )

    activa = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = "Promoción"
        verbose_name_plural = "Promociones"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

#Alumno
class Alumno(models.Model):

    promocion = models.ForeignKey(
        Promocion,
        on_delete=models.PROTECT,
        related_name="alumnos"
    )

    cedula = models.CharField(
        max_length=10,
        unique=True
    )

    nombres = models.CharField(
        max_length=100
    )

    apellidos = models.CharField(
        max_length=100
    )

    especialidad = models.CharField(
        max_length=50,
        blank=True
    )

    grado = models.CharField(
        max_length=30,
        blank=True
    )

    novedades = models.TextField(
        blank=True
    )

    activo = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"
        ordering = ["apellidos", "nombres"]

    def __str__(self):
        return f"{self.apellidos} {self.nombres} ({self.promocion.nombre})"
    
#Responsable
class Responsable(models.Model):

    GRADOS = [
        ("SLDO", "Soldado"),
        ("CBOP", "Cabo Primero"),
        ("CBOS", "Cabo Segundo"),
        ("SGOS", "Sargento Segundo"),
        ("SGOP", "Sargento Primero"),
        ("SUBP", "Suboficial Primero"),
        ("SUBM", "Suboficial Mayor"),
        ("TNTE", "Teniente"),
        ("CAPT", "Capitán"),
        ("MAYO", "Mayor"),
        ("TCNL", "Teniente Coronel"),
        ("CRNL", "Coronel"),
    ]

    grado = models.CharField(
        max_length=5,
        choices=GRADOS
    )

    cedula = models.CharField(
        max_length=10,
        unique=True
    )

    nombres = models.CharField(
        max_length=100
    )

    apellidos = models.CharField(
        max_length=100
    )

    cargo = models.CharField(
        max_length=100
    )

    activo = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = "Responsable"
        verbose_name_plural = "Responsables"
        ordering = ["apellidos"]

    def __str__(self):
        return f"{self.get_grado_display()} {self.apellidos} {self.nombres}"

    def clean(self):

        if len(self.cedula) != 10:

            raise ValidationError({
                "cedula": "La cédula debe tener exactamente 10 dígitos."
            })

        if not self.cedula.isdigit():

            raise ValidationError({
                "cedula": "La cédula solo debe contener números."
            })
#Armamento
class Armamento(models.Model):

    ESTADOS = [
        ("OPERABLE", "Operable"),
        ("MANTENIMIENTO", "Mantenimiento"),
        ("NO_OPERABLE", "No Operable"),
    ]

    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código"
    )

    numero_serie = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Número de Serie"
    )

    tipo = models.ForeignKey(
        TipoArmamento,
        on_delete=models.PROTECT,
        related_name="armamentos"
    )

    marca = models.CharField(max_length=100)

    modelo = models.CharField(max_length=100)

    calibre = models.CharField(max_length=50)

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="OPERABLE"
    )

    ubicacion = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        related_name="armamentos"
    )

    duenio = models.ForeignKey(
        Alumno,
        on_delete=models.PROTECT,
        related_name="armamentos",
        verbose_name="Dueño del fusil",
        null=True,
        blank=True,
    )

    responsable = models.ForeignKey(
        Responsable,
        on_delete=models.PROTECT,
        related_name="armamentos"
    )

    observaciones = models.TextField(
        blank=True
    )

    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Armamento"
        verbose_name_plural = "Armamentos"
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.numero_serie}"

    @property
    def nombre_completo(self):
        return f"{self.tipo} {self.marca} {self.modelo}"

    @property
    def esta_disponible(self):
        return self.estado == "OPERABLE"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

#Movimiento
class Movimiento(models.Model):

    TIPOS = [
        ("INGRESO", "Ingreso"),
        ("CAMBIO_UBICACION", "Cambio de ubicación"),
        ("CAMBIO_RESPONSABLE", "Cambio de responsable del armerillo"),
        ("CAMBIO_DUENIO", "Cambio de dueño"),
        ("NO_OPERABLE", "Marcar como No Operable"),
        ("BAJA", "Dar de baja"),
    ]

    armamento = models.ForeignKey(
        Armamento,
        on_delete=models.PROTECT,
        related_name="movimientos"
    )

    tipo = models.CharField(
        max_length=25,
        choices=TIPOS
    )

    ubicacion_origen = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        related_name="movimientos_origen",
        null=True,
        blank=True
    )

    ubicacion_destino = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        related_name="movimientos_destino",
        null=True,
        blank=True
    )

    responsable_anterior = models.ForeignKey(
        Responsable,
        on_delete=models.PROTECT,
        related_name="movimientos_anterior",
        null=True,
        blank=True
    )

    responsable_nuevo = models.ForeignKey(
        Responsable,
        on_delete=models.PROTECT,
        related_name="movimientos_nuevo",
        null=True,
        blank=True
    )

    duenio_anterior = models.ForeignKey(
        Alumno,
        on_delete=models.PROTECT,
        related_name="movimientos_duenio_anterior",
        null=True,
        blank=True
    )

    duenio_nuevo = models.ForeignKey(
        Alumno,
        on_delete=models.PROTECT,
        related_name="movimientos_duenio_nuevo",
        null=True,
        blank=True
    )

    estado_anterior = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    estado_nuevo = models.CharField(
        max_length=20,
        choices=Armamento.ESTADOS,
        blank=True,
        null=True
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    observacion = models.TextField(
        blank=True,
        null=True
    )

    usuario = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Movimiento"
        verbose_name_plural = "Movimientos"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.armamento.codigo} - {self.get_tipo_display()}"
    
#Mantenimiento
class Mantenimiento(models.Model):

    ESTADOS = [
        ("PENDIENTE", "Pendiente"),
        ("EN_PROCESO", "En proceso"),
        ("FINALIZADO", "Finalizado"),
    ]

    armamento = models.ForeignKey(
        Armamento,
        on_delete=models.PROTECT,
        related_name="mantenimientos"
    )

    fecha_ingreso = models.DateField()

    fecha_salida = models.DateField(
        null=True,
        blank=True
    )

    descripcion = models.TextField()

    motivo = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="PENDIENTE"
    )

    responsable_armerillo = models.ForeignKey(
        Responsable,
        on_delete=models.PROTECT,
        related_name="mantenimientos_tecnico",
        verbose_name="Responsable del armerillo",
        null=True,
        blank=True,
    )

    ubicacion_destino = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        related_name="mantenimientos_destino",
        null=True,
        blank=True
    )

    responsable_destino = models.ForeignKey(
        Responsable,
        on_delete=models.PROTECT,
        related_name="mantenimientos_responsable",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"
        ordering = ["-fecha_ingreso"]

    def __str__(self):
        return f"{self.armamento.codigo} - {self.estado}"
