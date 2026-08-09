from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.inventario.models import Armamento, Movimiento, Responsable

# Create your views here.
@login_required
def dashboard(request):

    # Solo se cuentan armamentos activos
    total_armamentos = Armamento.objects.filter(
        activo=True
    ).count()

    operables = Armamento.objects.filter(
        activo=True,
        estado="OPERABLE"
    ).count()

    mantenimiento = Armamento.objects.filter(
        activo=True,
        estado="MANTENIMIENTO"
    ).count()

    no_operables = Armamento.objects.filter(
        activo=True,
        estado="NO_OPERABLE"
    ).count()

    responsables = Responsable.objects.filter(
        activo=True
    ).count()

    # El historial sí incluye todos los movimientos,
    # incluso los de armamentos dados de baja.
    ultimos_movimientos = (
        Movimiento.objects
        .select_related(
            "armamento",
            "usuario"
        )
        .order_by("-fecha")[:10]
    )

    context = {
        "total_armamentos": total_armamentos,
        "operables": operables,
        "mantenimiento": mantenimiento,
        "no_operables": no_operables,
        "responsables": responsables,
        "ultimos_movimientos": ultimos_movimientos,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )