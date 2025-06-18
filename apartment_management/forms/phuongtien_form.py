from django import forms
from ..models import PhuongTien

class PhuongTienForm(forms.ModelForm):
    class Meta:
        model = PhuongTien
        fields = ['loai_phuong_tien', 'bien_so', 'mau', 'mo_ta']
        widgets = {
            'loai_phuong_tien': forms.Select(attrs={'class': 'form-select'}),
            'bien_so': forms.TextInput(attrs={'class': 'form-control'}),
            'mau': forms.TextInput(attrs={'class': 'form-control'}),
            'mo_ta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
