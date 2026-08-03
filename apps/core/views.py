from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.inventario.models import Armamento, Movimiento, Responsable

# Create your views here.
@login_required
def dashboard(request):

    total_armamentos = Armamento.objects.count()

    operables = Armamento.objects.filter(
        estado="OPERABLE"
    ).count()

    mantenimiento = Armamento.objects.filter(
        estado="MANTENIMIENTO"
    ).count()

    no_operables = Armamento.objects.filter(
        estado="NO_OPERABLE"
    ).count()

    responsables = Responsable.objects.filter(
        activo=True
    ).count()

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
    