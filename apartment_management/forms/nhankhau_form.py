from django import forms
from ..models import NhanKhau, TamTruTamVang
from django.utils import timezone

class NhanKhauForm(forms.ModelForm):
    class Meta:
        model = NhanKhau
        fields = [
            'ho_khau', 'ho_ten', 'ngay_sinh', 'gioi_tinh',
            'ma_can_cuoc', 'so_dien_thoai', 'thoi_gian_chuyen_den',
            'thoi_gian_chuyen_di', 'quan_he_voi_chu_ho', 'trang_thai'
        ]
        widgets = {
            'ngay_sinh': forms.DateInput(attrs={'type': 'date'}),
            'thoi_gian_chuyen_den': forms.DateInput(attrs={'type': 'date'}),
            'thoi_gian_chuyen_di': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        if not self.instance.pk:
            self.fields['trang_thai'].widget = forms.HiddenInput()
            self.fields['thoi_gian_chuyen_di'].widget = forms.HiddenInput()

            self.fields['trang_thai'].required = False
            self.fields['thoi_gian_chuyen_di'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)

        if not self.instance.pk:
            instance.trang_thai = 'Đang sinh sống'
            instance.thoi_gian_chuyen_di = None

        if commit:
            instance.save()

        return instance

class TamTruTamVangForm(forms.ModelForm):
    class Meta:
        model = TamTruTamVang
        fields = ['thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'ly_do']
        widgets = {
            'thoi_gian_bat_dau': forms.DateInput(attrs={'type': 'date'}),
            'thoi_gian_ket_thuc': forms.DateInput(attrs={'type': 'date'}),
            'ly_do': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
    
class TamTruForm(forms.ModelForm):
    class Meta:
        model = NhanKhau
        fields = [
            'ho_khau', 'ho_ten', 'ngay_sinh', 'gioi_tinh',
            'ma_can_cuoc', 'so_dien_thoai', 'quan_he_voi_chu_ho',
            'thoi_gian_chuyen_den'  # Thêm trường này vào
        ]
        widgets = {
            'ngay_sinh': forms.DateInput(attrs={'type': 'date'}),
            'thoi_gian_chuyen_den': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if not instance.thoi_gian_chuyen_den:
            instance.thoi_gian_chuyen_den = timezone.now()  # Gán giá trị mặc định nếu không có

        if commit:
            instance.save()

        return instance


