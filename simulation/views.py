
from django.shortcuts import render
from .forms import ChoixForm
from .models import ChoixActif, Simulation, Commentaire
from django.contrib.auth.models import User
def index(request):
	num_entreprise=ChoixActif.objects.all().count()
	return render(
        request,
        'index.html',
        context={'num_entreprise':num_entreprise},)
from django.views import generic
class EntrepriseList(generic.ListView):
	model=ChoixActif
	paginate_by=10
class EntrepriseDetail(generic.DetailView):
	model=ChoixActif

class SimulationDetail(generic.DetailView):
	model= Simulation
from django.core.files import File
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
def showsimlation(request):
    simul=get_object_or_404(Simulation,pk=1)
    if request.method == 'POST':
        form = ChoixForm(request.POST)
        if form.is_valid():

			
            choix={'GOOGLE':'GOOGL','AMAZON':'AMZN','FORD':'F','APPLE':'AAPL','EXXON':'XOM','WALMART':'WMT'}
            source = 'iex'
            start=form.cleaned_data.get('date_debut')
            end=form.cleaned_data.get('date_fin')
            choices=form.cleaned_data.get('actifs')
            actions=[ choix[choice.nom_entreprise] for choice in choices]
            numAActifs = len(actions)
            #RExtraire les données online
            data = coursBourses(actions, source, start, end)
			

            #Calculer les rendements
            Sansrisq = 0.0021
            dur = 20
            # Information: utilisation de 252 jours car les jours de travail sont de 252 jours par année
            numPeriodesAnnee = 252.0/dur
            donneePeriode = data[::dur]
            rets = np.log(donneePeriode/donneePeriode.shift(1))

            #Calculer l'espérance et la variance de l'action
            espJourRend = rets.mean()
            covariance = rets.cov()

            #Créer une nouvelle figure
            plt.figure(figsize=(8,6))

            #simulation par la méthode de Monte Carlo des portefeuilles
            numPortfolios = 100000
            resultats = np.zeros((3,numPortfolios))

            #Calculer les portefeuilles
            for i in range(numPortfolios):
                #générer un échantillon de nombres aléatoires normalisé de taille numAActifs qui représentent les poids de chaque portefeuille
                poids = np.random.random(numAActifs)
                poids /= np.sum(poids)
    
                #Calcul du rendement attendu et de la volatilité du portefeuille
                pret, pvar = calcPerfPortfeuille(poids, espJourRend, covariance)
    
                #Convertir les résultats en base annuelle, calculer le ratio de Sharpe et les stocker
                resultats[0,i] = float(pret*numPeriodesAnnee)
                resultats[1,i] = float(pvar*np.sqrt(numPeriodesAnnee))
                resultats[2,i] = float((resultats[0,i] - Sansrisq)/resultats[1,i])
    
            #Tracer les résultats de la méthode de Monte Carlo en utilisant les poids générés précédement
            plt.scatter(resultats[1,:], resultats[0,:], c=resultats[2,:], marker='o')

            #Trouver une frontière efficace, les rendements cibles annuels de 9% et 16% sont convertis pour
            # correspondre à la période des rendements moyens calculée précédemment

            targetReturns = np.linspace(-0.1, 0.26, 50)/(252./dur)
            efficientPortfolios = frontierMarkowitz(espJourRend, covariance, targetReturns)
            plt.plot([p['fun']*np.sqrt(numPeriodesAnnee) for p in efficientPortfolios], targetReturns*numPeriodesAnnee, marker='x')

            #Trouver le portefeuille avec un ratio de Sharpe maximal
            maxSharpe = ratioSharpeMax(espJourRend, covariance, Sansrisq)
            rp, sdp = calcPerfPortfeuille(maxSharpe['x'], espJourRend, covariance)
            plt.plot(sdp*np.sqrt(numPeriodesAnnee), rp*numPeriodesAnnee, 'r*', markersize=15.0)

            #Trouver un portefeuille avec une variance minimal 
            minVar = portefeuilleMinVariance(espJourRend, covariance)
            rp, sdp = calcPerfPortfeuille(minVar['x'], espJourRend, covariance)
            plt.plot(sdp*np.sqrt(numPeriodesAnnee), rp*numPeriodesAnnee, 'y*', markersize=15.0)
            plt.grid(True)
            plt.xlabel('La volatilité attendue')
            plt.ylabel('le rendement attendu')
            plt.colorbar(label='le ratio de Sharpe')
            plt.title('Portefeuille avec plusieurs actifs')
            plt.tight_layout()
            simul.imagesecond.delete()
            simul.imagefirst.delete()
            plt.savefig("media/first/first.png", dpi=100)

            ind = np.arange(numAActifs)
            width = 0.35
            fig, ax = plt.subplots(figsize=(8,6))
            rects1 = ax.bar(ind, maxSharpe['x'], width, color='r', alpha=0.75)
            rects2 = ax.bar(ind + width, minVar['x'], width, color='#6699ff', alpha=0.75)
            ax.set_ylabel("le poids d'un actif d'un portefeuille")
            ax.set_ylim(0,1)
            ax.set_title("Comparaison de la composition d'un portefeuille")
            ax.set_xticks(ind + width)
            ax.set_xticklabels(actions)
            plt.tight_layout()
            ax.legend((rects1[0], rects2[0]), ('ratio de Sharpe maximal', 'Volatilité minimale'))
            plt.savefig('media/second/second.png', dpi=100)
            reopen1 = open("media/first/first.png", 'rb')
            django_file1 = File(reopen1)
            reopen2 = open("media/second/second.png", 'rb')
            django_file2 = File(reopen2)
            simul.date_debut=form.cleaned_data.get('date_debut')
            simul.date_fin=form.cleaned_data.get('date_fin')
            simul.actifs.set(form.cleaned_data.get('actifs'))
            simul.imagefirst.save('first.png', django_file1, save=True)
            simul.imagesecond.save('second.png', django_file2, save=True)
            simul.save()
            return HttpResponseRedirect(reverse('simu', kwargs={'pk':1,}) )
    else:
        form = ChoixForm

    return render(request, 'simulation/tolearn.html', {'form': form})

import pandas_datareader.data as web
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import scipy.optimize as sco
def coursBourses(symboles, source, dateDepart, dateFin):
    actions = pd.DataFrame()
    for symbole in symboles:
        actions[symbole] = web.DataReader(symbole, data_source=source, start=dateDepart, end=dateFin)['close']
    return actions
def calcPerfPortfeuille(poids, esperances, matriceCov):
    '''
    Calculer l'espérance attendue pour les rendements et la volatilité pour un portefeuille constitué des actifs,
    chaque actif est associé à un poid spécifique.
    ENTREE
    poids: une list sous la forme d'un array qui spécifie le poid de chaque actif
    esperances: la valeur de l'ésperance calculé pour chaque actif
    matriceCov: La covariance pour chaque actif du portefeuille
    SORTIE:
    tuple contenant la volatilité et le rendement de chaque portefeuille
    '''    
    #Calculer le rendement et la covariance
    portReturn = np.sum( esperances*poids )
    portStdDev = np.sqrt(np.dot(poids.T, np.dot(matriceCov, poids)))
    return portReturn, portStdDev
def oppRatioSharpe(poids, esperances, matriceCov, Sansrisq):
    '''
    donne l'opposé du ratio de Sharpe pour un portfolio constitué des actifs spécifiques
    ENTREE:
    poids: une list sous la forme d'un array qui spécifie le poid de chaque actif
    esperances: la valeur de l'espérance calculé pour chaque actif
    matriceCov: La covariance pour chaque actif du pportefeuille
    Sansrisq: la valeur temporelle de l'argent 
    '''
    p_ret, p_var = calcPerfPortfeuille(poids, esperances, matriceCov)
    return -(p_ret - Sansrisq) / p_var
def VolPortefeuille(poids, esperances, matriceCov):
    '''
    Returns the volatility of the specified portfolio of assets
    Donne accès à la volatilité d'un portefeuille constitué des actifs spécifiques
    ENTREE:
    poids: une list sous la forme d'un array qui spécifie le poid de chaque actif
    esperances: la valeur de l'espérance calculé pour chaque actif
    matriceCov: La covariance pour chaque actif du portefeuille
    SORTIE:
    la volatilité d'un portefeuille
    '''
    return calcPerfPortfeuille(poids, esperances, matriceCov)[1]
def ratioSharpeMax(esperances, matriceCov, Sansrisq):
    '''
    Chercher le portedeuille qui permet de maximiser le ratio de Sharpe
    la volatilité d'un portefeuille
    ENTREE:
    poids: une list sous la forme d'un array qui spécifie le poid de chaque actif
    esperances: la valeur de l'espérance calculé pour chaque actif
    matriceCov: La covariance pour chaque actif du portefeuille
    '''
    numAActifs = len(esperances)
    args = (esperances, matriceCov, Sansrisq)
    constraintes = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    contraintes = tuple( (0,1) for asset in range(numAActifs))
    opts = sco.minimize(oppRatioSharpe, numAActifs*[1./numAActifs,], args=args, method='SLSQP', bounds=contraintes, constraints=constraintes)
    
    return opts
def portefeuilleMinVariance(esperances, matriceCov):
    '''
    Chercher le portefeuille qui a une volatilité minimal
    
    ENTREE:
    esperances: la valeur de l'espérance calculée pour chaque actif
    matriceCov: La covariance pour chaque actif du portefeuille
    '''
    numAActifs = len(esperances)
    args = (esperances, matriceCov)
    constraintes = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bornes = tuple( (0,1) for asset in range(numAActifs))
    opts = sco.minimize(VolPortefeuille, numAActifs*[1./numAActifs,], args=args, method='SLSQP', bounds=bornes, constraints=constraintes)
    
    return opts

def rendOptimal(esperances, matriceCov, targetReturn):
    '''
    Trouver le portefeuille des actifs le rendement cible avec la plus basse volatilité
    
    ENTREE:
    esperances: la valeur de l'espérance calculée pour chaque actif
    matriceCov: La covariance pour chaque actif du portefeuille
    rendCible: le taux annuel du rendement attendu cible
    
    SORTIE:
    Un dictionaire qui représente les résultats de l'optimisation
    '''
    numAActifs = len(esperances)
    args = (esperances, matriceCov)
    def RendPortefeuille(poids):
        return calcPerfPortfeuille(poids, esperances, matriceCov)[0]
    constraintes = ({'type': 'eq', 'fun': lambda x: RendPortefeuille(x) - targetReturn},
                   {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bornes = tuple((0,1) for asset in range(numAActifs))
    return sco.minimize(VolPortefeuille, numAActifs*[1./numAActifs,], args=args, method='SLSQP', bounds=bornes, constraints=constraintes)
def frontierMarkowitz(esperances, matriceCov, rangeOfReturns):
    '''
    Trouver l'ensemble des portefeuilles comprenant la frontière efficace
    
    ENTREE:
    esperances: la valeur de l'espérance calculé pour chaque actif
    matriceCov: La covariance pour chaque actif du portefeuille
    rendCible: le taux annuel du rendement attendu cible
    
    SORTIE:
    Un dictionaire qui représente les résultats de l'optimisation
    '''
    efficientPortfolios = []
    for ret in rangeOfReturns:
        efficientPortfolios.append(rendOptimal(esperances, matriceCov, ret))
        
    return efficientPortfolios 
	
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
class CommentaireCreate(CreateView):
	model=Commentaire
	fields=['description',]
	def get_context_data(self, **kwargs):
		context = super(CommentaireCreate, self).get_context_data(**kwargs)
		context['simulation'] = get_object_or_404(Simulation, pk = self.kwargs['pk'])
		return context
	def form_valid(self, form):
		form.instance.auteur = self.request.user
		form.instance.simulation=get_object_or_404(Simulation, pk = self.kwargs['pk'])
		return super(CommentaireCreate, self).form_valid(form)
	def get_success_url(self): 
		return reverse('simu', kwargs={'pk': 1,})