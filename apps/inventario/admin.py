from django.contrib import admin
from .models import TipoArmamento, Ubicacion, Responsable ,Armamento, Movimiento, Mantenimiento, Promocion, Alumno

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
        "codigo",
        "numero_serie",
        "tipo",
        "marca",
        "modelo",
        "calibre",
        "estado",
        "ubicacion",
        "duenio",
        "responsable",
        "activo",
    )

    list_filter = (
        "estado",
        "tipo",
        "ubicacion",
        "activo",
    )

    search_fields = (
        "codigo",
        "numero_serie",
        "marca",
        "modelo",
        "duenio__apellidos",
        "duenio__nombres",
        "duenio__promocion__nombre",
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
        "armamento__codigo",
        "armamento__numero_serie",
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
        "responsable_armerillo",
    )

    list_filter = (
        "estado",
        "fecha_ingreso",
    )

    search_fields = (
        "armamento__codigo",
        "armamento__numero_serie",
        "responsable_armerillo__apellidos",
        "responsable_armerillo__nombres",
    )

#Promocion y Alumno
@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa")
    search_fields = ("nombre",)


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = (
        "apellidos",
        "nombres",
        "promocion",
        "activo",
    )

    list_filter = (
        "promocion",
        "activo",
    )

    search_fields = (
        "apellidos",
        "nombres",
        "cedula",
    )