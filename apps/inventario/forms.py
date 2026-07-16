from django import forms
from .models import Ubicacion, Armamento, TipoArmamento


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