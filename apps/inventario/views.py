from django.shortcuts import render, redirect, get_object_or_404
from .models import Ubicacion, Armamento, TipoArmamento, Responsable, Movimiento
from .forms import UbicacionForm, ArmamentoForm, TipoArmamentoForm, ResponsableForm, MovimientoForm
from django.contrib import messages

from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test

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
@login_required
def lista_armamentos(request):

    buscar = request.GET.get("buscar", "")

    armamentos = Armamento.objects.all()

    if buscar:
        armamentos = armamentos.filter(
            Q(codigo__icontains=buscar) |
            Q(numero_serie__icontains=buscar) |
            Q(marca__icontains=buscar) |
            Q(modelo__icontains=buscar)
        )

    paginator = Paginator(armamentos, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "inventario/armamentos/lista.html",
        {
            "page_obj": page_obj,
            "buscar": buscar,
        }
    )

@login_required
@user_passes_test(es_administrador)
def crear_armamento(request):

    if request.method == "POST":

        form = ArmamentoForm(request.POST)

        if form.is_valid():
            form.save()

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

            form.save()

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
def eliminar_armamento(request, pk):

    armamento = get_object_or_404(
        Armamento,
        pk=pk
    )

    if request.method == "POST":

        armamento.delete()

        messages.success(
            request,
            "Armamento eliminado correctamente."
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

            movimiento.ubicacion_origen = armamento.ubicacion
            movimiento.responsable_anterior = armamento.responsable
            movimiento.estado_anterior = armamento.estado

            if movimiento.ubicacion_destino:
                armamento.ubicacion = movimiento.ubicacion_destino

            if movimiento.responsable_nuevo:
                armamento.responsable = movimiento.responsable_nuevo

            if movimiento.estado_nuevo:
                armamento.estado = movimiento.estado_nuevo

            # Si el movimiento es BAJA,
            # el armamento deja de estar activo.
            if movimiento.tipo == "BAJA":
                armamento.activo = False

            # Si se devuelve,
            # vuelve a estar activo.
            elif movimiento.tipo == "DEVOLUCION":
                armamento.activo = True

            armamento.save(
                update_fields=[
                    "ubicacion",
                    "responsable",
                    "estado",
                    "activo",
                ]
            )

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
def reporte_armamentos_pdf(request):
    return generar_reporte_armamentos_pdf(request)

