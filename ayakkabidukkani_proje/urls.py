from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hesap/', include('kullanici.urls')),

    # =========================================================================
    # DJANGO AUTHENTICATION URL'leri
    # =========================================================================
    
    # GİRİŞ / ÇIKIŞ
    path('hesap/giris/', 
        auth_views.LoginView.as_view(template_name='registration/login.html'), 
        name='login'
    ),
    path('hesap/cikis/', 
        auth_views.LogoutView.as_view(next_page='/'), 
        name='logout'
    ),

    # ŞİFRE DEĞİŞTİRME (Yeni eklenen/kontrol edilen kısım)
    path('hesap/sifre-degistir/', 
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change_form.html'
        ), 
        name='password_change' # <-- PROFİL SAYFASINDA ARANAN İSİM
    ),
    path('hesap/sifre-degistir/tamamlandi/', 
        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'
        ), 
        name='password_change_done'
    ),

    # ŞİFRE SIFIRLAMA
    path('hesap/sifre-sifirla/', 
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), 
        name='password_reset'
    ),
    path('hesap/sifre-sifirla/gonderildi/', 
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
        name='password_reset_done'
    ),
    path('hesap/sifirla/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
        name='password_reset_confirm'
    ),
    path('hesap/sifirla/tamamlandi/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
        name='password_reset_complete'
    ),
    
    # =========================================================================
    
    # KATALOG
    path('', include('katalog.urls')),
]