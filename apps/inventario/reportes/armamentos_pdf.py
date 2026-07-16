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

from apps.inventario.models import Armamento



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
        "Reporte General de Armamentos"
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

def generar_reporte_armamentos_pdf(request):


    response = HttpResponse(
        content_type="application/pdf"
    )


    response["Content-Disposition"] = (
        'attachment; filename="Reporte_Armamentos.pdf"'
    )



    doc = SimpleDocTemplate(

        response,

        pagesize=landscape(A4),

        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,

        # IMPORTANTE:
        # deja espacio para el encabezado
        topMargin=3 * cm,

        bottomMargin=2 * cm,

    )



    elementos = []


    estilos = getSampleStyleSheet()



    # Título interno del documento

    titulo = Paragraph(

        "<b>Listado General de Armamentos</b>",

        estilos["Heading1"]

    )


    elementos.append(titulo)



    elementos.append(

        Paragraph(

            f"Total de armamentos registrados: {Armamento.objects.count()}",

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

        "Código",

        "Serie",

        "Tipo",

        "Marca",

        "Modelo",

        "Calibre",

        "Estado",

        "Ubicación",

        "Responsable"

    ]]



    armamentos = Armamento.objects.select_related(

        "tipo",

        "ubicacion",

        "responsable"

    )



    for arma in armamentos:


        datos.append([


            arma.codigo,


            arma.numero_serie,


            arma.tipo.nombre,


            arma.marca,


            arma.modelo,


            arma.calibre,


            arma.get_estado_display(),


            arma.ubicacion.nombre,


            str(arma.responsable),


        ])




    tabla = Table(datos)



    tabla.setStyle(

        TableStyle([


            # Encabezado azul

            (
                "BACKGROUND",
                (0,0),
                (-1,0),
                colors.HexColor("#1F4E78")
            ),


            (
                "TEXTCOLOR",
                (0,0),
                (-1,0),
                colors.white
            ),


            (
                "FONTNAME",
                (0,0),
                (-1,0),
                "Helvetica-Bold"
            ),


            (
                "FONTSIZE",
                (0,0),
                (-1,0),
                10
            ),


            (
                "BOTTOMPADDING",
                (0,0),
                (-1,0),
                10
            ),



            # Bordes

            (
                "GRID",
                (0,0),
                (-1,-1),
                0.5,
                colors.grey
            ),



            # Fondo filas

            (
                "BACKGROUND",
                (0,1),
                (-1,-1),
                colors.beige
            ),



            (
                "ALIGN",
                (0,0),
                (-1,-1),
                "CENTER"
            ),



            (
                "VALIGN",
                (0,0),
                (-1,-1),
                "MIDDLE"
            ),



        ])

    )



    elementos.append(tabla)



    # IMPORTANTE:
    # activa encabezado y pie

    doc.build(

        elementos,

        onFirstPage=encabezado_pie,

        onLaterPages=encabezado_pie

    )



    return response