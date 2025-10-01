from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User # YENİ: Kullanıcı modelini import et

# Marka Modeli
class Marka(models.Model):
    isim = models.CharField(max_length=100)
    
    def __str__(self):
        return self.isim
    
# Ayakkabı Modeli
class Ayakkabi(models.Model):
    marka = models.ForeignKey(Marka, on_delete=models.CASCADE)
    model_adi = models.CharField(max_length=150)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    aciklama = models.TextField(blank=True)
    slug = models.SlugField(unique=True, max_length=150)
    
    resim = models.ImageField(upload_to='ayakkabi_resimleri/', 
                              blank=True, 
                              null=True,
                              verbose_name="Ürün Resmi")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.marka.isim}-{self.model_adi}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.marka.isim} {self.model_adi}"

# Ayakkabi Varyant Modeli (Renk/Beden/Stok)
class AyakkabiVaryant(models.Model):
    ayakkabi = models.ForeignKey(Ayakkabi, on_delete=models.CASCADE)
    renk = models.CharField(max_length=50)
    beden = models.CharField(max_length=10) 
    stok = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.ayakkabi.model_adi} - {self.renk} ({self.beden})"

# Sepet Modelleri
class Sepet(models.Model):
    # GÜNCELLEME: user alanı eklendi
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    sepet_id = models.CharField(max_length=250, blank=True, null=True) # null=True ekledim ki user varsa sepet_id boş kalabilsin
    eklenme_tarihi = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.sepet_id if self.sepet_id else f"User Sepeti ({self.user.username})"
        
class SepetOgesi(models.Model):
    varyant = models.ForeignKey(AyakkabiVaryant, on_delete=models.CASCADE)
    sepet = models.ForeignKey(Sepet, on_delete=models.CASCADE)
    miktar = models.IntegerField(default=1)
    
    def toplam_fiyat(self):
        return self.varyant.ayakkabi.fiyat * self.miktar
        
    def __str__(self):
        return str(self.varyant)

# Sipariş Modelleri
class Siparis(models.Model):
    DURUM_SECENEKLERI = [
        ('Hazırlanıyor', 'Hazırlanıyor'),
        ('Kargoda', 'Kargoda'),
        ('Teslim Edildi', 'Teslim Edildi'),
        ('İptal Edildi', 'İptal Edildi'),
    ]
    
    # GÜNCELLEME: user alanı eklendi
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    sepet_id = models.CharField(max_length=250, blank=True, verbose_name="Anonim Sepet ID")
    ad_soyad = models.CharField(max_length=100)
    email = models.EmailField()
    adres = models.TextField()
    toplam_fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    durum = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default='Hazırlanıyor')
    
    def __str__(self):
        return f"Sipariş {self.id} - {self.ad_soyad}"
        
class SiparisOgesi(models.Model):
    siparis = models.ForeignKey(Siparis, on_delete=models.CASCADE)
    varyant = models.ForeignKey(AyakkabiVaryant, on_delete=models.CASCADE)
    miktar = models.IntegerField()
    fiyat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Satış Fiyatı")
    
    def alt_toplam(self):
        if self.fiyat is not None and self.miktar is not None:
            return self.fiyat * self.miktar
        return 0.00
    alt_toplam.short_description = 'Alt Toplam'
        
    def __str__(self):
        return f"{self.varyant.ayakkabi.model_adi} x {self.miktar}"