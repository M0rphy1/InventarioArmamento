from django.shortcuts import render
from apps.inventario.models import Armamento, Movimiento, Responsable

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
        "armamento",
        "usuario"
    ).order_by("-fecha")[:10]

    bajas = Armamento.objects.filter(
        estado="BAJA"
    ).count()

    responsables = Responsable.objects.filter(
        activo=True
    ).count()

    context = {
        "total_armamentos": total_armamentos,
        "disponibles": disponibles,
        "prestados": prestados,
        "mantenimiento": mantenimiento,
        "ultimos_movimientos": ultimos_movimientos,
        "bajas": bajas,
        "responsables": responsables,
    }

    return render(request, "dashboard/dashboard.html", context)
    