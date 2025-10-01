from django.contrib import admin
from django.db.models import Sum # <-- HATA DÜZELTİLDİ: Sum fonksiyonu doğru yerden alındı
from .models import Marka, Ayakkabi, AyakkabiVaryant, Siparis, SiparisOgesi

# ========================================================
# 1. AYAKKABI VARYANTLARI (Inline Yönetim)
# ========================================================

# Ayakkabının detay sayfasında varyantları düzenlemeyi sağlar
class AyakkabiVaryantInline(admin.TabularInline):
    model = AyakkabiVaryant
    extra = 1 # Varsayılan olarak 1 tane boş varyant göster
    fields = ['renk', 'beden', 'stok'] # Gösterilecek alanlar

# ========================================================
# 2. AYAKKABI ADMIN
# ========================================================

@admin.register(Ayakkabi)
class AyakkabiAdmin(admin.ModelAdmin):
    # Liste görünümü için
    list_display = ('model_adi', 'marka', 'fiyat', 'stok_durumu', 'slug')
    list_filter = ('marka', 'fiyat')
    search_fields = ('model_adi', 'aciklama')
    prepopulated_fields = {'slug': ('marka', 'model_adi')} # Slug'ı otomatik doldur

    # Detay sayfasında AyakkabiVaryant'ları inline olarak göster
    inlines = [AyakkabiVaryantInline]

    # Modeldeki toplam stok sayısını göstermek için bir metod ekleyelim
    def stok_durumu(self, obj):
        # Ayakkabıya bağlı tüm varyantların stoklarını topla
        toplam_stok = AyakkabiVaryant.objects.filter(ayakkabi=obj).aggregate(
            toplam=Sum('stok') # <-- DÜZELTME YAPILDI: Sum() doğrudan kullanılıyor
        )['toplam']
        return toplam_stok if toplam_stok is not None else 0
    stok_durumu.short_description = 'Toplam Stok' # Admin panelinde görünen başlık

# ========================================================
# 3. SİPARİŞLERİN YÖNETİMİ
# ========================================================

# Siparişin detay sayfasında hangi ürünlerin sipariş edildiğini gösterir
class SiparisOgesiInline(admin.TabularInline):
    model = SiparisOgesi
    extra = 0 
    # fields listesini alt_toplam metoduyla güncelliyoruz
    fields = ('varyant', 'miktar', 'fiyat', 'alt_toplam') 
    readonly_fields = ('varyant', 'miktar', 'fiyat', 'alt_toplam') # Hepsini readonly yapıyoruz.
    can_delete = False 


@admin.register(Siparis)
class SiparisAdmin(admin.ModelAdmin):
    # Liste görünümü
    list_display = ('id', 'ad_soyad', 'olusturma_tarihi', 'toplam_fiyat', 'durum')
    list_filter = ('durum', 'olusturma_tarihi')
    search_fields = ('ad_soyad', 'email', 'adres')
    date_hierarchy = 'olusturma_tarihi' # Tarihe göre filtreleme

    # Detay sayfasındaki alanların sırası ve gruplandırılması
    fieldsets = (
        ('Müşteri Bilgileri', {
            'fields': ('ad_soyad', 'email', 'adres')
        }),
        ('Sipariş Durumu ve Fiyat', {
            'fields': ('durum', 'toplam_fiyat', 'olusturma_tarihi')
        }),
    )
    
    # Sipariş öğelerini siparişin hemen altında göster
    inlines = [SiparisOgesiInline]
    
    # Okuma izni verilen alanlar (değiştirilemez)
    readonly_fields = ('olusturma_tarihi', 'toplam_fiyat')


# ========================================================
# 4. BASİT KAYITLAR
# ========================================================

# Marka'yı admin panelinde basitçe göster
admin.site.register(Marka)

# NOT: AyakkabiVaryant, AyakkabiAdmin içinde inline olarak yönetildiği için buraya kaydetmeye gerek yoktur.
# Marka, Ayakkabi ve Siparis zaten @admin.register ile kaydedilmiştir.