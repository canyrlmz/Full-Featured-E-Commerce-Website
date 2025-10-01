from django.db import models
from django.contrib.auth.models import User # Django'nun hazır User modelini dahil ediyoruz

class Profil(models.Model):
    # Kullanıcıya tekil (OneToOne) bağlantı
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Eklemek istediğimiz alanlar
    adres = models.CharField(max_length=255, verbose_name="Adres", blank=True, null=True)
    telefon = models.CharField(max_length=20, verbose_name="Telefon Numarası", blank=True, null=True)
    
    # Diğer ek alanları buraya ekleyebilirsiniz (Örn: dogum_tarihi, cinsiyet vb.)

    def __str__(self):
        # Yönetici panelinde kolay tanıma için
        return f'{self.user.username} - Profil'
