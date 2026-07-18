from django.http import HttpResponse

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import cm

from datetime import datetime

from apps.inventario.models import Movimiento


# ==============================
# ENCABEZADO Y PIE DE PÁGINA
# ==============================

def encabezado_pie(canvas, doc):

    canvas.saveState()

    canvas.setFont("Helvetica-Bold", 16)

    canvas.drawString(
        2 * cm,
        19.5 * cm,
        "SISTEMA DE INVENTARIO DE ARMAMENTO"
    )

    canvas.setFont("Helvetica", 10)

    canvas.drawString(
        2 * cm,
        18.8 * cm,
        "Reporte General de Movimientos"
    )

    canvas.drawRightString(
        27 * cm,
        18.8 * cm,
        datetime.now().strftime("%d/%m/%Y %H:%M")
    )

    canvas.line(
        2 * cm,
        18.5 * cm,
        27 * cm,
        18.5 * cm
    )

    canvas.drawRightString(
        27 * cm,
        1.2 * cm,
        f"Página {doc.page}"
    )

    canvas.restoreState()


# ==============================
# GENERAR PDF
# ==============================

def generar_reporte_movimientos_pdf(request):

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        'attachment; filename="Reporte_Movimientos.pdf"'
    )

    doc = SimpleDocTemplate(

        response,

        pagesize=landscape(A4),

        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,

        topMargin=3 * cm,

        bottomMargin=2 * cm,

    )

    elementos = []

    estilos = getSampleStyleSheet()
    estilo_tabla = estilos["BodyText"]
    estilo_tabla.fontSize = 8
    estilo_tabla.leading = 10

    titulo = Paragraph(

        "<b>Listado General de Movimientos</b>",

        estilos["Heading1"]

    )

    elementos.append(titulo)

    elementos.append(

        Paragraph(

            f"Total de movimientos registrados: {Movimiento.objects.count()}",

            estilos["Normal"]

        )

    )

    elementos.append(
        Spacer(1, 0.5 * cm)
    )

    # ==============================
    # TABLA
    # ==============================

    datos = [[

        "Fecha",

        "Armamento",

        "Tipo",

        "Ubicación Origen",

        "Ubicación Destino",

        "Resp. Anterior",

        "Resp. Nuevo",

        "Usuario"

    ]]

    movimientos = Movimiento.objects.select_related(

        "armamento",

        "ubicacion_origen",

        "ubicacion_destino",

        "responsable_anterior",

        "responsable_nuevo",

        "usuario"

    )

    for movimiento in movimientos:

        datos.append([

            Paragraph(movimiento.fecha.strftime("%d/%m/%Y %H:%M"), estilo_tabla),

            Paragraph(movimiento.armamento.codigo, estilo_tabla),

            Paragraph(movimiento.get_tipo_display(), estilo_tabla),

            Paragraph(
                movimiento.ubicacion_origen.nombre if movimiento.ubicacion_origen else "-",
                estilo_tabla
            ),

            Paragraph(
                movimiento.ubicacion_destino.nombre if movimiento.ubicacion_destino else "-",
                estilo_tabla
            ),

            Paragraph(
                str(movimiento.responsable_anterior) if movimiento.responsable_anterior else "-",
                estilo_tabla
            ),

            Paragraph(
                str(movimiento.responsable_nuevo) if movimiento.responsable_nuevo else "-",
                estilo_tabla
            ),

            Paragraph(
                str(movimiento.usuario),
                estilo_tabla
            )

        ])

    tabla = Table(datos)

    tabla.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1F4E78")
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

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
                9
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, 0),
                10
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.beige
            ),

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

        ])

    )

    elementos.append(tabla)

    doc.build(

        elementos,

        onFirstPage=encabezado_pie,

        onLaterPages=encabezado_pie

    )

    return response