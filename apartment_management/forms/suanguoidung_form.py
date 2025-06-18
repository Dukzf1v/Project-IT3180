from django import forms
from ..models import NguoiDung

class SuaNguoiDungForm(forms.ModelForm):
    class Meta:
        model = NguoiDung
        fields = ['ho_ten', 'email', 'so_dien_thoai', 'vai_tro']  # Chỉnh sửa các trường này

    def __init__(self, *args, **kwargs):
        super(SuaNguoiDungForm, self).__init__(*args, **kwargs)
        self.fields['ho_ten'].widget.attrs['placeholder'] = 'Họ và tên'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['so_dien_thoai'].widget.attrs['placeholder'] = 'Số điện thoại'
        self.fields['vai_tro'].widget.attrs['placeholder'] = 'Vai trò'
