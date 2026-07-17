from django.contrib import admin
from .models import TipoArmamento, Ubicacion, Responsable ,Armamento, Movimiento, Mantenimiento

# Register your models here.
@admin.register(TipoArmamento)
class TipoArmamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    ordering = ("nombre",)
#Ubicacion
@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ("id", "es_taller", "nombre")
    search_fields = ("nombre",)
    ordering = ("nombre",)
#Responsable
@admin.register(Responsable)
class ResponsableAdmin(admin.ModelAdmin):

    list_display = (
        "grado",
        "apellidos",
        "nombres",
        "cargo",
        "activo",
    )

    search_fields = (
        "cedula",
        "apellidos",
        "nombres",
    )

    list_filter = (
        "grado",
        "activo",
    )
#Armamento
@admin.register(Armamento)
class ArmamentoAdmin(admin.ModelAdmin):

    list_display = (
        "numero_inventario",
        "numero_serie",
        "codigo",
        "tipo",
        "marca",
        "estado",
        "ubicacion",
        "responsable",
    )

    list_filter = (
        "estado",
        "tipo",
        "ubicacion",
    )

    search_fields = (
        "numero_inventario",
        "numero_serie",
        "codigo",
        "marca",
    )

    ordering = ("codigo",)
#Movimiento
@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):

    list_display = (
        "armamento",
        "tipo",
        "usuario",
        "fecha",
    )

    list_filter = (
        "tipo",
        "fecha",
    )

    search_fields = (
        "armamento__serie",
    )

    readonly_fields = (
        "fecha",
    )
# Mantenimiento
@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):

    list_display = (
        "armamento",
        "fecha_ingreso",
        "fecha_salida",
        "estado",
        "tecnico",
    )

    list_filter = (
        "estado",
        "fecha_ingreso",
    )

    search_fields = (
        "armamento__codigo",
        "armamento__numero_serie",
        "tecnico",
    )