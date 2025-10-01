from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction 
from django.core.exceptions import ObjectDoesNotExist 
from django.contrib import messages 
from django.contrib.auth.decorators import login_required 
from .forms import CheckoutForm 
from .models import Ayakkabi, AyakkabiVaryant, Sepet, SepetOgesi, Siparis, SiparisOgesi

# =======================================================
# HELPER FONKSİYONLAR (KULLANICI/SEPET GÜNCELLEMESİ)
# =======================================================

def _get_sepet_id(request):
    """Anonim sepetler için session ID'sini alır/oluşturur."""
    if not request.session.session_key:
        request.session.create()
    return request.session.get('sepet_id', request.session.session_key)

def _get_sepet(request):
    """Kullanıcının sepetini döndürür, yoksa oluşturur ve anonim sepeti birleştirir."""
    
    # 1. Giriş yapmış kullanıcı için sepeti bulmaya çalış
    if request.user.is_authenticated:
        try:
            sepet = Sepet.objects.get(user=request.user)
            return sepet
        except Sepet.DoesNotExist:
            pass # Yoksa anonim sepet kontrolüne geç

    # 2. Anonim (Session ID) sepeti bulmaya çalış
    sepet_id = _get_sepet_id(request)
    try:
        anonim_sepet = Sepet.objects.get(sepet_id=sepet_id)
    except Sepet.DoesNotExist:
        anonim_sepet = None

    # 3. Anonim Sepet Varsa ve Kullanıcı Giriş Yaptıysa (Birleştirme/Migrasyon)
    if anonim_sepet and request.user.is_authenticated:
        
        # Anonim sepeti, kullanıcının yeni sepeti olarak ata (Migrasyon)
        anonim_sepet.user = request.user 
        anonim_sepet.sepet_id = None # Artık session ID'si gerekmez
        anonim_sepet.save()
        
        # Session'daki anonim sepet ID'sini temizle
        if 'sepet_id' in request.session:
            del request.session['sepet_id']
            
        messages.info(request, "Anonim sepetiniz hesabınıza aktarıldı.")
        return anonim_sepet

    # 4. Yeni Sepet Oluşturma (Anonim veya Kullanıcılı)
    if request.user.is_authenticated:
        # Kullanıcı varsa, ona ait bir sepet oluştur
        sepet = Sepet.objects.create(user=request.user)
    else:
        # Kullanıcı yoksa, anonim sepet oluştur
        sepet = Sepet.objects.create(sepet_id=sepet_id)
        
    return sepet
    
def _get_aktif_sepet(request):
    """Helper: Mevcut aktif sepeti döndürür veya None."""
    if request.user.is_authenticated:
        try:
            return Sepet.objects.get(user=request.user)
        except Sepet.DoesNotExist:
            return None
    else:
        sepet_id = _get_sepet_id(request)
        try:
            return Sepet.objects.get(sepet_id=sepet_id)
        except Sepet.DoesNotExist:
            return None

# =======================================================
# KATALOG VIEW FONKSİYONLARI 
# =======================================================

def ayakkabi_listesi(request):
    tum_ayakkabilar = Ayakkabi.objects.all()
    context = {
        'ayakkabilar': tum_ayakkabilar,
        'sayfa_basligi': 'Ayakkabı Dükkanı | Tüm Modeller'
    }
    return render(request, 'katalog/ayakkabi_listesi.html', context)

def ayakkabi_detay(request, slug):
    ayakkabi = get_object_or_404(Ayakkabi, slug=slug)
    varyantlar = AyakkabiVaryant.objects.filter(ayakkabi=ayakkabi, stok__gt=0) 
    
    context = {
        'ayakkabi': ayakkabi,
        'varyantlar': varyantlar,
        'sayfa_basligi': ayakkabi.model_adi 
    }
    return render(request, 'katalog/ayakkabi_detay.html', context)


# =======================================================
# SEPET VIEW FONKSİYONLARI 
# =======================================================

# 3. Ürünü Sepete Ekleme View'i
def sepete_ekle(request, varyant_id):
    varyant = get_object_or_404(AyakkabiVaryant, id=varyant_id)
    
    # Yeni helper fonksiyonu kullanıldı
    sepet = _get_sepet(request)

    try:
        sepet_ogesi = SepetOgesi.objects.get(varyant=varyant, sepet=sepet)
        
        # Stok kontrolü yaparak miktarı artır
        if sepet_ogesi.miktar < varyant.stok:
            sepet_ogesi.miktar += 1
            sepet_ogesi.save()
            messages.success(request, f"'{varyant}' sepete eklendi.")
        else:
            messages.warning(request, f"'{varyant}' için yeterli stok kalmadı.")
            
    except SepetOgesi.DoesNotExist:
        # Sepette yoksa, stokta 1'den fazla ürün varsa ekle
        if varyant.stok > 0:
            sepet_ogesi = SepetOgesi.objects.create(
                varyant=varyant,
                miktar=1,
                sepet=sepet
            )
            messages.success(request, f"'{varyant}' sepete eklendi.")
        else:
             messages.error(request, f"'{varyant}' şu anda stokta yok.")
            
    return redirect('ayakkabi_detay', slug=varyant.ayakkabi.slug)

# 4. Sepet Görüntüleme View'i
def sepeti_goruntule(request):
    sepet = _get_aktif_sepet(request)
    sepet_ogeleri = []
    toplam_fiyat = 0
    
    if sepet:
        sepet_ogeleri = SepetOgesi.objects.filter(sepet=sepet)
        for oge in sepet_ogeleri:
            toplam_fiyat += oge.toplam_fiyat()
        
    context = {
        'sepet_ogeleri': sepet_ogeleri,
        'toplam_fiyat': toplam_fiyat
    }
    
    return render(request, 'katalog/sepet.html', context)

# 5, 6, 7. Sepet İşlemleri (Miktar Artır/Azalt/Çıkar)

def miktar_azalt(request, sepet_ogesi_id):
    sepet_ogesi = get_object_or_404(SepetOgesi, id=sepet_ogesi_id)
    # GÜVENLİK KONTROLÜ (Bu sepet öğesi, request.user/session'a ait mi?)
    if _get_aktif_sepet(request) != sepet_ogesi.sepet:
        messages.error(request, "Yetkisiz işlem girişimi.")
        return redirect('sepeti_goruntule')
    
    if sepet_ogesi.miktar > 1:
        sepet_ogesi.miktar -= 1
        sepet_ogesi.save()
        messages.info(request, f"'{sepet_ogesi.varyant}' miktarı 1 azaltıldı.")
    else:
        sepet_ogesi.delete() 
        messages.warning(request, f"'{sepet_ogesi.varyant}' sepetten çıkarıldı.")
        
    return redirect('sepeti_goruntule')

def miktar_artir(request, sepet_ogesi_id):
    sepet_ogesi = get_object_or_404(SepetOgesi, id=sepet_ogesi_id)
    if _get_aktif_sepet(request) != sepet_ogesi.sepet:
        messages.error(request, "Yetkisiz işlem girişimi.")
        return redirect('sepeti_goruntule')
        
    if sepet_ogesi.miktar < sepet_ogesi.varyant.stok:
        sepet_ogesi.miktar += 1
        sepet_ogesi.save()
        messages.info(request, f"'{sepet_ogesi.varyant}' miktarı 1 artırıldı.")
    else:
        messages.error(request, f"'{sepet_ogesi.varyant}' için yeterli stok kalmadı.")
        
    return redirect('sepeti_goruntule')

def sepetten_cikar(request, sepet_ogesi_id):
    sepet_ogesi = get_object_or_404(SepetOgesi, id=sepet_ogesi_id)
    if _get_aktif_sepet(request) != sepet_ogesi.sepet:
        messages.error(request, "Yetkisiz işlem girişimi.")
        return redirect('sepeti_goruntule')
        
    varyant_adi = str(sepet_ogesi.varyant)
    sepet_ogesi.delete()
    
    messages.warning(request, f"'{varyant_adi}' sepetten tamamen çıkarıldı.")
    
    return redirect('sepeti_goruntule')


# =======================================================
# SİPARİŞ/ÖDEME VIEW FONKSİYONLARI 
# =======================================================

# 8. Sipariş Oluşturma (Checkout) View'i
@transaction.atomic # Fonksiyonun tamamını tek bir veritabanı işlemi olarak işaretler
def siparis_olustur(request):
    
    # Aktif Sepeti al
    sepet = _get_aktif_sepet(request) 
    
    # Sepet boşsa kontrol et
    if not sepet or not SepetOgesi.objects.filter(sepet=sepet).exists():
        messages.warning(request, "Sepetiniz boş olduğu için ödeme sayfasına geçilemiyor.")
        return redirect('sepeti_goruntule')
        
    sepet_ogeleri = SepetOgesi.objects.filter(sepet=sepet)
    toplam_fiyat = sum(oge.toplam_fiyat() for oge in sepet_ogeleri)
    form = CheckoutForm()
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST) 
        
        if form.is_valid():
            data = form.cleaned_data 
            
            # Ödeme Simülasyonu Kontrolü
            if data['kart_cvv'] not in ['123', '456']:
                form.add_error('kart_cvv', 'Ödeme başarısız oldu. Lütfen test için 123 veya 456 CVV kullanın.')
            else:
                # Ödeme BAŞARILI ise
                
                # Stok Kontrolü (Son bir kez)
                stok_yetersiz = False
                for sepet_oge in sepet_ogeleri:
                    if sepet_oge.miktar > sepet_oge.varyant.stok:
                        stok_yetersiz = True
                        messages.error(request, f"Stok hatası: **{sepet_oge.varyant}** için yeterli stok yok.")
                        break
                
                if stok_yetersiz:
                    pass 
                else:
                    # 1. Yeni Sipariş Oluştur
                    siparis = Siparis.objects.create(
                        # KULLANICI BAĞLANTISI
                        user=request.user if request.user.is_authenticated else None, 
                        sepet_id=sepet, # DÜZELTİLDİ: Artık Siparis modelindeki ForeignKey alanına doğru objeyi atıyoruz.
                        ad_soyad=data['ad_soyad'],
                        email=data['email'],
                        adres=data['adres'],
                        toplam_fiyat=toplam_fiyat,
                        durum='Hazırlanıyor'
                    )
                    
                    # 2. Sepet Öğelerini Sipariş Öğelerine Kopyala ve Stoktan Düş
                    for sepet_oge in sepet_ogeleri:
                        SiparisOgesi.objects.create(
                            siparis=siparis,
                            varyant=sepet_oge.varyant,
                            miktar=sepet_oge.miktar,
                            fiyat=sepet_oge.varyant.ayakkabi.fiyat 
                        )
                        
                        sepet_oge.varyant.stok -= sepet_oge.miktar
                        sepet_oge.varyant.save()
                        
                    # 3. Sepeti Temizle (Sepet objesini sil)
                    sepet.delete()
                    
                    # Eğer anonim sepet kullanıldıysa session ID'sini de temizle
                    if not request.user.is_authenticated and 'sepet_id' in request.session:
                        del request.session['sepet_id']

                    messages.success(request, "Siparişiniz başarıyla alındı! Teşekkür ederiz.")
                    # 4. Onay sayfasına yönlendir
                    return redirect('siparis_onay', siparis_id=siparis.id)

    # GET isteği (veya POST'ta hata oluşursa) burası çalışır
    context = {
        'sepet_ogeleri': sepet_ogeleri,
        'toplam_fiyat': toplam_fiyat,
        'form': form, 
    }
    return render(request, 'katalog/checkout.html', context)


# 9. Sipariş Onay View'i 
def siparis_onay(request, siparis_id):
    siparis = get_object_or_404(Siparis, id=siparis_id)
    # GÜVENLİK KONTROLÜ: Kullanıcı giriş yapmışsa, siparişin ona ait olduğunu kontrol et.
    if request.user.is_authenticated and siparis.user != request.user:
        messages.error(request, "Bu siparişi görüntüleme yetkiniz yok.")
        return redirect('ayakkabi_listesi') 
        
    siparis_ogeleri = SiparisOgesi.objects.filter(siparis=siparis)
    
    context = {
        'siparis': siparis,
        'siparis_ogeleri': siparis_ogeleri
    }
    return render(request, 'katalog/siparis_onay.html', context)