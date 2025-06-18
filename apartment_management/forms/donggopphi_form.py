from django import forms
from ..models import DanhSachPhiDongGop, DongGopPhi

class DanhSachPhiDongGopForm(forms.ModelForm):
    class Meta:
        model = DanhSachPhiDongGop
        fields = ['ten_phi', 'so_tien_goi_y', 'noi_dung', 'ngay_bat_dau', 'ngay_ket_thuc']
        widgets = {
            'ngay_bat_dau': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'ngay_ket_thuc': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

class DongGopPhiForm(forms.ModelForm):
    class Meta:
        model = DongGopPhi
        fields = ['ho_khau', 'ngay_dong', 'so_tien_dong', 'ghi_chu']
        widgets = {
            'ngay_dong': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }   