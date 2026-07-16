from django.urls import path
from . import views

urlpatterns = [

    path(
        "ubicaciones/",
        views.lista_ubicaciones,
        name="lista_ubicaciones",
    ),

    path(
        "ubicaciones/nueva/",
        views.crear_ubicacion,
        name="crear_ubicacion",
    ),

    path(
        "ubicaciones/<int:pk>/editar/",
        views.editar_ubicacion,
        name="editar_ubicacion",
    ),

    path(
        "ubicaciones/<int:pk>/eliminar/",
        views.eliminar_ubicacion,
        name="eliminar_ubicacion",
    ),

    path(
        "armamentos/",
        views.lista_armamentos,
        name="lista_armamentos",
    ),

    path(
        "armamentos/nuevo/",
        views.crear_armamento,
        name="crear_armamento",
    ),

    path(
        "armamentos/<int:pk>/editar/",
        views.editar_armamento,
        name="editar_armamento",
    ),

    path(
        "armamentos/<int:pk>/eliminar/",
        views.eliminar_armamento,
        name="eliminar_armamento",
    ),

    path(
        "tipos/",
        views.lista_tipos,
        name="lista_tipos"
    ),

    path(
        "tipos/nuevo/",
        views.crear_tipo,
        name="crear_tipo"
    ),

    path(
        "tipos/<int:pk>/editar/",
        views.editar_tipo,
        name="editar_tipo"
    ),

    path(
        "tipos/<int:pk>/eliminar/",
        views.eliminar_tipo,
        name="eliminar_tipo"
    ),

    path(
        "responsables/",
        views.lista_responsables,
        name="lista_responsables"
    ),

    path(
        "responsables/nuevo/",
        views.crear_responsable,
        name="crear_responsable"
    ),

    path(
        "responsables/<int:pk>/editar/",
        views.editar_responsable,
        name="editar_responsable"
    ),

    path(
        "responsables/<int:pk>/eliminar/",
        views.eliminar_responsable,
        name="eliminar_responsable"
    ),

    path(
        "movimientos/",
        views.lista_movimientos,
        name="lista_movimientos"
    ),

    path(
        "movimientos/nuevo/",
        views.crear_movimiento,
        name="crear_movimiento"
    ),

#PDF
    path(
        "reportes/armamentos/pdf/",
        views.reporte_armamentos_pdf,
        name="reporte_armamentos_pdf",
    ),

]