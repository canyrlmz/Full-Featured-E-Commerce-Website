from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction

# KENDİ FORMLARINIZI İÇE AKTARIN
from .forms import KullaniciKayitFormu, UserUpdateForm, ProfileUpdateForm 
from .models import Profil # Profil modelini içeri aktarıyoruz

# Katalog modelinden Siparis modelini çekiyoruz
from katalog.models import Siparis, SiparisOgesi 

# =======================================================
# 1. KAYIT VIEW (DEĞİŞİKLİK YOK)
# =======================================================
def kayit(request):
    if request.user.is_authenticated:
        return redirect('ayakkabi_listesi')
        
    if request.method == 'POST':
        form = KullaniciKayitFormu(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Kayıt başarılı olduğunda Profil objesi de oluşturulur
            # User modelindeki 'post_save' sinyalini kullanırsanız bu kod gereksiz olabilir.
            Profil.objects.create(user=user)
            
            messages.success(request, f"Hoş geldin, {user.username}! Hesabın başarıyla oluşturuldu.")
            return redirect('ayakkabi_listesi') 
        else:
            messages.error(request, "Kayıt sırasında hatalar oluştu. Lütfen formu kontrol edin.")
    else:
        form = KullaniciKayitFormu()
        
    return render(request, 'registration/kayit.html', {'form': form})

# =======================================================
# 2. PROFİL VIEW (GÜNCELLENDİ)
# =======================================================
@login_required 
@transaction.atomic
def profil(request):
    user = request.user
    
    # Kullanıcının bir Profil objesi yoksa oluşturur.
    # Bu, sayfa ilk kez yüklendiğinde oluşabilecek hataları engeller.
    try:
        profil_objesi = user.profil
    except Profil.DoesNotExist:
        profil_objesi = Profil.objects.create(user=user)
    
    if request.method == 'POST':
        # Temel kullanıcı bilgileri formunu doldur
        u_form = UserUpdateForm(request.POST, instance=user)
        # Ek profil bilgileri formunu doldur
        p_form = ProfileUpdateForm(request.POST, instance=profil_objesi) 
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save() 
            
            messages.success(request, 'Profil bilgileriniz başarıyla güncellendi!')
            return redirect('profil')
        else:
            messages.error(request, "Güncelleme sırasında hatalar oluştu. Lütfen formu kontrol edin.")
    
    else:
        # Sayfa ilk yüklendiğinde mevcut bilgileri formlara getir
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profil_objesi)

    context = {
        'u_form': u_form, # Kullanıcı bilgilerini güncelleme formu
        'p_form': p_form, # Ek profil bilgilerini güncelleme formu
        'sayfa_basligi': f"{request.user.username} Profil Sayfası",
    }
    return render(request, 'kullanici/profil.html', context)

# =======================================================
# 3. SİPARİŞLERİM (LİSTE) VIEW (DEĞİŞİKLİK YOK)
# =======================================================
@login_required 
def siparis_listesi(request):
    siparisler = Siparis.objects.filter(user=request.user).order_by('-olusturma_tarihi')
    
    context = {
        'siparisler': siparisler,
        'sayfa_basligi': 'Sipariş Geçmişim',
    }
    return render(request, 'kullanici/siparis_listesi.html', context)

# =======================================================
# 4. SİPARİŞ DETAY VIEW (DEĞİŞİKLİK YOK)
# =======================================================
@login_required 
def siparis_detay(request, siparis_id):
    siparis = get_object_or_404(Siparis, id=siparis_id)
    
    if siparis.user != request.user:
        messages.error(request, "Bu siparişi görüntüleme yetkiniz bulunmamaktadır.")
        return redirect('siparis_listesi')
        
    siparis_ogeleri = SiparisOgesi.objects.filter(siparis=siparis)
    
    context = {
        'siparis': siparis,
        'siparis_ogeleri': siparis_ogeleri,
        'sayfa_basligi': f"Sipariş #{siparis.id} Detayı",
    }
    return render(request, 'kullanici/siparis_detay.html', context)