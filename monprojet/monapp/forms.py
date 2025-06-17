from django import forms
from .models import Services, Applications, UsageRessource, Utilisateurs, Serveurs, TypeServeurs

class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'


    def clean(self):
        cleaned_data = super().clean()
        serveur = cleaned_data.get('serveur_lancement')
        memoire_necessaire = cleaned_data.get('espace_memoire_utilise')

        if not serveur or not memoire_necessaire:
            return cleaned_data
        services_sur_serveur = Services.objects.filter(serveur_lancement=serveur)
        total_memoire_utilisee = sum(service.espace_memoire_utilise for service in services_sur_serveur)
        total_services = services_sur_serveur.count()

        memoire_disponible = serveur.capacite_stockage_serveurs - total_memoire_utilisee
        cpu_disponible = serveur.nombre_processeur_serveurs - total_services

        if memoire_necessaire > memoire_disponible:
            raise forms.ValidationError(f"Pas assez de mémoire disponible sur {serveur.nom_serveurs} (dispo : {memoire_disponible} Mo).")

        if cpu_disponible <= 0:
            raise forms.ValidationError(f"Pas assez de processeurs disponibles sur {serveur.nom_serveurs} (déjà {total_services} services actifs).")

        return cleaned_data

class ImportApplicationsForm(forms.Form):
    fichier = forms.FileField(label="Fichier JSON à importer")

class ApplicationsForm(forms.ModelForm):
    class Meta:
        model = Applications
        fields = '__all__'

    def clean(self):

        cleaned_data = super().clean()
        memoire_app = cleaned_data.get("memoire_utilisee")
        cpu_app = cleaned_data.get("cpu_utilise")
        if not self.instance.pk:
            return cleaned_data
        services_lies = UsageRessource.objects.filter(applications=self.instance)

        memoire_totale = memoire_app or 0
        cpu_total = cpu_app or 0


        for usage in services_lies:
            service = usage.services
            serveur = service.serveur_lancement
            memoire_totale += service.espace_memoire_utilise
            cpu_total += 1  # 1 service = 1 CPU

        if services_lies.exists():
            serveur = services_lies.first().services.serveur_lancement
            if memoire_totale > serveur.capacite_stockage_serveurs:
                raise forms.ValidationError(
                    f"Pas assez de stockage sur le serveur {serveur.nom_serveurs}. "
                    f"Disponible : {serveur.capacite_stockage_serveurs} Mo, requis : {memoire_totale} Mo."
                )
            if cpu_total > serveur.nombre_processeur_serveurs:
                raise forms.ValidationError(
                    f"Pas assez de CPU sur le serveur {serveur.nom_serveurs}. "
                    f"Disponible : {serveur.nombre_processeur_serveurs}, requis : {cpu_total}."
                )

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

