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

]