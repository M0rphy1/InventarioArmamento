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

def generar_reporte_armamentos_pdf(request, armamentos):


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
    estilo_tabla = estilos["BodyText"]
    estilo_tabla.fontSize = 8
    estilo_tabla.leading = 9



    # Título interno del documento

    titulo = Paragraph(

        "<b>Listado General de Armamentos</b>",

        estilos["Heading1"]

    )


    elementos.append(titulo)



    elementos.append(

        Paragraph(

            f"Total de armamentos encontrados: {armamentos.count()}",

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

        "Dueño",

        "Promoción",

        "Responsable",

        "Estado",

        "Ubicación",

    ]]



    for arma in armamentos:


        datos.append([

            Paragraph(arma.codigo, estilo_tabla),

            Paragraph(arma.numero_serie, estilo_tabla),

            Paragraph(arma.tipo.nombre, estilo_tabla),

            Paragraph(arma.marca, estilo_tabla),

            Paragraph(arma.modelo, estilo_tabla),

            Paragraph(arma.calibre, estilo_tabla),

            Paragraph(str(arma.duenio) if arma.duenio else "-", estilo_tabla),

            Paragraph(
                arma.duenio.promocion.nombre
                if arma.duenio and arma.duenio.promocion
                else "-",
                estilo_tabla
            ),

            Paragraph(
                f"{arma.responsable.grado} {arma.responsable.apellidos} {arma.responsable.nombres}",
                estilo_tabla
            ),

            Paragraph(arma.get_estado_display(), estilo_tabla),

            Paragraph(arma.ubicacion.nombre, estilo_tabla),

        ])

    #tabla = Table(datos)
    tabla = Table(
        datos,
        colWidths=[
            2.4 * cm,   # Código
            2.6 * cm,   # Serie
            1.3 * cm,   # Tipo
            1.5 * cm,   # Marca
            1.8 * cm,   # Modelo
            2.0 * cm,   # Calibre
            1.6 * cm,   # Dueño
            1.9 * cm,   # Promoción
            4.2 * cm,   # Responsable
            2.3 * cm,   # Estado
            4.0 * cm,   # Ubicación
        ]
    )

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