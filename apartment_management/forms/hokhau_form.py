from django import forms
from apartment_management.models import HoKhau

class HoKhauForm(forms.ModelForm):
    class Meta:
        model = HoKhau
        fields = [
            'so_can_ho', 'tang', 'toa_nha', 'ngay_lap', 'dien_tich',
            'so_xe_may', 'so_o_to', 'trang_thai', 'ngay_chuyen_di'
        ]
        widgets = {
            'ngay_lap': forms.DateInput(attrs={'type': 'date'}),
            'ngay_chuyen_di': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if not self.instance.pk: 
            self.fields['trang_thai'].required = False 
            self.fields['ngay_chuyen_di'].required = False  
            self.fields['trang_thai'].widget = forms.HiddenInput()  
            self.fields['ngay_chuyen_di'].widget = forms.HiddenInput()  
        else: 
            self.fields['trang_thai'].required = False
            self.fields['ngay_chuyen_di'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if not self.instance.pk: 
            instance.trang_thai = 'Đang ở'
            instance.so_xe_may = 0
            instance.so_o_to = 0

        if commit:
            instance.save()

        return instance

