from django import forms
from .models import Ubicacion, Armamento, TipoArmamento, Responsable, Movimiento, Mantenimiento, Promocion, Alumno
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError

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
            self.fields["duenio"].disabled = True
            self.fields["responsable"].disabled = True

            self.fields["estado"].help_text = (
                "El estado solo puede modificarse desde el módulo Movimientos o Mantenimiento."
            )

            self.fields["ubicacion"].help_text = (
                "La ubicación solo puede modificarse desde el módulo Movimientos."
            )

            self.fields["duenio"].help_text = (
                "El dueño del fusil no puede modificarse desde este formulario."
            )

            self.fields["responsable"].help_text = (
                "El responsable del armerillo no puede modificarse desde este formulario."
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
            "estado",
            "ubicacion",
            "duenio",
            "responsable",
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

            "estado": forms.Select(attrs={"class": "form-select"}),

            "ubicacion": forms.Select(attrs={"class": "form-select"}),

            "duenio": forms.Select(attrs={
                "class": "form-select",
                "id": "id_duenio",
            }),

            "responsable": forms.Select(attrs={"class": "form-select"}),

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
                "class": "form-control",
                "inputmode": "numeric",
                "pattern": "[0-9]{10}",
                "maxlength": "10",
                "oninput": "this.value=this.value.replace(/[^0-9]/g,'')",
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
            "duenio_nuevo",
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

            "duenio_nuevo": forms.Select(attrs={
                "class": "form-select",
                "id": "id_duenio_nuevo",
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

            ("CAMBIO_UBICACION", "Cambio de ubicación"),

            ("CAMBIO_RESPONSABLE", "Cambio de responsable del armerillo"),

            ("CAMBIO_DUENIO", "Cambio de dueño"),

            ("NO_OPERABLE", "Marcar como No Operable"),

        ]

    def clean(self):

        cleaned_data = super().clean()

        tipo = cleaned_data.get("tipo")
        armamento = cleaned_data.get("armamento")
        ubicacion = cleaned_data.get("ubicacion_destino")
        responsable = cleaned_data.get("responsable_nuevo")
        duenio = cleaned_data.get("duenio_nuevo")

        # ==========================
        # Cambio de ubicación
        # ==========================

        if tipo == "CAMBIO_UBICACION":

            if not ubicacion:

                self.add_error(
                    "ubicacion_destino",
                    "Debe seleccionar una ubicación."
                )

        # ==========================
        # Cambio de responsable
        # ==========================

        if tipo == "CAMBIO_RESPONSABLE":

            if not responsable:

                self.add_error(
                    "responsable_nuevo",
                    "Debe seleccionar un responsable."
                )

        # ==========================
        # Cambio de dueño
        # ==========================

        if tipo == "CAMBIO_DUENIO":

            if not duenio:

                self.add_error(
                    "duenio_nuevo",
                    "Debe seleccionar el nuevo dueño."
                )

        # ==========================
        # No operable
        # ==========================

        if tipo == "NO_OPERABLE":

            if armamento and armamento.estado == "NO_OPERABLE":

                self.add_error(
                    "armamento",
                    "El armamento ya se encuentra marcado como No Operable."
                )

            cleaned_data["estado_nuevo"] = "NO_OPERABLE"

        return cleaned_data

class MantenimientoForm(forms.ModelForm):

    class Meta:

        model = Mantenimiento

        fields = [
            "armamento",
            "fecha_ingreso",
            "motivo",
            "descripcion",
            "responsable_armerillo",
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

            "responsable_armerillo": forms.Select(attrs={
                "class": "form-select"
            }),

            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        hoy = timezone.localdate()
        maximo = hoy + timedelta(days=180)

        self.fields["fecha_ingreso"].widget.attrs["min"] = hoy.isoformat()
        self.fields["fecha_ingreso"].widget.attrs["max"] = maximo.isoformat()
        self.fields["responsable_armerillo"].disabled = True


    def clean_fecha_ingreso(self):

        fecha = self.cleaned_data["fecha_ingreso"]

        hoy = timezone.localdate()
        maximo = hoy + timedelta(days=180)

        if fecha < hoy:

            raise ValidationError(
                "La fecha de ingreso no puede ser anterior a la fecha actual."
            )

        if fecha > maximo:

            raise ValidationError(
                "La fecha de ingreso no puede superar los 180 días desde hoy."
            )

        return fecha

    def clean_armamento(self):

        armamento = self.cleaned_data["armamento"]

        existe = Mantenimiento.objects.filter(
            armamento=armamento,
            estado="EN_PROCESO"
        ).exists()

        if existe:

            raise ValidationError(
                "Este armamento ya tiene un mantenimiento en proceso."
            )

        return armamento

class FinalizarMantenimientoForm(forms.ModelForm):

    class Meta:

        model = Mantenimiento

        fields = [
            "estado",
            "fecha_salida",
            "ubicacion_destino",
            "responsable_destino",
            "descripcion",
            "responsable_armerillo",
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

            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),

            "responsable_armerillo": forms.Select(attrs={
                "class": "form-select"
            }),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["estado"].choices = [
            ("FINALIZADO", "Finalizado")
        ]

        hoy = timezone.localdate()
        maximo = hoy + timedelta(days=180)

        self.fields["fecha_salida"].widget.attrs["min"] = hoy.isoformat()
        self.fields["fecha_salida"].widget.attrs["max"] = maximo.isoformat()
        if self.instance and self.instance.pk:
            self.fields["responsable_armerillo"].initial = self.instance.responsable_armerillo
            self.fields["responsable_armerillo"].disabled = True

    def clean_fecha_salida(self):

        fecha = self.cleaned_data["fecha_salida"]

        hoy = timezone.localdate()
        maximo = hoy + timedelta(days=180)

        if fecha < hoy:

            raise ValidationError(
                "La fecha de salida no puede ser anterior a la fecha actual."
            )

        if fecha > maximo:

            raise ValidationError(
                "La fecha de salida no puede superar los 180 días desde hoy."
            )

        return fecha

    def clean(self):

        cleaned_data = super().clean()

        fecha_ingreso = self.instance.fecha_ingreso
        fecha_salida = cleaned_data.get("fecha_salida")

        if fecha_salida and fecha_salida < fecha_ingreso:

            raise ValidationError(
                "La fecha de salida no puede ser anterior a la fecha de ingreso."
            )

        return cleaned_data

#Formulario para filtros Reportes
class ReporteArmamentoForm(forms.Form):

    responsables = forms.ModelMultipleChoiceField(

        queryset=Responsable.objects.filter(
            activo=True
        ).order_by("apellidos", "nombres"),

        required=False,

        widget=forms.SelectMultiple(attrs={
            "id": "id_responsables",
        })

    )

    armamentos = forms.ModelMultipleChoiceField(

        queryset=Armamento.objects.all().order_by("codigo"),

        required=False,

        widget=forms.SelectMultiple(attrs={
            "id": "id_armamentos",
        })

    )

    estado = forms.ChoiceField(

        required=False,

        choices=[

            ("", "Todos"),
            ("OPERABLE", "Operable"),
            ("MANTENIMIENTO", "Mantenimiento"),
            ("NO_OPERABLE", "No Operable"),

        ],

        widget=forms.Select(attrs={
            "class": "form-select"
        })

    )

    ubicacion = forms.ModelChoiceField(

        queryset=Ubicacion.objects.all(),

        required=False,

        empty_label="Todas",

        widget=forms.Select(attrs={
            "class": "form-select"
        })

    )

    tipo = forms.ModelChoiceField(

        queryset=TipoArmamento.objects.all(),

        required=False,

        empty_label="Todos",

        widget=forms.Select(attrs={
            "class": "form-select"
        })

    )

    promocion = forms.ModelChoiceField(

        queryset=Promocion.objects.filter(
            activa=True
        ).order_by("nombre"),

        required=False,

        empty_label="Todas las promociones",

        widget=forms.Select(attrs={
            "class": "form-select"
        })

    )

#Promocion
class PromocionForm(forms.ModelForm):

    class Meta:

        model = Promocion

        fields = [
            "nombre",
            "descripcion",
            "activa",
        ]

        widgets = {

            "nombre": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "descripcion": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "activa": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

        }

    def clean_nombre(self):

        nombre = self.cleaned_data["nombre"].strip().upper()

        existe = Promocion.objects.filter(
            nombre__iexact=nombre
        )

        if self.instance.pk:
            existe = existe.exclude(pk=self.instance.pk)

        if existe.exists():

            raise ValidationError(
                "Ya existe una promoción con ese nombre."
            )

        return nombre

#Alumno
class AlumnoForm(forms.ModelForm):

    class Meta:

        model = Alumno

        fields = [
            "promocion",
            "cedula",
            "nombres",
            "apellidos",
            "activo",
        ]

        widgets = {

            "promocion": forms.Select(attrs={
                "class": "form-select"
            }),

            "cedula": forms.TextInput(attrs={
                "class": "form-control",
                "inputmode": "numeric",
                "pattern": "[0-9]{10}",
                "maxlength": "10",
                "oninput": "this.value=this.value.replace(/[^0-9]/g,'')",
            }),

            "nombres": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "apellidos": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "activo": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

        }

    def clean_cedula(self):

        cedula = self.cleaned_data["cedula"].strip()

        existe = Alumno.objects.filter(
            cedula=cedula
        )

        if self.instance.pk:

            existe = existe.exclude(pk=self.instance.pk)

        if existe.exists():

            raise ValidationError(
                "Ya existe un alumno con esa cédula."
            )

        return cedula

    def clean_nombres(self):

        return self.cleaned_data["nombres"].strip().upper()

    def clean_apellidos(self):

        return self.cleaned_data["apellidos"].strip().upper()

class ReporteAlumnoForm(forms.Form):

    promocion = forms.ModelChoiceField(

        queryset=Promocion.objects.filter(
            activa=True
        ).order_by("nombre"),

        required=False,

        empty_label="Todas las promociones",

        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )