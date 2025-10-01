from django.urls import path
from . import views

urlpatterns = [
    # Kayıt Sayfası
    path('kayit/', views.kayit, name='kayit'),
    
    # Profil Sayfası (user/ ile değil, sadece /hesap/profil)
    path('profil/', views.profil, name='profil'),
    
    # Sipariş Listesi
    path('siparislerim/', views.siparis_listesi, name='siparis_listesi'),
    
    # Sipariş Detay Sayfası
    path('siparislerim/<int:siparis_id>/', views.siparis_detay, name='siparis_detay'),
]