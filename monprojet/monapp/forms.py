from django import forms
from .models import Services, Applications, UsageRessource, Utilisateurs, Serveurs, TypeServeurs

class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'

class ApplicationsForm(forms.ModelForm):
    class Meta:
        model = Applications
        fields = '__all__'

class UsageRessourceForm(forms.ModelForm):
    class Meta:
        model = UsageRessource
        fields = '__all__'

class ServeursForm(forms.ModelForm):
    class Meta:
        model = Serveurs
        fields = '__all__'

class UtilisateursForm(forms.ModelForm):
    class Meta:
        model = Utilisateurs
        fields = '__all__'

class TypeServeursForm(forms.ModelForm):
    class Meta:
        model = TypeServeurs
        fields = '__all__'

