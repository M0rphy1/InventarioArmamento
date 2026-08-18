from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.inventario.models import Armamento, Movimiento, Responsable


@login_required
def dashboard(request):

    # ==========================================
    # ARMAMENTOS ACTIVOS
    # ==========================================

    armamentos_activos = Armamento.objects.filter(
        activo=True
    )

    total_armamentos = armamentos_activos.count()

    operables = armamentos_activos.filter(
        estado="OPERABLE"
    ).count()

    mantenimiento = armamentos_activos.filter(
        estado="MANTENIMIENTO"
    ).count()

    no_operables = armamentos_activos.filter(
        estado="NO_OPERABLE"
    ).count()

    responsables = Responsable.objects.filter(
        activo=True
    ).count()


    # ==========================================
    # UBICACIÓN DE LOS ARMAMENTOS
    # ==========================================

    armamentos_armerillo = armamentos_activos.filter(
        ubicacion__nombre__iexact="Armería Principal"
    ).count()

    armamentos_fuera = total_armamentos - armamentos_armerillo


    # ==========================================
    # ÚLTIMOS MOVIMIENTOS
    # ==========================================

    ultimos_movimientos = (
        Movimiento.objects
        .select_related(
            "armamento",
            "usuario"
        )
        .order_by("-fecha")[:10]
    )


    # ==========================================
    # CONTEXTO
    # ==========================================

    context = {
        "total_armamentos": total_armamentos,
        "operables": operables,
        "mantenimiento": mantenimiento,
        "no_operables": no_operables,
        "responsables": responsables,

        "armamentos_armerillo": armamentos_armerillo,
        "armamentos_fuera": armamentos_fuera,

        "ultimos_movimientos": ultimos_movimientos,
    }


    return render(
        request,
        "dashboard/dashboard.html",
        context
    )