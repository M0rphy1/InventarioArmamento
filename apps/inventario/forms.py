from django import forms
from .models import Ubicacion, Armamento, TipoArmamento, Responsable, Movimiento


class UbicacionForm(forms.ModelForm):

    class Meta:
        model = Ubicacion
        fields = [
            "nombre",
            "descripcion",
        ]

        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
        }

class ArmamentoForm(forms.ModelForm):

    class Meta:
        model = Armamento
        fields = [
            "codigo",
            "numero_serie",
            "tipo",
            "marca",
            "modelo",
            "calibre",
            "numero_inventario",
            "anio_fabricacion",
            "estado",
            "ubicacion",
            "responsable",
            "fecha_ingreso",
            "observaciones",
            "activo",
        ]

        widgets = {
            "codigo": forms.TextInput(attrs={"class": "form-control"}),

            "numero_serie": forms.TextInput(attrs={"class": "form-control"}),

            "tipo": forms.Select(attrs={"class": "form-select"}),

            "marca": forms.TextInput(attrs={"class": "form-control"}),

            "modelo": forms.TextInput(attrs={"class": "form-control"}),

            "calibre": forms.TextInput(attrs={"class": "form-control"}),

            "numero_inventario": forms.TextInput(attrs={"class": "form-control"}),

            "anio_fabricacion": forms.NumberInput(attrs={"class": "form-control"}),

            "estado": forms.Select(attrs={"class": "form-select"}),

            "ubicacion": forms.Select(attrs={"class": "form-select"}),

            "responsable": forms.Select(attrs={"class": "form-select"}),

            "fecha_ingreso": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),

            "activo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

class TipoArmamentoForm(forms.ModelForm):

    class Meta:
        model = TipoArmamento
        fields = [
            "nombre",
            "descripcion",
        ]

        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
        }

class ResponsableForm(forms.ModelForm):

    class Meta:
        model = Responsable

        fields = [
            "grado",
            "cedula",
            "nombres",
            "apellidos",
            "cargo",
            "activo",
        ]

        widgets = {
            "grado": forms.Select(attrs={
                "class": "form-select"
            }),
            "cedula": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "nombres": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "apellidos": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "cargo": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "activo": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

class MovimientoForm(forms.ModelForm):

    class Meta:
        model = Movimiento

        fields = [
            "armamento",
            "tipo",
            "ubicacion_destino",
            "responsable_nuevo",
            "estado_nuevo",
            "observacion",
        ]

        widgets = {

            "armamento": forms.Select(attrs={
                "class": "form-select"
            }),

            "tipo": forms.Select(attrs={
                "class": "form-select"
            }),

            "ubicacion_destino": forms.Select(attrs={
                "class": "form-select"
            }),

            "responsable_nuevo": forms.Select(attrs={
                "class": "form-select"
            }),

            "estado_nuevo": forms.Select(attrs={
                "class": "form-select"
            }),

            "observacion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),

        }

def clean(self):

    cleaned_data = super().clean()

    tipo = cleaned_data.get("tipo")
    ubicacion = cleaned_data.get("ubicacion_destino")
    responsable = cleaned_data.get("responsable_nuevo")
    estado = cleaned_data.get("estado_nuevo")

    if tipo == "CAMBIO_UBICACION" and not ubicacion:
        self.add_error(
            "ubicacion_destino",
            "Debe seleccionar una ubicación."
        )

    if tipo == "CAMBIO_RESPONSABLE" and not responsable:
        self.add_error(
            "responsable_nuevo",
            "Debe seleccionar un responsable."
        )

    if tipo == "PRESTAMO":

        if not responsable:
            self.add_error(
                "responsable_nuevo",
                "Debe seleccionar un responsable."
            )

        cleaned_data["estado_nuevo"] = "PRESTADO"

    if tipo == "DEVOLUCION":
        cleaned_data["estado_nuevo"] = "DISPONIBLE"

    if tipo == "MANTENIMIENTO":
        cleaned_data["estado_nuevo"] = "MANTENIMIENTO"

    if tipo == "BAJA":
        cleaned_data["estado_nuevo"] = "BAJA"

    return cleaned_data