from .models import Sepet, SepetOgesi
from django.db.models import Sum # YENİ: Sum import edildi

def sepet_toplami(request):
    toplam_miktar = 0
    
    # 1. Kullanıcı Giriş yapmışsa
    if request.user.is_authenticated:
        try:
            # Kullanıcının sepetini bul
            sepet = Sepet.objects.get(user=request.user)
            # Sepetindeki tüm öğelerin (SepetOgesi) 'miktar' alanlarının toplamını al
            toplam_miktar = SepetOgesi.objects.filter(sepet=sepet).aggregate(Sum('miktar'))['miktar__sum']
        except Sepet.DoesNotExist:
            pass # Sepet yoksa miktar 0 kalır
            
    # 2. Kullanıcı Giriş yapmamışsa (Anonim)
    else:
        sepet_id = request.session.get('sepet_id')
        if sepet_id:
            try:
                # Anonim sepeti bul
                sepet = Sepet.objects.get(sepet_id=sepet_id)
                # Sepetindeki tüm öğelerin 'miktar' alanlarının toplamını al
                toplam_miktar = SepetOgesi.objects.filter(sepet=sepet).aggregate(Sum('miktar'))['miktar__sum']
            except Sepet.DoesNotExist:
                pass # Sepet yoksa miktar 0 kalır

    # Eğer toplam_miktar None ise (sepette hiç ürün yoksa), 0 yap
    if toplam_miktar is None:
        toplam_miktar = 0

    return {
        'sepet_toplami': toplam_miktar
    }