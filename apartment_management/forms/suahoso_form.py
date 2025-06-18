from django import forms
from ..models import NguoiDung

class SuaHoSoForm(forms.ModelForm):
    ho_ten = forms.CharField(max_length=100, required=True, label="Họ tên")
    email = forms.EmailField(max_length=100, required=True, label="Email")
    so_dien_thoai = forms.CharField(max_length=15, required=True, label="Số điện thoại")

    class Meta:
        model = NguoiDung
        fields = ['ho_ten', 'email', 'so_dien_thoai']
