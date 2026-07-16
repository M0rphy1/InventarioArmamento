from django.shortcuts import render
from apps.inventario.models import Armamento, Movimiento

# Create your views here.
def dashboard(request):

    total_armamentos = Armamento.objects.count()

    disponibles = Armamento.objects.filter(
        estado="DISPONIBLE"
    ).count()

    prestados = Armamento.objects.filter(
        estado="PRESTADO"
    ).count()

    mantenimiento = Armamento.objects.filter(
        estado="MANTENIMIENTO"
    ).count()

    ultimos_movimientos = Movimiento.objects.select_related(
        "armamento"
    ).order_by("-fecha")[:5]

    context = {
        "total_armamentos": total_armamentos,
        "disponibles": disponibles,
        "prestados": prestados,
        "mantenimiento": mantenimiento,
        "ultimos_movimientos": ultimos_movimientos,
    }

    return render(request, "dashboard/dashboard.html", context)
    