from django.db import models
from email.policy import default
from django.core.exceptions import ValidationError
from django.db.models import Sum
#from monapp.models import Services, UsageRessource

class Serveurs(models.Model):
    nom_serveurs = models.CharField(max_length=100, default="serveur_test")  # Ajout d'un default pour éviter problème migration
    type_serveur = models.ForeignKey("TypeServeurs", on_delete=models.CASCADE, default=None)  # Clé étrangère, renommée au singulier pour clarifier
    nombre_processeur_serveurs = models.IntegerField(default=100, blank=False)
    capacite_memoire_serveurs = models.IntegerField(default=100)
    capacite_stockage_serveurs = models.IntegerField(default=100)

    def __str__(self):
        return self.nom_serveurs

    def dico(self):
        return {
            "Nom": self.nom_serveurs,
            "Type": self.type_serveur,
            "Nombre de Processeur(s)": self.nombre_processeur_serveurs,
            "Capacité de la mémoire": self.capacite_memoire_serveurs,
            "Capacité de stockage": self.capacite_stockage_serveurs,
        }

class Services(models.Model):
    nom_services = models.CharField(max_length=100)
    date_lancement = models.DateField()
    espace_memoire_utilise = models.IntegerField(help_text="en Mo")
    memoire_vive_necessaire = models.IntegerField(help_text="en Mo")
    serveur_lancement = models.ForeignKey(Serveurs, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_services

    def dico(self):
        return {"Nom":self.nom_services,"Date":self.date_lancement, "Espace mémoire utilisé":self.espace_memoire_utilise, "Mémoire vive nécessaire":self.memoire_vive_necessaire,"Serveur de lancement":self.serveur_lancement}


class Utilisateurs(models.Model):
    nom_utilisateurs = models.CharField(max_length=100)
    prenom_utilisateurs = models.CharField(max_length=100)
    email_utilisateurs = models.EmailField(blank=False)

    def __str__(self):
        return f"{self.prenom_utilisateurs} {self.nom_utilisateurs}"

    def dico(self):
        return {"Nom":self.nom_utilisateurs,"Prenom":self.prenom_utilisateurs,"Email":self.email_utilisateurs}



class Applications(models.Model):
    nom_applications = models.CharField(max_length=100)
    logo_applications = models.ImageField(upload_to='logos/', null=True, blank=True)
    utilisateur_applications = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE)
    memoire_utilisee = models.IntegerField(help_text="Mémoire utilisée en Mo", default=0)
    cpu_utilise = models.IntegerField(help_text="Nombre de CPU nécessaires", default=1)

    def __str__(self):
        return self.nom_applications

    def clean(self):

        usages = UsageRessource.objects.filter(applications=self)
        services_lies = Services.objects.filter(id__in=usages.values_list('services', flat=True))

        if not services_lies.exists():
            return


        serveur = services_lies.first().serveur_lancement


        memoire_services = Services.objects.filter(serveur_lancement=serveur).aggregate(
            total=Sum('espace_memoire_utilise')
        )['total'] or 0

        memoire_totale = memoire_services + self.memoire_utilisee

        if memoire_totale > serveur.capacite_stockage_serveurs:
            raise ValidationError(
                f"🚫 Impossible d'ajouter cette application. "
                f"La mémoire totale ({memoire_totale} Mo) dépasse la capacité du serveur "
                f"{serveur.nom_serveurs} ({serveur.capacite_stockage_serveurs} Mo)."
            )

    def dico(self):
        return {
            "Nom": self.nom_applications,
            "Logo": self.logo_applications,
            "Utilisateurs": self.utilisateur_applications,
            "Mémoire utilisée": self.memoire_utilisee,
            "CPU utilisés": self.cpu_utilise
        }


class UsageRessource(models.Model):
    applications = models.ForeignKey(Applications, on_delete=models.CASCADE)
    services = models.ForeignKey(Services, on_delete=models.CASCADE)
    type_ressource = models.CharField(max_length=50, choices=[
        ("Web", "Web"),
        ("DB", "Base de données"),
        ("Stockage", "Stockage"),
    ])

    def __str__(self):
        return f"{self.applications} utilise {self.services} ({self.type_ressource})"

    def dico(self):
        return {"Application":self.applications,"Services":self.services,"Type de ressource":self.type_ressource}

class TypeServeurs(models.Model):
    type = models.CharField(max_length=100)
    description_serveurs = models.TextField(blank=False)

    def __str__(self):
        return f"{self.type}"

    def dico(self):
        return {"Type":self.type,"Description":self.description_serveurs}