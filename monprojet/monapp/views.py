from django.shortcuts import render, redirect, get_object_or_404
from .models import Services, Applications, UsageRessource, Utilisateurs, Serveurs, TypeServeurs
from .forms import ServicesForm, ApplicationsForm, UsageRessourceForm, UtilisateursForm, ServeursForm, TypeServeursForm,ImportApplicationsForm
from django.views.generic.edit import CreateView
import json
from django.contrib import messages

#PAGE D'ACCUEIL

def home(request):
    return render(request, 'monapp/home.html')

# SERVICES
def services_list(request):
    services = Services.objects.all()
    return render(request, 'monapp/services_list.html', {'services': services})

def services_create(request):
    form = ServicesForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('services_list')
    return render(request, 'monapp/services_form.html', {'form': form})

def services_update(request, pk):
    service = get_object_or_404(Services, pk=pk)
    form = ServicesForm(request.POST or None, instance=service)
    if form.is_valid():
        form.save()
        return redirect('services_list')
    return render(request, 'monapp/services_form.html', {'form': form})

def services_delete(request, pk):
    service = get_object_or_404(Services, pk=pk)
    service.delete()
    return redirect('services_list')

def services_affiche(request):
    services = Services.objects.all()
    return render(request, 'monapp/services_affiche.html', {'services': services})


# APPLICATIONS
def applications_list(request):
    apps = Applications.objects.all()
    return render(request, 'monapp/applications_list.html', {'apps': apps})

def applications_create(request):
    form = ApplicationsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('applications_list')
    return render(request, 'monapp/applications_form.html', {'form': form})

def applications_update(request, pk):
    app = get_object_or_404(Applications, pk=pk)
    form = ApplicationsForm(request.POST or None, request.FILES or None, instance=app)
    if form.is_valid():
        form.save()
        return redirect('applications_list')
    return render(request, 'monapp/applications_form.html', {'form': form})

def applications_delete(request, pk):
    app = get_object_or_404(Applications, pk=pk)
    app.delete()
    return redirect('applications_list')

def applications_affiche(request):
    applications = Applications.objects.all()
    return render(request, 'monapp/applications_affiche.html', {'applications': applications})

class ApplicationsCreateView(CreateView):
    model = Applications
    form_class = ApplicationsForm
    template_name = 'applications_create.html'
    success_url = '/applications/new/'

def import_applications(request):
    if request.method == 'POST':
        form = ImportApplicationsForm(request.POST, request.FILES)
        if form.is_valid():
            fichier = request.FILES['fichier']
            try:
                data = json.load(fichier)


                serveur = Serveurs.objects.get(id=data['serveur_id'])


                services_existants = Services.objects.filter(serveur_lancement=serveur)
                memoire_utilisee = sum(s.espace_memoire_utilise for s in services_existants)
                cpu_utilise = sum(s.applications_set.count() for s in services_existants)  # Ou une autre logique CPU si dispo


                app_memoire = data['application']['memoire_utilisee']
                app_cpu = data['application']['cpu_utilise']


                if app_memoire + memoire_utilisee > serveur.capacite_stockage_serveurs:
                    messages.error(request, "Mémoire insuffisante sur le serveur pour cette application.")
                    return redirect('import_application')

                if app_cpu + cpu_utilise > serveur.nombre_processeur_serveurs:
                    messages.error(request, "CPU insuffisant sur le serveur pour cette application.")
                    return redirect('import_application')

                utilisateur = Utilisateurs.objects.get(id=data['application']['utilisateur_id'])
                app = Applications.objects.create(
                    nom_applications=data['application']['nom'],
                    memoire_utilisee=app_memoire,
                    cpu_utilise=app_cpu,
                    utilisateur_applications=utilisateur
                )


                for service_data in data['services']:
                    service = Services.objects.create(
                        nom_services=service_data['nom_services'],
                        espace_memoire_utilise=service_data['espace_memoire_utilise'],
                        serveur_lancement=serveur
                    )
                    UsageRessource.objects.create(applications=app, services=service)

                messages.success(request, "Application et services importés avec succès !")
                return redirect('applications_list')

            except Exception as e:
                messages.error(request, f"Erreur lors de l'import : {str(e)}")
    else:
        form = ImportApplicationsForm()

    return render(request, 'monapp/import_applications.html', {'form': form})

# USAGE RESSOURCES
def usageressource_list(request):
    usages = UsageRessource.objects.all()
    return render(request, 'monapp/usageressource_list.html', {'usages': usages})

def usageressource_create(request):
    form = UsageRessourceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('usageressource_list')
    return render(request, 'monapp/usageressource_form.html', {'form': form})

def usageressource_update(request, pk):
    usage = get_object_or_404(UsageRessource, pk=pk)
    form = UsageRessourceForm(request.POST or None, instance=usage)
    if form.is_valid():
        form.save()
        return redirect('usageressource_list')
    return render(request, 'monapp/usageressource_form.html', {'form': form})

def usageressource_delete(request, pk):
    usage = get_object_or_404(UsageRessource, pk=pk)
    usage.delete()
    return redirect('usageressource_list')

def usageressource_affiche(request):
    usageressources = UsageRessource.objects.all()
    return render(request, 'monapp/usageressource_affiche.html', {'usageressources': usageressources})

# TYPESERVEURS

def type_de_serveurs_list(request):
    types = TypeServeurs.objects.all()
    return render(request, 'monapp/type_de_serveurs_list.html', {'types': types})

def type_de_serveurs_create(request):
    form = TypeServeursForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('type_de_serveurs_list')
    return render(request, 'monapp/type_de_serveurs_form.html', {'form': form})

def type_de_serveurs_update(request, pk):
    type = get_object_or_404(TypeServeurs, pk=pk)
    form = TypeServeursForm(request.POST or None, instance=type)
    if form.is_valid():
        form.save()
        return redirect('type_de_serveurs_list')
    return render(request, 'monapp/type_de_serveurs_form.html', {'form': form})

def type_de_serveurs_delete(request, pk):
    type = get_object_or_404(TypeServeurs, pk=pk)
    type.delete()
    return redirect('type_de_serveurs_list')

# SERVEURS

def serveurs_list(request):
    serveurs = Serveurs.objects.all()
    return render(request, 'monapp/serveurs_list.html', {'serveurs': serveurs})

def serveurs_create(request):
    form = ServeursForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('serveurs_list')
    return render(request, 'monapp/serveurs_form.html', {'form': form})

def serveurs_update(request, pk):
    serveur = get_object_or_404(Serveurs, pk=pk)
    form = ServeursForm(request.POST or None, instance=serveur)
    if form.is_valid():
        form.save()
        return redirect('serveurs_list')
    return render(request, 'monapp/serveurs_form.html', {'form': form})

def serveurs_delete(request, pk):
    serveur = get_object_or_404(Serveurs, pk=pk)
    serveur.delete()
    return redirect('serveurs_list')

def serveurs_affiche(request):
    serveurs = Serveurs.objects.all()
    return render(request, 'monapp/serveurs_affiche.html', {'serveurs': serveurs})

# UTILISATEURS
def utilisateurs_list(request):
    utilisateurs = Utilisateurs.objects.all()
    return render(request, 'monapp/utilisateurs_list.html', {'utilisateurs': utilisateurs})

def utilisateurs_create(request):
    form = UtilisateursForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('utilisateurs_list')
    return render(request, 'monapp/utilisateurs_form.html', {'form': form})

def utilisateurs_update(request, pk):
    utilisateur= get_object_or_404(Utilisateurs, pk=pk)
    form = UtilisateursForm(request.POST or None, request.FILES or None, instance=utilisateur)
    if form.is_valid():
        form.save()
        return redirect('utilisateurs_list')
    return render(request, 'monapp/utilisateurs_form.html', {'form': form})

def utilisateurs_delete(request, pk):
    utilisateur = get_object_or_404(Utilisateurs, pk=pk)
    utilisateur.delete()
    return redirect('utilisateurs_list')