# utils.py
from datetime import date
from .models import TamTruTamVang

def cap_nhat_trang_thai_tamtru_tamvang():
    today = date.today()
    ds_het_han = TamTruTamVang.objects.filter(thoi_gian_ket_thuc__lt=today)

    for record in ds_het_han:
        nhankhau = record.nhan_khau
        if record.loai == 'Tạm trú':
            nhankhau.delete()
        elif record.loai == 'Tạm vắng':
            nhankhau.trang_thai = 'Đang sinh sống'
            nhankhau.save()
        record.delete()
