from django.contrib import admin

from .models import ChoixActif, Simulation, Commentaire
admin.site.register(ChoixActif)
admin.site.register(Simulation)
admin.site.register(Commentaire)
