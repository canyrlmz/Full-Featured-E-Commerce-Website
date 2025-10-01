from django.urls import path
from . import views

urlpatterns = [
    # 1. Ana Sayfa (Liste)
    path('', views.ayakkabi_listesi, name='ayakkabi_listesi'),
    
    # SEPET İŞLEMLERİ
    path('sepet/', views.sepeti_goruntule, name='sepeti_goruntule'),
    path('sepete_ekle/<int:varyant_id>/', views.sepete_ekle, name='sepete_ekle'),
    path('sepet/artir/<int:sepet_ogesi_id>/', views.miktar_artir, name='miktar_artir'),
    path('sepet/azalt/<int:sepet_ogesi_id>/', views.miktar_azalt, name='miktar_azalt'),
    path('sepet/sil/<int:sepet_ogesi_id>/', views.sepetten_cikar, name='sepetten_cikar'),
    
    # ÖDEME İŞLEMLERİ
    path('checkout/', views.siparis_olustur, name='siparis_olustur'),
    path('siparis/onay/<int:siparis_id>/', views.siparis_onay, name='siparis_onay'),
    
    # Burası önemli: 'ayakkabi_detay' adı bu satırda tanımlanmalı.
    path('urun/<slug:slug>/', views.ayakkabi_detay, name='ayakkabi_detay'),
]