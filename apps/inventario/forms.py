from django import forms
from .models import Ubicacion, Armamento, TipoArmamento, Responsable, Movimiento, Mantenimiento


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

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Si existe una instancia, estamos editando
        if self.instance and self.instance.pk:

            self.fields["estado"].disabled = True
            self.fields["ubicacion"].disabled = True
            self.fields["responsable"].disabled = True

            self.fields["estado"].help_text = (
                "El estado solo puede modificarse desde el módulo Movimientos o Mantenimiento."
            )

            self.fields["ubicacion"].help_text = (
                "La ubicación solo puede modificarse desde el módulo Movimientos."
            )

            self.fields["responsable"].help_text = (
                "El responsable solo puede modificarse desde el módulo Movimientos."
            )

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

            "observacion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["tipo"].choices = [
            ("INGRESO", "Ingreso"),
            ("SALIDA", "Salida"),
            ("PRESTAMO", "Préstamo"),
            ("DEVOLUCION", "Devolución"),
            ("CAMBIO_UBICACION", "Cambio de ubicación"),
            ("CAMBIO_RESPONSABLE", "Cambio de responsable"),
            ("BAJA", "Baja"),
        ]

    def clean(self):

        cleaned_data = super().clean()

        tipo = cleaned_data.get("tipo")
        armamento = cleaned_data.get("armamento")
        ubicacion = cleaned_data.get("ubicacion_destino")
        responsable = cleaned_data.get("responsable_nuevo")

        # ===============================
        # CAMBIO DE UBICACIÓN
        # ===============================

        if tipo == "CAMBIO_UBICACION":

            if not ubicacion:

                self.add_error(
                    "ubicacion_destino",
                    "Debe seleccionar una ubicación."
                )

        # ===============================
        # CAMBIO DE RESPONSABLE
        # ===============================

        if tipo == "CAMBIO_RESPONSABLE":

            if not responsable:

                self.add_error(
                    "responsable_nuevo",
                    "Debe seleccionar un responsable."
                )

        # ===============================
        # PRÉSTAMO
        # ===============================

        if tipo == "PRESTAMO":

            if not responsable:

                self.add_error(
                    "responsable_nuevo",
                    "Debe seleccionar un responsable."
                )

            if armamento:

                if armamento.estado == "PRESTADO":

                    self.add_error(
                        "armamento",
                        "Este armamento ya se encuentra prestado."
                    )

                elif armamento.estado == "MANTENIMIENTO":

                    self.add_error(
                        "armamento",
                        "El armamento está en mantenimiento."
                    )

                elif armamento.estado == "BAJA":

                    self.add_error(
                        "armamento",
                        "El armamento se encuentra dado de baja."
                    )

            cleaned_data["estado_nuevo"] = "PRESTADO"

        # ===============================
        # DEVOLUCIÓN
        # ===============================

        if tipo == "DEVOLUCION":

            if armamento and armamento.estado != "PRESTADO":

                self.add_error(
                    "armamento",
                    "Este armamento no se encuentra prestado."
                )

            cleaned_data["estado_nuevo"] = "DISPONIBLE"

        # ===============================
        # BAJA
        # ===============================

        if tipo == "BAJA":

            if armamento and armamento.estado == "BAJA":

                self.add_error(
                    "armamento",
                    "El armamento ya se encuentra dado de baja."
                )

            cleaned_data["estado_nuevo"] = "BAJA"

        return cleaned_data

class MantenimientoForm(forms.ModelForm):

    class Meta:

        model = Mantenimiento

        fields = [
            "armamento",
            "fecha_ingreso",
            "motivo",
            "descripcion",
            "tecnico",
        ]

        widgets = {

            "armamento": forms.Select(attrs={
                "class": "form-select"
            }),

            "fecha_ingreso": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "motivo": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),

            "tecnico": forms.TextInput(attrs={
                "class": "form-control"
            }),

        }

class FinalizarMantenimientoForm(forms.ModelForm):

    class Meta:

        model = Mantenimiento

        fields = [
            "estado",
            "fecha_salida",
            "ubicacion_destino",
            "responsable_destino",
            "descripcion",
            "tecnico",
        ]

        widgets = {

            "estado": forms.Select(attrs={
                "class": "form-select"
            }),

            "fecha_salida": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "ubicacion_destino": forms.Select(attrs={
                "class": "form-select"
            }),

            "responsable_destino": forms.Select(attrs={
                "class": "form-select"
            }),

            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),

            "tecnico": forms.TextInput(attrs={
                "class": "form-control"
            }),

        }

def __init__(self, *args, **kwargs):

    super().__init__(*args, **kwargs)

    self.fields["estado"].choices = [
        ("FINALIZADO", "Finalizado")
    ]