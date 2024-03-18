from django import forms
from primary.models import persona, doctor
from tertiary.models import cita

class DoctorForm(forms.ModelForm):
    class Meta:
        model = doctor
        fields = ['rec_senecyt', 'especialidad', 'institucion']

        def clean_rec_senecyt(self):
            rec_senecyt = self.cleaned_data.get('rec_senecyt')
            if len(rec_senecyt) > 10:  # Limitar a 10 caracteres
                raise forms.ValidationError("El campo rec_senecyt no puede tener más de 10 caracteres.")
            return rec_senecyt

        def clean_especialidad(self):
            especialidad = self.cleaned_data.get('especialidad')
            if len(especialidad) > 50:  # Limitar a 50 caracteres
                raise forms.ValidationError("El campo especialidad no puede tener más de 50 caracteres.")
            return especialidad

        def clean_institucion(self):
            institucion = self.cleaned_data.get('institucion')
            if len(institucion) > 100:  # Limitar a 100 caracteres
                raise forms.ValidationError("El campo institucion no puede tener más de 100 caracteres.")
            return institucion

        def error_css_class(self):
            return 'is-danger'

class CitaForm(forms.ModelForm):
    class Meta:
        model = cita
        fields = ['fecha', 'hora', 'detalle']

class SeleccionPacienteForm(forms.Form):
    paciente = forms.ChoiceField(choices=[], required=True)
    fecha_desde = forms.DateField(label='Fecha Desde', required=True)
    fecha_hasta = forms.DateField(label='Fecha Hasta', required=True)

    def __init__(self, *args, **kwargs):
        pacientes = kwargs.pop('pacientes', [])
        super(SeleccionPacienteForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].choices = pacientes