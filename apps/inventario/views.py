from django.shortcuts import render, redirect, get_object_or_404
from .models import Ubicacion, Armamento, TipoArmamento, Responsable, Movimiento, Mantenimiento, Promocion, Alumno
from .forms import UbicacionForm, ArmamentoForm, TipoArmamentoForm, ResponsableForm, MovimientoForm, MantenimientoForm, FinalizarMantenimientoForm, ReporteArmamentoForm, PromocionForm, AlumnoForm, ReporteAlumnoForm, ImportarMatrizAlumnosForm
from django.contrib import messages

from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.db import transaction
from openpyxl import load_workbook
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import registrar_movimiento

def es_administrador(user):
    return user.groups.filter(name="Administrador").exists()

# Create your views here.
@login_required
@user_passes_test(es_administrador)
def lista_ubicaciones(request):

    buscar = request.GET.get("buscar", "")

    ubicaciones = Ubicacion.objects.all()

    if buscar:

        ubicaciones = ubicaciones.filter(
            Q(codigo__icontains=buscar) |
            Q(nombre__icontains=buscar)
        )

    paginator = Paginator(ubicaciones, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "inventario/ubicaciones/lista.html",
        {
            "page_obj": page_obj,
            "buscar": buscar,
        }
    )

@login_required
@user_passes_test(es_administrador)
def crear_ubicacion(request):

    if request.method == "POST":

        form = UbicacionForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "La ubicación fue registrada correctamente."
            )
            return redirect("lista_ubicaciones")

    else:

        form = UbicacionForm()

    return render(
        request,
        "inventario/ubicaciones/form.html",
        {
            "form": form,
            "titulo": "Nueva Ubicación"
        }
    )

@login_required
@user_passes_test(es_administrador)
def editar_ubicacion(request, pk):

    ubicacion = get_object_or_404(
        Ubicacion,
        pk=pk
    )

    if request.method == "POST":

        form = UbicacionForm(
            request.POST,
            instance=ubicacion
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "La ubicación fue actualizada correctamente."
            )

            return redirect("lista_ubicaciones")

    else:

        form = UbicacionForm(
            instance=ubicacion
        )

    return render(
        request,
        "inventario/ubicaciones/form.html",
        {
            "form": form,
            "titulo": "Editar Ubicación"
        }
    )

@login_required
@user_passes_test(es_administrador)
def eliminar_ubicacion(request, pk):

    ubicacion = get_object_or_404(
        Ubicacion,
        pk=pk
    )

    if request.method == "POST":

        ubicacion.activo = False
        ubicacion.save()

        messages.success(
            request,
            "La ubicación fue desactivada correctamente."
        )

        return redirect("lista_ubicaciones")

    return render(
        request,
        "inventario/ubicaciones/eliminar.html",
        {
            "ubicacion": ubicacion
        }
    )
#Armamento
# Armamento
@login_required
def lista_armamentos(request):

    buscar = request.GET.get("buscar", "")

    armamentos = Armamento.objects.filter(
        activo=True
    )

    if buscar:

        armamentos = armamentos.filter(
            Q(codigo__icontains=buscar) |
            Q(numero_serie__icontains=buscar) |
            Q(marca__icontains=buscar) |
            Q(modelo__icontains=buscar)
        )

    paginator = Paginator(
        armamentos,
        10
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        "inventario/armamentos/lista.html",
        {
            "page_obj": page_obj,
            "buscar": buscar,
        }
    )

@login_required
def historial_armamento(request, pk):

    armamento = get_object_or_404(
        Armamento,
        pk=pk
    )

    movimientos = (
        Movimiento.objects.select_related(
            "usuario",
            "ubicacion_origen",
            "ubicacion_destino",
            "responsable_anterior",
            "responsable_nuevo",
        )
        .filter(armamento=armamento)
        .order_by("-fecha")
    )

    return render(
        request,
        "inventario/armamentos/historial.html",
        {
            "armamento": armamento,
            "movimientos": movimientos,
        }
    )

@login_required
@user_passes_test(es_administrador)
@transaction.atomic
def crear_armamento(request):

    if request.method == "POST":

        form = ArmamentoForm(request.POST)

        if form.is_valid():

            print("Estado enviado por el formulario:", form.cleaned_data["estado"])

            duenio = form.cleaned_data.get("duenio")

            confirmado = request.POST.get("confirmado")
            print("Dueño seleccionado:", duenio)
            print("Confirmado:", confirmado)

            arma_existente = None

            if duenio:
                arma_existente = Armamento.objects.filter(
                    duenio=duenio
                ).first()

            print("Arma encontrada:", arma_existente)

            if duenio and not confirmado:

                arma_existente = Armamento.objects.filter(
                    duenio=duenio
                ).first()

                if arma_existente:

                    return render(
                        request,
                        "inventario/armamentos/form.html",
                        {
                            "form": form,
                            "titulo": "Nuevo Armamento",
                            "confirmar_duenio": True,
                            "arma_existente": arma_existente,
                        }
                    )

            armamento = form.save(commit=False)

            print("Estado antes de guardar:", armamento.estado)

            armamento.save()

            print("Estado después de guardar:", armamento.estado)

            registrar_movimiento(

                armamento=armamento,

                tipo="INGRESO",

                usuario=request.user,

                ubicacion_origen=None,
                ubicacion_destino=armamento.ubicacion,

                responsable_anterior=None,
                responsable_nuevo=armamento.responsable,

                estado_anterior=None,
                estado_nuevo=armamento.estado,

                observacion="Registro inicial del armamento."
            )

            messages.success(
                request,
                "Armamento registrado correctamente."
            )

            return redirect("lista_armamentos")

    else:

        form = ArmamentoForm()

    return render(
        request,
        "inventario/armamentos/form.html",
        {
            "form": form,
            "titulo": "Nuevo Armamento"
        }
    )

@login_required
@user_passes_test(es_administrador)
def editar_armamento(request, pk):

    armamento = get_object_or_404(Armamento, pk=pk)

    if request.method == "POST":

        form = ArmamentoForm(
            request.POST,
            instance=armamento
        )

        if form.is_valid():

            armamento_editado = form.save(commit=False)

            # Mantener los valores originales
            armamento_editado.estado = armamento.estado
            armamento_editado.ubicacion = armamento.ubicacion
            armamento_editado.responsable = armamento.responsable

            armamento_editado.save()

            messages.success(
                request,
                "Armamento actualizado correctamente."
            )

            return redirect("lista_armamentos")

    else:

        form = ArmamentoForm(instance=armamento)

    return render(
        request,
        "inventario/armamentos/form.html",
        {
            "form": form,
            "titulo": "Editar Armamento",
        }
    )

@login_required
@user_passes_test(es_administrador)
@transaction.atomic
def eliminar_armamento(request, pk):

    armamento = get_object_or_404(
        Armamento,
        pk=pk
    )

    if request.method == "POST":

        # Guardamos los datos actuales
        estado_anterior = armamento.estado
        ubicacion_anterior = armamento.ubicacion
        responsable_anterior = armamento.responsable
        duenio_anterior = armamento.duenio

        # Baja lógica
        armamento.activo = False

        armamento.save(
            update_fields=["activo"]
        )

        # Registrar la baja en movimientos
        registrar_movimiento(

            armamento=armamento,

            tipo="BAJA",

            usuario=request.user,

            ubicacion_origen=ubicacion_anterior,
            ubicacion_destino=ubicacion_anterior,

            responsable_anterior=responsable_anterior,
            responsable_nuevo=responsable_anterior,

            estado_anterior=estado_anterior,
            estado_nuevo=estado_anterior,

            observacion=(
                "Armamento dado de baja del inventario. "
            )
        )

        messages.success(
            request,
            "El armamento fue dado de baja correctamente."
        )

        return redirect("lista_armamentos")

    return render(
        request,
        "inventario/armamentos/eliminar.html",
        {
            "armamento": armamento
        }
    )

@login_required
@user_passes_test(es_administrador)
def lista_tipos(request):

    buscar = request.GET.get("buscar", "")

    tipos = TipoArmamento.objects.filter(
        Q(nombre__icontains=buscar) |
        Q(descripcion__icontains=buscar)
    )

    paginator = Paginator(tipos, 10)

    page = request.GET.get("page")

    page_obj = paginator.get_page(page)

    return render(request,
        "inventario/tipos/lista.html",
        {
            "page_obj": page_obj,
            "buscar": buscar,
        }
    )

@login_required
@user_passes_test(es_administrador)
def crear_tipo(request):

    if request.method == "POST":

        form = TipoArmamentoForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("lista_tipos")

    else:

        form = TipoArmamentoForm()

    return render(
        request,
        "inventario/tipos/form.html",
        {
            "form": form,
            "titulo": "Nuevo Tipo de Armamento"
        }
    )

@login_required
@user_passes_test(es_administrador)
def editar_tipo(request, pk):

    tipo = get_object_or_404(TipoArmamento, pk=pk)

    if request.method == "POST":

        form = TipoArmamentoForm(request.POST, instance=tipo)

        if form.is_valid():

            form.save()

            return redirect("lista_tipos")

    else:

        form = TipoArmamentoForm(instance=tipo)

    return render(
        request,
        "inventario/tipos/form.html",
        {
            "form": form,
            "titulo": "Editar Tipo de Armamento"
        }
    )

@login_required
@user_passes_test(es_administrador)
def eliminar_tipo(request, pk):

    tipo = get_object_or_404(TipoArmamento, pk=pk)

    if request.method == "POST":

        tipo.delete()

        return redirect("lista_tipos")

    return render(
        request,
        "inventario/tipos/confirmar_eliminar.html",
        {
            "objeto": tipo
        }
    )

@login_required
@user_passes_test(es_administrador)
def lista_responsables(request):

    buscar = request.GET.get("buscar", "")

    responsables = Responsable.objects.all()

    if buscar:
        responsables = responsables.filter(
            Q(cedula__icontains=buscar) |
            Q(nombres__icontains=buscar) |
            Q(apellidos__icontains=buscar)
        )

    paginator = Paginator(responsables, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "inventario/responsables/lista.html",
        {
            "page_obj": page_obj,
            "buscar": buscar,
        }
    )

@login_required
@user_passes_test(es_administrador)
def crear_responsable(request):

    if request.method == "POST":

        form = ResponsableForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("lista_responsables")

    else:

        form = ResponsableForm()

    return render(
        request,
        "inventario/responsables/form.html",
        {
            "form": form,
            "titulo": "Nuevo Responsable"
        }
    )

@login_required
@user_passes_test(es_administrador)
def editar_responsable(request, pk):

    responsable = get_object_or_404(Responsable, pk=pk)

    if request.method == "POST":

        form = ResponsableForm(request.POST, instance=responsable)

        if form.is_valid():

            form.save()

            return redirect("lista_responsables")

    else:

        form = ResponsableForm(instance=responsable)

    return render(
        request,
        "inventario/responsables/form.html",
        {
            "form": form,
            "titulo": "Editar Responsable"
        }
    )

@login_required
@user_passes_test(es_administrador)
def eliminar_responsable(request, pk):

    responsable = get_object_or_404(Responsable, pk=pk)

    if request.method == "POST":

        responsable.delete()

        return redirect("lista_responsables")

    return render(
        request,
        "inventario/responsables/eliminar.html",
        {
            "responsable": responsable
        }
    )

@login_required
def lista_movimientos(request):

    movimientos = Movimiento.objects.select_related(
        "armamento",
        "usuario"
    ).order_by("-fecha")

    return render(
        request,
        "inventario/movimientos/lista.html",
        {
            "movimientos": movimientos
        }
    )

@login_required
@transaction.atomic
def crear_movimiento(request):

    if request.method == "POST":

        form = MovimientoForm(request.POST)

        if form.is_valid():

            movimiento = form.save(commit=False)

            armamento = movimiento.armamento

            movimiento.usuario = request.user

            # Guardar datos anteriores
            movimiento.ubicacion_origen = armamento.ubicacion
            movimiento.responsable_anterior = armamento.responsable
            movimiento.duenio_anterior = armamento.duenio
            movimiento.estado_anterior = armamento.estado

            # ==========================
            # Cambio de ubicación
            # ==========================

            if movimiento.tipo == "CAMBIO_UBICACION":

                armamento.ubicacion = movimiento.ubicacion_destino

            # ==========================
            # Cambio de responsable
            # ==========================

            elif movimiento.tipo == "CAMBIO_RESPONSABLE":

                armamento.responsable = movimiento.responsable_nuevo

            # ==========================
            # Cambio de dueño
            # ==========================

            elif movimiento.tipo == "CAMBIO_DUENIO":

                armamento.duenio = movimiento.duenio_nuevo

            # ==========================
            # No operable
            # ==========================

            elif movimiento.tipo == "NO_OPERABLE":

                armamento.estado = "NO_OPERABLE"

            # Guardar datos nuevos en el movimiento
            movimiento.estado_nuevo = armamento.estado

            armamento.save()

            movimiento.save()

            return redirect("lista_movimientos")

    else:

        form = MovimientoForm()

    return render(
        request,
        "inventario/movimientos/form.html",
        {
            "form": form,
            "titulo": "Registrar Movimiento"
        }
    )

#Generar PDF
from datetime import datetime
from reportlab.lib.units import cm
from .reportes.armamentos_pdf import generar_reporte_armamentos_pdf
from .reportes.responsables_pdf import generar_reporte_responsables_pdf
from .reportes.ubicaciones_pdf import generar_reporte_ubicaciones_pdf
from .reportes.tipos_pdf import generar_reporte_tipos_pdf
from .reportes.movimientos_pdf import generar_reporte_movimientos_pdf
from .reportes.mantenimientos_pdf import generar_reporte_mantenimientos_pdf
from .reportes.promociones_pdf import generar_reporte_promociones_pdf
from .reportes.alumnos_pdf import generar_reporte_alumnos_pdf

#Reporte de armamentos
@login_required
def reporte_armamentos_pdf(request):

    armamentos = Armamento.objects.select_related(
        "tipo",
        "ubicacion",
        "responsable",
        "duenio",
        "duenio__promocion",
    )

    # ==========================
    # RESPONSABLE
    # ==========================

    responsables = request.GET.getlist("responsables")

    if responsables:

        armamentos = armamentos.filter(
            responsable_id__in=responsables
        )

    # ==========================
    # ARMAMENTOS
    # ==========================

    armamentos_ids = request.GET.getlist("armamentos")

    if armamentos_ids:

        armamentos = armamentos.filter(
            id__in=armamentos_ids
        )

    # ==========================
    # ESTADO
    # ==========================

    estado = request.GET.get("estado")

    if estado:

        armamentos = armamentos.filter(
            estado=estado
        )

    # ==========================
    # UBICACIÓN
    # ==========================

    ubicacion = request.GET.get("ubicacion")

    if ubicacion:

        armamentos = armamentos.filter(
            ubicacion_id=ubicacion
        )

    # ==========================
    # TIPO
    # ==========================

    tipo = request.GET.get("tipo")

    if tipo:

        armamentos = armamentos.filter(
            tipo_id=tipo
        )

    # ==========================
    # PROMOCIÓN
    # ==========================

    promocion = request.GET.get("promocion")

    if promocion:

        armamentos = armamentos.filter(
            duenio__promocion_id=promocion
        )

    return generar_reporte_armamentos_pdf(
        request,
        armamentos
    )

def reporte_responsables_pdf(request):
    return generar_reporte_responsables_pdf(request)

def reporte_ubicaciones_pdf(request):
    return generar_reporte_ubicaciones_pdf(request)

def reporte_tipos_pdf(request):
    return generar_reporte_tipos_pdf(request)

def reporte_movimientos_pdf(request):
    return generar_reporte_movimientos_pdf(request)

def reporte_mantenimientos_pdf(request):
    return generar_reporte_mantenimientos_pdf(request)

def reporte_promociones_pdf(request):
    return generar_reporte_promociones_pdf(request)

@login_required
def reporte_alumnos_pdf(request):

    alumnos = Alumno.objects.select_related(
        "promocion"
    )

    promocion = request.GET.get("promocion")

    if promocion:

        alumnos = alumnos.filter(
            promocion_id=promocion
        )

    return generar_reporte_alumnos_pdf(
        request,
        alumnos
    )

#Mantenimiento
@login_required
def lista_mantenimientos(request):

    mantenimientos = Mantenimiento.objects.select_related(
        "armamento"
    ).order_by("-fecha_ingreso")

    return render(
        request,
        "inventario/mantenimientos/lista.html",
        {
            "mantenimientos": mantenimientos
        }
    )

@login_required
@transaction.atomic
def crear_mantenimiento(request):

    if request.method == "POST":

        form = MantenimientoForm(request.POST)

        if form.is_valid():

            mantenimiento = form.save(commit=False)

            # Todo mantenimiento nuevo inicia en proceso
            mantenimiento.estado = "EN_PROCESO"

            # Guardar el responsable actual del armamento
            mantenimiento.responsable_armerillo = (
            mantenimiento.armamento.responsable
)

            armamento = mantenimiento.armamento

            # Guardamos los datos anteriores
            estado_anterior = armamento.estado
            ubicacion_anterior = armamento.ubicacion
            responsable_anterior = armamento.responsable

            # Enviar automáticamente al taller
            taller = Ubicacion.objects.get(es_taller=True)

            armamento.estado = "MANTENIMIENTO"
            armamento.ubicacion = taller

            armamento.save()
            mantenimiento.save()

            # Registrar movimiento
            registrar_movimiento(

                armamento=armamento,

                tipo="MANTENIMIENTO",

                usuario=request.user,

                ubicacion_origen=ubicacion_anterior,
                ubicacion_destino=taller,

                responsable_anterior=responsable_anterior,
                responsable_nuevo=responsable_anterior,

                estado_anterior=estado_anterior,
                estado_nuevo="MANTENIMIENTO",

                observacion="Armamento enviado al taller de mantenimiento."
            )

            return redirect("lista_mantenimientos")

    else:

        form = MantenimientoForm()

    return render(
        request,
        "inventario/mantenimientos/form.html",
        {
            "form": form,
            "titulo": "Registrar Mantenimiento"
        }
    )

@login_required
@transaction.atomic
def editar_mantenimiento(request, pk):

    mantenimiento = get_object_or_404(
        Mantenimiento,
        pk=pk
    )

    if mantenimiento.estado == "FINALIZADO":

        messages.warning(
            request,
            "Este mantenimiento ya fue finalizado y no puede modificarse."
        )

        return redirect("lista_mantenimientos")

    if request.method == "POST":

        form = FinalizarMantenimientoForm(
            request.POST,
            instance=mantenimiento
        )

        if form.is_valid():

            mantenimiento = form.save(commit=False)

            armamento = mantenimiento.armamento

            # Datos anteriores
            estado_anterior = armamento.estado
            ubicacion_anterior = armamento.ubicacion
            responsable_anterior = armamento.responsable

            # Si finaliza y no tiene fecha de salida
            if (
                mantenimiento.estado == "FINALIZADO"
                and not mantenimiento.fecha_salida
            ):
                from django.utils import timezone
                mantenimiento.fecha_salida = timezone.now().date()

            # Cambios al armamento
            if mantenimiento.estado == "FINALIZADO":

                armamento.estado = "OPERABLE"

                if mantenimiento.ubicacion_destino:
                    armamento.ubicacion = mantenimiento.ubicacion_destino

                if mantenimiento.responsable_destino:
                    armamento.responsable = mantenimiento.responsable_destino

            elif mantenimiento.estado == "EN_PROCESO":

                taller = Ubicacion.objects.get(es_taller=True)

                armamento.estado = "MANTENIMIENTO"
                armamento.ubicacion = taller

            armamento.save()
            mantenimiento.save()

            # Registrar movimiento
            registrar_movimiento(

                armamento=armamento,

                tipo="MANTENIMIENTO",

                usuario=request.user,

                ubicacion_origen=ubicacion_anterior,
                ubicacion_destino=armamento.ubicacion,

                responsable_anterior=responsable_anterior,
                responsable_nuevo=armamento.responsable,

                estado_anterior=estado_anterior,
                estado_nuevo=armamento.estado,

                observacion=(
                    "Mantenimiento finalizado."
                    if mantenimiento.estado == "FINALIZADO"
                    else "Mantenimiento actualizado."
                )
            )

            return redirect("lista_mantenimientos")

    else:

        form = FinalizarMantenimientoForm(
            instance=mantenimiento
        )

    return render(
        request,
        "inventario/mantenimientos/form.html",
        {
            "form": form,
            "titulo": "Editar Mantenimiento"
        }
    )

@login_required
def eliminar_mantenimiento(request, pk):

    mantenimiento = get_object_or_404(
        Mantenimiento,
        pk=pk
    )

    if mantenimiento.estado == "FINALIZADO":

        messages.warning(
            request,
            "No se puede eliminar un mantenimiento finalizado porque forma parte del historial."
        )

        return redirect("lista_mantenimientos")

    if request.method == "POST":

        mantenimiento.delete()

        return redirect("lista_mantenimientos")

    return render(
        request,
        "inventario/mantenimientos/eliminar.html",
        {
            "mantenimiento": mantenimiento
        }
    )

from django.http import JsonResponse
@login_required
def obtener_responsable_armamento(request, pk):

    armamento = get_object_or_404(
        Armamento.objects.select_related(
            "duenio",
            "duenio__promocion",
            "ubicacion",
            "responsable",
        ),
        pk=pk,
    )

    return JsonResponse({

        "responsable_id": armamento.responsable.id,

        "codigo": armamento.codigo,

        "estado": armamento.get_estado_display(),

        "ubicacion": armamento.ubicacion.nombre,

        "duenio": (
            str(armamento.duenio)
            if armamento.duenio else
            "Sin asignar"
        ),

        "promocion": (
            armamento.duenio.promocion.nombre
            if armamento.duenio else
            "-"
        ),

    })

#Filtro de reportes
@login_required
def reporte_armamentos(request):

    form = ReporteArmamentoForm()

    return render(
        request,
        "inventario/reportes/armamentos_filtro.html",
        {
            "form": form
        }
    )

@login_required
def reporte_alumnos(request):

    form = ReporteAlumnoForm()

    return render(
        request,
        "inventario/reportes/alumnos_filtro.html",
        {
            "form": form
        }
    )

#Promocion
@login_required
def lista_promociones(request):

    buscar = request.GET.get("buscar", "")

    promociones = Promocion.objects.all()

    if buscar:

        promociones = promociones.filter(
            Q(nombre__icontains=buscar) |
            Q(descripcion__icontains=buscar)
        )

    paginator = Paginator(promociones, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "inventario/promociones/lista.html",
        {
            "page_obj": page_obj,
            "buscar": buscar,
        }
    )


@login_required
@user_passes_test(es_administrador)
def crear_promocion(request):

    if request.method == "POST":

        form = PromocionForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Promoción registrada correctamente."
            )

            return redirect("lista_promociones")

    else:

        form = PromocionForm()

    return render(
        request,
        "inventario/promociones/form.html",
        {
            "form": form,
            "titulo": "Nueva Promoción"
        }
    )


@login_required
@user_passes_test(es_administrador)
def editar_promocion(request, pk):

    promocion = get_object_or_404(
        Promocion,
        pk=pk
    )

    if request.method == "POST":

        form = PromocionForm(
            request.POST,
            instance=promocion
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Promoción actualizada correctamente."
            )

            return redirect("lista_promociones")

    else:

        form = PromocionForm(instance=promocion)

    return render(
        request,
        "inventario/promociones/form.html",
        {
            "form": form,
            "titulo": "Editar Promoción"
        }
    )


@login_required
@user_passes_test(es_administrador)
def eliminar_promocion(request, pk):

    promocion = get_object_or_404(
        Promocion,
        pk=pk
    )

    if promocion.alumnos.exists():

        messages.error(
            request,
            "No puede eliminar una promoción que tiene alumnos registrados."
        )

        return redirect("lista_promociones")

    if request.method == "POST":

        promocion.delete()

        messages.success(
            request,
            "Promoción eliminada correctamente."
        )

        return redirect("lista_promociones")

    return render(
        request,
        "inventario/promociones/eliminar.html",
        {
            "objeto": promocion,
            "titulo": "Eliminar Promoción"
        }
    )

#Alumno
@login_required
def lista_alumnos(request):

    buscar = request.GET.get("buscar", "")
    promocion_id = request.GET.get("promocion", "")

    alumnos = Alumno.objects.select_related(
        "promocion"
    )

    # Filtro de búsqueda
    if buscar:

        alumnos = alumnos.filter(
            Q(cedula__icontains=buscar) |
            Q(nombres__icontains=buscar) |
            Q(apellidos__icontains=buscar) |
            Q(promocion__nombre__icontains=buscar)
        )

    # Filtro por promoción
    if promocion_id:

        alumnos = alumnos.filter(
            promocion_id=promocion_id
        )

    # Promociones disponibles para el selector
    promociones = Promocion.objects.filter(
        activa=True
    )

    # Paginación
    paginator = Paginator(alumnos, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "inventario/alumnos/lista.html",
        {
            "page_obj": page_obj,
            "buscar": buscar,
            "promociones": promociones,
            "promocion_seleccionada": promocion_id,
        }
    )

@login_required
@user_passes_test(es_administrador)
def crear_alumno(request):

    if request.method == "POST":

        form = AlumnoForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Alumno registrado correctamente."
            )

            return redirect("lista_alumnos")

    else:

        form = AlumnoForm()

    return render(
        request,
        "inventario/alumnos/form.html",
        {
            "form": form,
            "titulo": "Nuevo Alumno"
        }
    )

@login_required
@user_passes_test(es_administrador)
def editar_alumno(request, pk):

    alumno = get_object_or_404(
        Alumno,
        pk=pk
    )

    if request.method == "POST":

        form = AlumnoForm(
            request.POST,
            instance=alumno
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Alumno actualizado correctamente."
            )

            return redirect("lista_alumnos")

    else:

        form = AlumnoForm(instance=alumno)

    return render(
        request,
        "inventario/alumnos/form.html",
        {
            "form": form,
            "titulo": "Editar Alumno"
        }
    )

@login_required
@user_passes_test(es_administrador)
def eliminar_alumno(request, pk):

    alumno = get_object_or_404(
        Alumno,
        pk=pk
    )

    if alumno.armamentos.exists():

        messages.error(
            request,
            "No puede eliminar un alumno que tiene armamentos asignados."
        )

        return redirect("lista_alumnos")

    if request.method == "POST":

        alumno.delete()

        messages.success(
            request,
            "Alumno eliminado correctamente."
        )

        return redirect("lista_alumnos")

    return render(
        request,
        "inventario/alumnos/eliminar.html",
        {
            "objeto": alumno,
            "titulo": "Eliminar Alumno"
        }
    )

#Import excel
def separar_apellido_nombre(texto):

    texto = " ".join(str(texto).strip().split())

    partes = texto.split()

    if len(partes) < 2:
        raise ValueError(
            "El campo APELLIDO NOMBRE debe contener al menos "
            "un apellido y un nombre."
        )

    if len(partes) == 2:

        apellidos = partes[0]
        nombres = partes[1]

    elif len(partes) == 3:

        apellidos = " ".join(partes[:2])
        nombres = partes[2]

    else:

        apellidos = " ".join(partes[:2])
        nombres = " ".join(partes[2:])

    return apellidos, nombres
@login_required
@user_passes_test(es_administrador)
def importar_matriz_alumnos(request):

    # ==========================================================
    # CONFIRMAR IMPORTACIÓN
    # ==========================================================

    if request.method == "POST" and request.POST.get(
        "confirmar_importacion"
    ) == "1":

        registros = request.session.get(
            "matriz_alumnos_registros"
        )

        promocion_id = request.session.get(
            "matriz_alumnos_promocion"
        )

        if not registros or not promocion_id:

            messages.error(
                request,
                "No existe una matriz pendiente de importación."
            )

            return redirect("importar_matriz_alumnos")

        try:

            promocion = Promocion.objects.get(
                id=promocion_id,
                activa=True
            )

        except Promocion.DoesNotExist:

            messages.error(
                request,
                "La promoción seleccionada ya no existe o está inactiva."
            )

            return redirect("importar_matriz_alumnos")

        try:

            with transaction.atomic():

                alumnos_creados = 0
                armamentos_creados = 0

                for registro in registros:

                    fila = registro["fila"]

                    # ==================================================
                    # DATOS DEL ALUMNO
                    # ==================================================

                    cedula = registro["cedula"]

                    if not cedula:

                        raise ValueError(
                            f"Fila {fila}: la cédula está vacía."
                        )

                    if len(cedula) != 10 or not cedula.isdigit():

                        raise ValueError(
                            f"Fila {fila}: la cédula "
                            f"'{cedula}' no es válida."
                        )

                    # Verificar cédula duplicada

                    if Alumno.objects.filter(
                        cedula=cedula
                    ).exists():

                        raise ValueError(
                            f"Fila {fila}: la cédula "
                            f"'{cedula}' ya existe."
                        )

                    # ==================================================
                    # SEPARAR APELLIDO Y NOMBRE
                    # ==================================================

                    apellido_nombre = registro[
                        "apellido_nombre"
                    ]

                    try:

                        apellidos, nombres = (
                            separar_apellido_nombre(
                                apellido_nombre
                            )
                        )

                    except ValueError as e:

                        raise ValueError(
                            f"Fila {fila}: {e}"
                        )

                    # ==================================================
                    # CREAR ALUMNO
                    # ==================================================

                    alumno = Alumno.objects.create(

                        promocion=promocion,

                        cedula=cedula,

                        nombres=nombres,

                        apellidos=apellidos,

                        especialidad=registro[
                            "especialidad"
                        ],

                        grado=registro[
                            "grado"
                        ],

                        novedades=registro[
                            "novedades"
                        ],

                        activo=True
                    )

                    alumnos_creados += 1

                    # ==================================================
                    # TIPO DE ARMAMENTO
                    # ==================================================

                    nombre_tipo = registro["tipo"]

                    if not nombre_tipo:

                        raise ValueError(
                            f"Fila {fila}: el tipo de armamento "
                            f"está vacío."
                        )

                    tipo = TipoArmamento.objects.filter(
                        nombre__iexact=nombre_tipo,
                        activo=True
                    ).first()

                    if not tipo:

                        raise ValueError(
                            f"Fila {fila}: no existe el tipo "
                            f"de armamento '{nombre_tipo}'."
                        )

                    # ==================================================
                    # UBICACIÓN
                    # ==================================================

                    nombre_ubicacion = registro[
                        "ubicacion"
                    ]

                    if not nombre_ubicacion:

                        raise ValueError(
                            f"Fila {fila}: la ubicación está vacía."
                        )

                    ubicacion = Ubicacion.objects.filter(
                        nombre__iexact=nombre_ubicacion,
                        activo=True
                    ).first()

                    if not ubicacion:

                        raise ValueError(
                            f"Fila {fila}: no existe la ubicación "
                            f"'{nombre_ubicacion}'."
                        )

                    # ==================================================
                    # RESPONSABLE
                    # ==================================================

                    responsable_texto = registro[
                        "responsable"
                    ]

                    if not responsable_texto:

                        raise ValueError(
                            f"Fila {fila}: el responsable "
                            f"está vacío."
                        )

                    responsable = None

                    responsables = Responsable.objects.filter(
                        activo=True
                    )

                    texto_excel = (
                        responsable_texto
                        .strip()
                        .lower()
                    )

                    for r in responsables:

                        # Formato: APELLIDOS NOMBRES
                        nombre_apellidos = (
                            f"{r.apellidos} {r.nombres}"
                            .strip()
                            .lower()
                        )

                        # Formato: NOMBRES APELLIDOS
                        nombre_nombres = (
                            f"{r.nombres} {r.apellidos}"
                            .strip()
                            .lower()
                        )

                        if texto_excel in [
                            nombre_apellidos,
                            nombre_nombres,
                        ]:

                            responsable = r
                            break

                    if not responsable:

                        raise ValueError(
                            f"Fila {fila}: no se encontró "
                            f"el responsable "
                            f"'{responsable_texto}'."
                        )

                    # ==================================================
                    # DATOS DEL ARMAMENTO
                    # ==================================================

                    codigo = registro["codigo"]

                    numero_serie = registro[
                        "numero_serie"
                    ]

                    if not codigo:

                        raise ValueError(
                            f"Fila {fila}: el código del "
                            f"armamento está vacío."
                        )

                    if not numero_serie:

                        raise ValueError(
                            f"Fila {fila}: el número de serie "
                            f"está vacío."
                        )

                    # Verificar código

                    if Armamento.objects.filter(
                        codigo=codigo
                    ).exists():

                        raise ValueError(
                            f"Fila {fila}: el código "
                            f"'{codigo}' ya existe."
                        )

                    # Verificar número de serie

                    if Armamento.objects.filter(
                        numero_serie=numero_serie
                    ).exists():

                        raise ValueError(
                            f"Fila {fila}: el número de serie "
                            f"'{numero_serie}' ya existe."
                        )

                    # ==================================================
                    # ESTADO
                    # ==================================================

                    estado = registro[
                        "estado"
                    ].upper().strip()

                    estados_validos = [
                        "OPERABLE",
                        "MANTENIMIENTO",
                        "NO_OPERABLE",
                    ]

                    if estado not in estados_validos:

                        raise ValueError(
                            f"Fila {fila}: el estado "
                            f"'{estado}' no es válido. "
                            f"Valores permitidos: "
                            f"{', '.join(estados_validos)}."
                        )

                    # ==================================================
                    # CREAR ARMAMENTO
                    # ==================================================

                    Armamento.objects.create(

                        codigo=codigo,

                        numero_serie=numero_serie,

                        tipo=tipo,

                        marca=registro[
                            "marca"
                        ],

                        modelo=registro[
                            "modelo"
                        ],

                        calibre=registro[
                            "calibre"
                        ],

                        estado=estado,

                        ubicacion=ubicacion,

                        duenio=alumno,

                        responsable=responsable,

                        observaciones=registro[
                            "observaciones"
                        ],

                        activo=True
                    )

                    armamentos_creados += 1

            # ======================================================
            # LIMPIAR SESIÓN
            # ======================================================

            request.session.pop(
                "matriz_alumnos_registros",
                None
            )

            request.session.pop(
                "matriz_alumnos_promocion",
                None
            )

            messages.success(
                request,
                f"Importación completada correctamente. "
                f"Alumnos creados: {alumnos_creados}. "
                f"Armamentos creados: {armamentos_creados}."
            )

            return redirect(
                "lista_alumnos"
            )

        except Exception as e:

            messages.error(
                request,
                f"No se realizó la importación. {e}"
            )

            return redirect(
                "importar_matriz_alumnos"
            )

    # ==========================================================
    # VISTA PREVIA
    # ==========================================================

    if request.method == "POST":

        form = ImportarMatrizAlumnosForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            promocion = form.cleaned_data[
                "promocion"
            ]

            archivo = form.cleaned_data[
                "archivo"
            ]

            try:

                workbook = load_workbook(
                    archivo,
                    read_only=True,
                    data_only=True
                )

                hoja = workbook.active

                filas = list(
                    hoja.iter_rows(
                        values_only=True
                    )
                )

                workbook.close()

                if not filas:

                    messages.error(
                        request,
                        "El archivo Excel está vacío."
                    )

                    return render(
                        request,
                        "inventario/alumnos/importar_matriz.html",
                        {
                            "form": form
                        }
                    )

                # ==================================================
                # ENCABEZADOS
                # ==================================================

                encabezados = [
                    str(valor).strip()
                    if valor is not None
                    else ""
                    for valor in filas[0]
                ]

                encabezados_esperados = [
                    "ORD",
                    "ESPECIALIDAD",
                    "GRADO",
                    "APELLIDO NOMBRE",
                    "CEDULA",
                    "N° FUSIL",
                    "NOVEDADES",
                    "NÚMERO DE SERIE",
                    "TIPO",
                    "MARCA",
                    "MODELO",
                    "CALIBRE",
                    "ESTADO",
                    "UBICACIÓN",
                    "RESPONSABLE",
                    "OBSERVACIONES",
                ]

                if encabezados != encabezados_esperados:

                    messages.error(
                        request,
                        "Los encabezados del Excel "
                        "no coinciden con la plantilla."
                    )

                    return render(
                        request,
                        "inventario/alumnos/importar_matriz.html",
                        {
                            "form": form,
                            "encabezados_actuales": encabezados,
                            "encabezados_esperados":
                                encabezados_esperados,
                        }
                    )

                # ==================================================
                # LEER REGISTROS
                # ==================================================

                registros = []

                for numero_fila, fila in enumerate(
                    filas[1:],
                    start=2
                ):

                    if not any(
                        valor is not None
                        and str(valor).strip() != ""
                        for valor in fila
                    ):
                        continue

                    datos = dict(
                        zip(encabezados, fila)
                    )

                    registro = {

                        "fila": numero_fila,

                        "ord": str(
                            datos.get("ORD", "")
                        ).strip(),

                        "especialidad": str(
                            datos.get("ESPECIALIDAD", "")
                        ).strip(),

                        "grado": str(
                            datos.get("GRADO", "")
                        ).strip(),

                        "apellido_nombre": str(
                            datos.get("APELLIDO NOMBRE", "")
                        ).strip(),

                        "cedula": str(
                            datos.get("CEDULA", "")
                        ).strip(),

                        "codigo": str(
                            datos.get("N° FUSIL", "")
                        ).strip(),

                        "novedades": str(
                            datos.get("NOVEDADES", "")
                        ).strip(),

                        "numero_serie": str(
                            datos.get("NÚMERO DE SERIE", "")
                        ).strip(),

                        "tipo": str(
                            datos.get("TIPO", "")
                        ).strip(),

                        "marca": str(
                            datos.get("MARCA", "")
                        ).strip(),

                        "modelo": str(
                            datos.get("MODELO", "")
                        ).strip(),

                        "calibre": str(
                            datos.get("CALIBRE", "")
                        ).strip(),

                        "estado": str(
                            datos.get("ESTADO", "")
                        ).strip().upper(),

                        "ubicacion": str(
                            datos.get("UBICACIÓN", "")
                        ).strip(),

                        "responsable": str(
                            datos.get("RESPONSABLE", "")
                        ).strip(),

                        "observaciones": str(
                            datos.get("OBSERVACIONES", "")
                        ).strip(),
                    }

                    registros.append(
                        registro
                    )

                # ==================================================
                # GUARDAR VISTA PREVIA EN SESIÓN
                # ==================================================

                request.session[
                    "matriz_alumnos_registros"
                ] = registros

                request.session[
                    "matriz_alumnos_promocion"
                ] = promocion.id

                return render(
                    request,
                    "inventario/alumnos/importar_matriz.html",
                    {
                        "form": form,
                        "promocion": promocion,
                        "archivo": archivo,
                        "archivo_recibido": True,
                        "registros": registros,
                        "total_registros": len(
                            registros
                        ),
                    }
                )

            except Exception as e:

                messages.error(
                    request,
                    f"Error al leer el archivo Excel: {e}"
                )

    else:

        form = ImportarMatrizAlumnosForm()

    return render(
        request,
        "inventario/alumnos/importar_matriz.html",
        {
            "form": form
        }
    )
#MAtriz excel
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter
from django.http import HttpResponse

def descargar_plantilla_matriz(request):

    workbook = Workbook()

    hoja = workbook.active
    hoja.title = "Matriz de Alumnos"

    encabezados = [
        "ORD",
        "ESPECIALIDAD",
        "GRADO",
        "APELLIDO NOMBRE",
        "CEDULA",
        "N° FUSIL",
        "NOVEDADES",
        "NÚMERO DE SERIE",
        "TIPO",
        "MARCA",
        "MODELO",
        "CALIBRE",
        "ESTADO",
        "UBICACIÓN",
        "RESPONSABLE",
        "OBSERVACIONES",
    ]

    hoja.append(encabezados)

    # Formato de encabezados
    for celda in hoja[1]:
        celda.font = Font(bold=True)
        celda.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    # Ancho de columnas
    anchos = [
        8, 18, 15, 28, 14, 18, 22, 22,
        18, 15, 15, 15, 18, 22, 30, 30
    ]

    for numero, ancho in enumerate(anchos, start=1):
        hoja.column_dimensions[
            get_column_letter(numero)
        ].width = ancho

    # Congelar encabezados
    hoja.freeze_panes = "A2"

    # Filtro
    hoja.auto_filter.ref = "A1:P1"

    # Segunda hoja con instrucciones
    instrucciones = workbook.create_sheet(
        "Instrucciones"
    )

    instrucciones.append([
        "INSTRUCCIONES PARA LA IMPORTACIÓN"
    ])

    instrucciones.append([
        "No cambie los nombres de los encabezados de la hoja "
        "'Matriz de Alumnos'."
    ])

    instrucciones.append([
        "Complete una fila por cada alumno y su armamento."
    ])

    instrucciones.append([
        "APELLIDO NOMBRE",
        "Escriba primero los apellidos y después los nombres."
    ])

    instrucciones.append([
        "CEDULA",
        "Debe contener 10 dígitos."
    ])

    instrucciones.append([
        "N° FUSIL",
        "Código único del armamento."
    ])

    instrucciones.append([
        "TIPO",
        "Debe coincidir con un tipo de armamento registrado."
    ])

    instrucciones.append([
        "UBICACIÓN",
        "Debe coincidir con una ubicación registrada."
    ])

    instrucciones.append([
        "RESPONSABLE",
        "Debe coincidir con un responsable registrado."
    ])

    instrucciones.append([
        "ESTADO",
        "OPERABLE, MANTENIMIENTO o NO_OPERABLE."
    ])

    instrucciones.column_dimensions["A"].width = 30
    instrucciones.column_dimensions["B"].width = 90

    instrucciones["A1"].font = Font(
        bold=True,
        size=14
    )

    # Preparar respuesta
    respuesta = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    respuesta[
        "Content-Disposition"
    ] = (
        'attachment; '
        'filename="plantilla_matriz_alumnos_armamentos.xlsx"'
    )

    workbook.save(respuesta)

    return respuesta