from .models import Movimiento


def registrar_movimiento(
    armamento,
    tipo,
    usuario,
    ubicacion_origen=None,
    ubicacion_destino=None,
    responsable_anterior=None,
    responsable_nuevo=None,
    estado_anterior=None,
    estado_nuevo=None,
    observacion=""
):

    Movimiento.objects.create(

        armamento=armamento,

        tipo=tipo,

        usuario=usuario,

        ubicacion_origen=ubicacion_origen,
        ubicacion_destino=ubicacion_destino,

        responsable_anterior=responsable_anterior,
        responsable_nuevo=responsable_nuevo,

        estado_anterior=estado_anterior,
        estado_nuevo=estado_nuevo,

        observacion=observacion,
    )