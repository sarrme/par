from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
class ChoixActif(models.Model):
	nom_entreprise=models.CharField(max_length=20,help_text="entrer le nom de l'entreprise")
	decription_entreprise=models.TextField(max_length=1000,help_text="entrer une description")
	logo=models.ImageField(upload_to='logos')
	class Meta:
		ordering=['nom_entreprise']
	def get_absolute_url(self):
		return reverse('entreprises', args=[str(self.id)])
	def __str__(self):
		return self.nom_entreprise
class Simulation(models.Model):
	actifs=models.ManyToManyField(ChoixActif,help_text="Choisir un actif")
	date_debut=models.DateField(null=True, blank=True,help_text='Entrer la date du début de la simulation')
	date_fin=models.DateField(null=True, blank=True,help_text='Entrer la date de fin de la simulation')
	imagefirst=models.ImageField(upload_to='first')
	imagesecond=models.ImageField(upload_to='second')
	class Meta:
		ordering=['date_debut']
	def __str__(self):
		return '{} {} {}'.format(', '.join([ actif.nom_entreprise for actif in self.actifs.all()[:3] ]),self.date_debut,self.date_fin)
	def get_absolute_url(self):
		return reverse('simu', args=[str(self.id)])
class Commentaire(models.Model):
	simulation=models.ForeignKey(Simulation, on_delete=models.SET_NULL, null=True, blank=True)
	auteur=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	description=models.TextField(max_length=1000, help_text="Entrer un commentaire")
	date=models.DateField(auto_now_add=True)
	class Meta:
		ordering=['date']
	def get_absolute_url(self):
		return reverse('commentaires', args=[str(self.id)])
	def __str__(self):
		return '{} {} {}'.format(self.auteur,'comment '+self.description[:75],self.date)