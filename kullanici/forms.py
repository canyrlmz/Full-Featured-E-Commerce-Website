from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Özel Profil Modelini İçe Aktar (Bu satırın çalışması için models.py dosyanızda Profil modeli olmalıdır)
from .models import Profil 

# =======================================================
# 1. Kullanıcı Kayıt Formu (Mevcut Formunuz)
# =======================================================
class KullaniciKayitFormu(UserCreationForm):
    class Meta:
        model = User
        # Kayıt sırasında kullanıcı adı ve e-posta alıyoruz
        fields = ('username', 'email')

    # Bootstrap form-control class'ını otomatik ekle
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
# =======================================================
# 2. Kullanıcı Bilgilerini Güncelleme Formu (UserUpdateForm)
# =======================================================
class UserUpdateForm(forms.ModelForm):
    # Alanları açıkça tanımlayarak class ve label ekleme
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=False, label="Ad", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, label="Soyad", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
# =======================================================
# 3. Ek Profil Bilgilerini Güncelleme Formu (ProfileUpdateForm) <--- GÜNCELLENDİ
# =======================================================

class ProfileUpdateForm(forms.ModelForm):
    # Form alanlarını burada tanımlayın ve Bootstrap class'ını ekleyin
    adres = forms.CharField(
        label="Adres",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    telefon = forms.CharField(
        label="Telefon Numarası", 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: 5xx xxx xx xx'})
    )

    class Meta:
        # Ek Profil Modelini kullanıyoruz
        model = Profil 
        # Modeldeki karşılık gelen alanları belirtin
        fields = ['adres', 'telefon']