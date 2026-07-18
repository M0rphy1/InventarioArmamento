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

from apps.inventario.models import Responsable


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
        "Reporte General de Responsables"
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

def generar_reporte_responsables_pdf(request):

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        'attachment; filename="Reporte_Responsables.pdf"'
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

    titulo = Paragraph(

        "<b>Listado General de Responsables</b>",

        estilos["Heading1"]

    )

    elementos.append(titulo)

    elementos.append(

        Paragraph(

            f"Total de responsables registrados: {Responsable.objects.count()}",

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

        "Grado",

        "Cédula",

        "Nombres",

        "Apellidos",

        "Cargo",

        "Estado"

    ]]

    responsables = Responsable.objects.all()

    for responsable in responsables:

        datos.append([

            responsable.get_grado_display(),

            responsable.cedula,

            responsable.nombres,

            responsable.apellidos,

            responsable.cargo,

            "Activo" if responsable.activo else "Inactivo"

        ])

    tabla = Table(datos)

    tabla.setStyle(

        TableStyle([

            # Encabezado azul
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
                10
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, 0),
                10
            ),

            # Bordes

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            # Fondo de filas

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