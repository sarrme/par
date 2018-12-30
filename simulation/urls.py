
from django.urls import path
from . import views
urlpatterns = [
	path('',views.index, name='index'),
	path('entreprises/',views.EntrepriseList.as_view(),name='actifs'),
	path('entreprise/<int:pk>',views.EntrepriseDetail.as_view(),name='entreprises'),
	]
urlpatterns += [  
	path('change/',views.showsimlation,name='tolearn'),
    path('pagesimu/<int:pk>',views.SimulationDetail.as_view(),name='simu'),
	path('pagesimu/<int:pk>/commentaire/', views.CommentaireCreate.as_view(), name='blog-comment'),
]
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
