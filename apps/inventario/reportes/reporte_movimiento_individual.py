from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from apps.inventario.models import Movimiento


def generar_reporte_movimiento_individual_pdf(
    request,
    movimiento,

    # =====================================================
    # FIRMA CENTRAL
    # =====================================================

    firma_grado="",
    firma_nombres="",
    firma_apellidos="",
    firma_cargo="",

    # =====================================================
    # FIRMA CUSTODIO ENTREGA
    # =====================================================

    entrega_grado="",
    entrega_nombres="",
    entrega_apellidos="",
    entrega_cargo="",

    # =====================================================
    # FIRMA CUSTODIO RECIBE
    # =====================================================

    recibe_grado="",
    recibe_nombres="",
    recibe_apellidos="",
    recibe_cargo="",

    # =====================================================
    # CONTROL DE FIRMAS
    # =====================================================

    tres_firmas=False,
):

    # =====================================================
    # RESPUESTA PDF
    # =====================================================

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'inline; filename="movimiento_{movimiento.id}.pdf"'
    )

    # =====================================================
    # DOCUMENTO
    # =====================================================

    documento = SimpleDocTemplate(

        response,

        pagesize=A4,

        rightMargin=1.5 * cm,

        leftMargin=1.5 * cm,

        topMargin=1.5 * cm,

        bottomMargin=1.5 * cm,

    )

    estilos = getSampleStyleSheet()

    elementos = []

    # =====================================================
    # TÍTULO
    # =====================================================

    elementos.append(
        Paragraph(
            "REPORTE INDIVIDUAL DE MOVIMIENTO",
            estilos["Title"]
        )
    )

    elementos.append(
        Spacer(
            1,
            0.5 * cm
        )
    )

    # =====================================================
    # INFORMACIÓN DEL MOVIMIENTO
    # =====================================================

    datos_movimiento = [

        [
            "Fecha",
            movimiento.fecha.strftime(
                "%d/%m/%Y %H:%M:%S"
            )
        ],

        [
            "Armamento",
            movimiento.armamento.codigo
        ],

        [
            "Número de serie",
            movimiento.armamento.numero_serie
        ],

        [
            "Tipo de movimiento",
            movimiento.get_tipo_display()
        ],

        [
            "Usuario que registra",
            str(movimiento.usuario)
        ],

    ]

    tabla_movimiento = Table(

        datos_movimiento,

        colWidths=[
            5 * cm,
            11 * cm
        ]

    )

    tabla_movimiento.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#212529")
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (0, -1),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

        ])
    )

    elementos.append(
        tabla_movimiento
    )

    elementos.append(
        Spacer(
            1,
            0.5 * cm
        )
    )

    # =====================================================
    # DETALLES DEL MOVIMIENTO
    # =====================================================

    datos_detalle = []


    # =====================================================
    # CAMBIO DE UBICACIÓN
    # =====================================================

    if movimiento.tipo == "CAMBIO_UBICACION":

        datos_detalle.extend([

            [
                "Ubicación anterior",
                (
                    str(movimiento.ubicacion_origen)
                    if movimiento.ubicacion_origen
                    else "No registrada"
                )
            ],

            [
                "Ubicación nueva",
                (
                    str(movimiento.ubicacion_destino)
                    if movimiento.ubicacion_destino
                    else "No registrada"
                )
            ],

        ])


    # =====================================================
    # CAMBIO DE RESPONSABLE
    # =====================================================

    elif movimiento.tipo == "CAMBIO_RESPONSABLE":

        datos_detalle.extend([

            [
                "Custodio anterior",
                (
                    str(movimiento.responsable_anterior)
                    if movimiento.responsable_anterior
                    else "No registrado"
                )
            ],

            [
                "Custodio nuevo",
                (
                    str(movimiento.responsable_nuevo)
                    if movimiento.responsable_nuevo
                    else "No registrado"
                )
            ],

        ])


    # =====================================================
    # CAMBIO DE DUEÑO
    # =====================================================

    elif movimiento.tipo == "CAMBIO_DUENIO":

        datos_detalle.extend([

            [
                "Dueño anterior",
                (
                    str(movimiento.duenio_anterior)
                    if movimiento.duenio_anterior
                    else "No registrado"
                )
            ],

            [
                "Dueño nuevo",
                (
                    str(movimiento.duenio_nuevo)
                    if movimiento.duenio_nuevo
                    else "No registrado"
                )
            ],

        ])


    # =====================================================
    # NO OPERABLE
    # =====================================================

    elif movimiento.tipo == "NO_OPERABLE":

        datos_detalle.extend([

            [
                "Estado anterior",
                movimiento.estado_anterior
                or "No registrado"
            ],

            [
                "Estado nuevo",
                movimiento.estado_nuevo
                or "No registrado"
            ],

        ])


    # =====================================================
    # ENTRADA / SALIDA QR
    # =====================================================

    elif movimiento.tipo in ["ENTRADA", "SALIDA"]:

        datos_detalle.extend([

            [
                "Ubicación",
                (
                    str(movimiento.ubicacion_destino)
                    if movimiento.ubicacion_destino
                    else "No registrada"
                )
            ],

            [
                "Responsable",
                (
                    str(movimiento.responsable_nuevo)
                    if movimiento.responsable_nuevo
                    else "No registrado"
                )
            ],

        ])


    # =====================================================
    # OBSERVACIÓN
    # =====================================================

    datos_detalle.append([

        "Observación",

        movimiento.observacion
        or "Sin observaciones"

    ])

    tabla_detalle = Table(

        datos_detalle,

        colWidths=[
            5 * cm,
            11 * cm
        ]

    )

    tabla_detalle.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#f2f2f2")
            ),

            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

        ])
    )

    elementos.append(
        tabla_detalle
    )

    elementos.append(
        Spacer(
            1,
            2 * cm
        )
    )

    # =====================================================
    # FIRMAS
    # =====================================================

    # -----------------------------------------------------
    # CUSTODIO - ENTREGA
    # -----------------------------------------------------

    if movimiento.responsable_anterior:

        custodio_entrega_nombre = (
            f"{movimiento.responsable_anterior.apellidos} "
            f"{movimiento.responsable_anterior.nombres}"
        ).upper()

        custodio_entrega_grado = (
            movimiento.responsable_anterior.get_grado_display()
        ).upper()

    else:

        custodio_entrega_nombre = "NO REGISTRADO"
        custodio_entrega_grado = ""


    # -----------------------------------------------------
    # CUSTODIO - RECIBE
    # -----------------------------------------------------

    if movimiento.responsable_nuevo:

        custodio_recibe_nombre = (
            f"{movimiento.responsable_nuevo.apellidos} "
            f"{movimiento.responsable_nuevo.nombres}"
        ).upper()

        custodio_recibe_grado = (
            movimiento.responsable_nuevo.get_grado_display()
        ).upper()

    else:

        custodio_recibe_nombre = "NO REGISTRADO"
        custodio_recibe_grado = ""


    # -----------------------------------------------------
    # FIRMA CENTRAL
    # -----------------------------------------------------

    firma_central_nombre = (
        f"{firma_apellidos} "
        f"{firma_nombres}"
    ).upper().strip()

    firma_central_grado = firma_grado.upper().strip()

    firma_central_cargo = firma_cargo.upper().strip()


    # =====================================================
    # TABLA DE FIRMAS
    # =====================================================

    firmas = [

        # LÍNEA PARA FIRMA
        [
            "________________________________",
            "________________________________",
            "________________________________"
        ],

        # NOMBRES
        [
            custodio_entrega_nombre,
            firma_central_nombre,
            custodio_recibe_nombre
        ],

        # GRADOS
        [
            custodio_entrega_grado,
            firma_central_grado,
            custodio_recibe_grado
        ],

        # CARGOS / IDENTIFICACIÓN DE LA FIRMA
        [
            "CUSTODIO - ENTREGA",
            firma_central_cargo,
            "CUSTODIO - RECIBE"
        ],

    ]


    tabla_firmas = Table(

        firmas,

        colWidths=[
            5.5 * cm,
            5.5 * cm,
            5.5 * cm
        ],

        rowHeights=[
            0.7 * cm,
            0.6 * cm,
            0.6 * cm,
            0.8 * cm
        ]

    )


    tabla_firmas.setStyle(

        TableStyle([

            # ---------------------------------------------
            # ALINEACIÓN
            # ---------------------------------------------

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            # ---------------------------------------------
            # NOMBRES
            # ---------------------------------------------

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, 0),
                8
            ),

            # ---------------------------------------------
            # GRADOS
            # ---------------------------------------------

            (
                "FONTNAME",
                (0, 1),
                (-1, 1),
                "Helvetica"
            ),

            (
                "FONTSIZE",
                (0, 1),
                (-1, 1),
                7
            ),

            # ---------------------------------------------
            # LÍNEA DE FIRMA
            # ---------------------------------------------

            (
                "FONTNAME",
                (0, 2),
                (-1, 2),
                "Helvetica"
            ),

            (
                "FONTSIZE",
                (0, 2),
                (-1, 2),
                8
            ),

            # ---------------------------------------------
            # TEXTO INFERIOR
            # ---------------------------------------------

            (
                "FONTNAME",
                (0, 3),
                (-1, 3),
                "Helvetica-Bold"
            ),

            (
                "FONTSIZE",
                (0, 3),
                (-1, 3),
                8
            ),

            # ---------------------------------------------
            # ESPACIADO
            # ---------------------------------------------

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                3
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                3
            ),

        ])

    )


    elementos.append(
        tabla_firmas
    )

    # =====================================================
    # GENERAR PDF
    # =====================================================

    documento.build(
        elementos
    )

    return response