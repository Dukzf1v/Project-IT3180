from django import forms
from ..models import Phi, CapNhatPhiSinhHoat

class PhiForm(forms.ModelForm):
    class Meta:
        model = Phi
        fields = ['ho_khau', 'loai_phi', 'gia_phi_dich_vu', 'gia_phi_quan_ly', 'gia_phi_gui_xe_may', 'gia_phi_gui_o_to', 'nam']
        widgets = {
            'ho_khau': forms.Select(attrs={'class': 'form-control'}),
            'loai_phi': forms.Select(attrs={'class': 'form-control'}),
            'gia_phi_dich_vu': forms.NumberInput(attrs={'class': 'form-control'}),
            'gia_phi_quan_ly': forms.NumberInput(attrs={'class': 'form-control'}),
            'gia_phi_gui_xe_may': forms.NumberInput(attrs={'class': 'form-control'}),
            'gia_phi_gui_o_to': forms.NumberInput(attrs={'class': 'form-control'}),
            'nam': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        gia_phi_dich_vu = cleaned_data.get('gia_phi_dich_vu')
        gia_phi_quan_ly = cleaned_data.get('gia_phi_quan_ly')
        gia_phi_gui_xe_may = cleaned_data.get('gia_phi_gui_xe_may')
        gia_phi_gui_o_to = cleaned_data.get('gia_phi_gui_o_to')

        if not gia_phi_dich_vu and not gia_phi_quan_ly and not gia_phi_gui_xe_may and not gia_phi_gui_o_to:
            raise forms.ValidationError("Please fill in at least one fee field.")
        return cleaned_data

class CapNhatPhiSinhHoatForm(forms.ModelForm):
    class Meta:
        model = CapNhatPhiSinhHoat
        fields = ['ho_khau', 'tien_dien', 'tien_nuoc', 'tien_internet', 'thang', 'nam']
        widgets = {
            'ho_khau': forms.Select(attrs={'class': 'form-control'}),
            'tien_dien': forms.NumberInput(attrs={'class': 'form-control'}),
            'tien_nuoc': forms.NumberInput(attrs={'class': 'form-control'}),
            'tien_internet': forms.NumberInput(attrs={'class': 'form-control'}),
            'thang': forms.NumberInput(attrs={'class': 'form-control'}),
            'nam': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tien_dien = cleaned_data.get('tien_dien')
        tien_nuoc = cleaned_data.get('tien_nuoc')
        tien_internet = cleaned_data.get('tien_internet')

        if not tien_dien or not tien_nuoc or not tien_internet:
            raise forms.ValidationError("Please fill in all utility fee fields.")
        return cleaned_data

class CapNhatPhiForm(forms.ModelForm):
    class Meta:
        model = Phi
        fields = ['gia_phi_dich_vu', 'gia_phi_quan_ly', 'gia_phi_gui_xe_may', 'gia_phi_gui_o_to']
        widgets = {
            'gia_phi_dich_vu': forms.NumberInput(attrs={'min': 0}),
            'gia_phi_quan_ly': forms.NumberInput(attrs={'min': 0}),
            'gia_phi_gui_xe_may': forms.NumberInput(attrs={'min': 0}),
            'gia_phi_gui_o_to': forms.NumberInput(attrs={'min': 0}),
        }
        
class UploadPhiSinhHoatForm(forms.Form):
    excel_file = forms.FileField(label='Tải lên file Excel', required=True)
    thang = forms.IntegerField(label='Chọn tháng', min_value=1, max_value=12, required=True)
