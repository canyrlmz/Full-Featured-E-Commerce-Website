from django import forms

# Ödeme simülasyonu için kart tipi ve ay listeleri
AY_SECENEKLERI = [(i, str(i).zfill(2)) for i in range(1, 13)]
YIL_SECENEKLERI = [(i, i) for i in range(2025, 2035)]
KART_SECENEKLERI = [
    ('Visa', 'Visa'),
    ('Mastercard', 'Mastercard'),
    ('Amex', 'American Express'),
]

class CheckoutForm(forms.Form):
    # 1. Teslimat Bilgileri Alanları
    ad_soyad = forms.CharField(
        label='Adınız Soyadınız',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tam Adınız'})
    )
    email = forms.EmailField(
        label='E-posta Adresi',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'mail@ornek.com'})
    )
    adres = forms.CharField(
        label='Teslimat Adresi (Mahalle, Cadde, No, İl/İlçe)',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Açık adresinizi yazınız.'})
    )
    
    # 2. Ödeme Simülasyonu Alanları
    kart_tipi = forms.ChoiceField(
        label='Kart Tipi',
        choices=KART_SECENEKLERI,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    kart_numarasi = forms.CharField(
        label='Kart Numarası',
        min_length=16,
        max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXXX XXXX XXXX XXXX', 'pattern': '[0-9]{16}'})
    )
    kart_son_ay = forms.ChoiceField(
        label='Son Ay',
        choices=AY_SECENEKLERI,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    kart_son_yil = forms.ChoiceField(
        label='Son Yıl',
        choices=YIL_SECENEKLERI,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    kart_cvv = forms.CharField(
        label='CVV',
        min_length=3,
        max_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX', 'pattern': '[0-9]{3}'})
    )

    # Django Forms'un otomatik olarak yapmadığı zorunlu alan kontrolünü sağlamak için
    # tüm alanlar varsayılan olarak zaten zorunludur (required=True).