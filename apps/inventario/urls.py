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
        "armamentos/<int:pk>/historial/",
        views.historial_armamento,
        name="historial_armamento",
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

    path(
        "responsables/pdf/",
        views.reporte_responsables_pdf,
        name="reporte_responsables_pdf",
    ),

    path(
            "ubicaciones/pdf/",
            views.reporte_ubicaciones_pdf,
            name="reporte_ubicaciones_pdf",
        ),

    path(
            "tipos/pdf/",
            views.reporte_tipos_pdf,
            name="reporte_tipos_pdf",
        ),

    path(
            "movimientos/pdf/",
            views.reporte_movimientos_pdf,
            name="reporte_movimientos_pdf",
        ),

    path(
            "mantenimientos/pdf/",
            views.reporte_mantenimientos_pdf,
            name="reporte_mantenimientos_pdf",
        ),

    path(
        "reportes/promociones/pdf/",
        views.reporte_promociones_pdf,
        name="reporte_promociones_pdf",
    ),

    path(
        "reportes/alumnos/pdf/",
        views.reporte_alumnos_pdf,
        name="reporte_alumnos_pdf",
    ),

#mantenimiento
    path(
        "mantenimientos/",
        views.lista_mantenimientos,
        name="lista_mantenimientos"
    ),

    path(
        "mantenimientos/nuevo/",
        views.crear_mantenimiento,
        name="crear_mantenimiento"
    ),

    path(
        "mantenimientos/<int:pk>/editar/",
        views.editar_mantenimiento,
        name="editar_mantenimiento"
    ),

    path(
        "mantenimientos/<int:pk>/eliminar/",
        views.eliminar_mantenimiento,
        name="eliminar_mantenimiento"
    ),

    path(
        "armamentos/<int:pk>/responsable/",
        views.obtener_responsable_armamento,
        name="obtener_responsable_armamento",
    ),

#Filtro Reportes
    path(
        "reportes/armamentos/",
        views.reporte_armamentos,
        name="reporte_armamentos",
    ),

    path(
        "reportes/alumnos/",
        views.reporte_alumnos,
        name="reporte_alumnos",
    ),

#Promocion
    path(
        "promociones/",
        views.lista_promociones,
        name="lista_promociones"
    ),

    path(
        "promociones/nuevo/",
        views.crear_promocion,
        name="crear_promocion"
    ),

    path(
        "promociones/<int:pk>/editar/",
        views.editar_promocion,
        name="editar_promocion"
    ),

    path(
        "promociones/<int:pk>/eliminar/",
        views.eliminar_promocion,
        name="eliminar_promocion"
    ),
#Alumno
    path(
        "alumnos/",
        views.lista_alumnos,
        name="lista_alumnos"
    ),

    path(
        "alumnos/nuevo/",
        views.crear_alumno,
        name="crear_alumno"
    ),

    path(
        "alumnos/<int:pk>/editar/",
        views.editar_alumno,
        name="editar_alumno"
    ),

    path(
        "alumnos/<int:pk>/eliminar/",
        views.eliminar_alumno,
        name="eliminar_alumno"
    ),

]