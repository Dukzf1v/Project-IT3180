from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class NguoiDung(models.Model):
    VAI_TRO_CHOICES = [
        ('Quản lý', 'Quản lý'),
        ('Kế toán', 'Kế toán'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    ho_ten = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    so_dien_thoai = models.CharField(max_length=15)
    vai_tro = models.CharField(max_length=30, choices=VAI_TRO_CHOICES)

    def __str__(self):
        return f"{self.ho_ten} - {self.vai_tro}"

class HoKhau(models.Model):
    TRANG_THAI_CHOICES = [
        ('Đang ở', 'Đang ở'),
        ('Đã rời đi', 'Đã rời đi'),
    ]
    so_can_ho = models.CharField(max_length=10)
    tang = models.IntegerField()
    toa_nha = models.CharField(max_length=30)
    ngay_lap = models.DateField(null=True, blank=True)
    ngay_chuyen_di = models.DateField(null=True, blank=True)
    dien_tich = models.FloatField(null=True, blank=True)
    so_xe_may = models.IntegerField(null=True, blank=True)
    so_o_to = models.IntegerField(null=True, blank=True)
    chu_ho = models.ForeignKey('NhanKhau', on_delete=models.SET_NULL, null=True, blank=True, related_name='chu_ho_cua_ho_khau')
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES)

    def save(self, *args, **kwargs):
        """Override phương thức save để cập nhật hoặc tạo mới các bản ghi Phi khi HoKhau được lưu."""
        super().save(*args, **kwargs)

        loai_phi_choices = ['Dịch vụ', 'Gửi xe', 'Quản lý', 'Sinh hoạt']
        
        for loai_phi in loai_phi_choices:
            phi, created = Phi.objects.get_or_create(ho_khau=self, loai_phi=loai_phi, nam=timezone.now().year)
            phi.cap_nhat_phi()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Căn hộ {self.so_can_ho} - Tầng {self.tang} - {self.toa_nha}"


class NhanKhau(models.Model):
    GIOI_TINH_CHOICES = [('Nam', 'Nam'), ('Nữ', 'Nữ')]
    TRANG_THAI_CHOICES = [
        ('Đang sinh sống', 'Đang sinh sống'),
        ('Đã chuyển đi', 'Đã chuyển đi'),
        ('Đã qua đời', 'Đã qua đời'),
    ]
    ho_khau = models.ForeignKey(HoKhau, on_delete=models.CASCADE)
    ho_ten = models.CharField(max_length=100)
    ngay_sinh = models.DateField()
    gioi_tinh = models.CharField(max_length=3, choices=GIOI_TINH_CHOICES)
    ma_can_cuoc = models.CharField(max_length=15, unique=True)
    so_dien_thoai = models.CharField(max_length=15)
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='Đang sinh sống')
    thoi_gian_chuyen_den = models.DateField()
    thoi_gian_chuyen_di = models.DateField(null=True, blank=True)
    quan_he_voi_chu_ho = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.ho_ten} ({self.ma_can_cuoc})"

class TamTruTamVang(models.Model):
    LOAI_CHOICES = [('Tạm trú', 'Tạm trú'), ('Tạm vắng', 'Tạm vắng')]
    nhan_khau = models.ForeignKey(NhanKhau, on_delete=models.CASCADE)
    loai = models.CharField(max_length=10, choices=LOAI_CHOICES)
    thoi_gian_bat_dau = models.DateField()
    thoi_gian_ket_thuc = models.DateField()
    ly_do = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nhan_khau.ho_ten} - {self.loai} từ {self.thoi_gian_bat_dau} đến {self.thoi_gian_ket_thuc}"

class PhuongTien(models.Model):
    LOAI_CHOICES = [('Ô tô', 'Ô tô'), ('Xe máy', 'Xe máy')]
    ho_khau = models.ForeignKey(HoKhau, on_delete=models.CASCADE)
    loai_phuong_tien = models.CharField(max_length=10, choices=LOAI_CHOICES)
    bien_so = models.CharField(max_length=15)
    mau = models.CharField(max_length=10)
    mo_ta = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.loai_phuong_tien} - {self.bien_so} ({self.mau})"


class DanhSachPhiDongGop(models.Model):
    ten_phi = models.CharField(max_length=30, primary_key=True)
    so_tien_goi_y = models.IntegerField()
    noi_dung = models.TextField(null=True, blank=True)
    ngay_bat_dau = models.DateField(null=True, blank=True) 
    ngay_ket_thuc = models.DateField(null=True, blank=True)  

    def __str__(self):
        return self.ten_phi

class DongGopPhi(models.Model):
    phi = models.ForeignKey(DanhSachPhiDongGop, on_delete=models.CASCADE)
    ho_khau = models.ForeignKey(HoKhau, on_delete=models.CASCADE)
    ngay_dong = models.DateField()
    so_tien_dong = models.IntegerField()
    ghi_chu = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('phi', 'ho_khau', 'ngay_dong') 

    def __str__(self):
        return f"Đóng {self.so_tien_dong} cho {self.phi.ten_phi} - {self.ho_khau.so_can_ho}"

class Phi(models.Model):
    LOAI_CHOICES = [
        ('Dịch vụ', 'Dịch vụ'),
        ('Gửi xe', 'Gửi xe'),
        ('Quản lý', 'Quản lý'),
        ('Sinh hoạt', 'Sinh hoạt'),
    ]
    ho_khau = models.ForeignKey(HoKhau, on_delete=models.CASCADE)
    loai_phi = models.CharField(max_length=20, choices=LOAI_CHOICES)
    
    gia_phi_dich_vu = models.IntegerField(null=True, blank=True, default=16500)  
    gia_phi_quan_ly = models.IntegerField(null=True, blank=True, default=7000)  
    gia_phi_gui_xe_may = models.IntegerField(null=True, blank=True, default=70000) 
    gia_phi_gui_o_to = models.IntegerField(null=True, blank=True, default=1200000)  
    nam = models.IntegerField(default=timezone.now().year)

    def cap_nhat_phi(self):
        if not self.ho_khau.ngay_lap:
            return  # Nếu không có ngày lập, không làm gì

        ngay_lap = self.ho_khau.ngay_lap
        current_month = timezone.now().month
        start_month = ngay_lap.month + 1 if current_month > ngay_lap.month else ngay_lap.month

        for month in range(start_month, current_month + 1):  # Từ tháng sau ngày lập đến tháng hiện tại
            chi_tiet_phi, created = ChiTietPhiTheoThang.objects.get_or_create(
                phi=self, thang=month
            )

            # Tính phí cho các loại phí khác nhau
            if self.loai_phi == 'Dịch vụ':
                chi_tiet_phi.so_tien = self.tinh_phi_dich_vu()
            elif self.loai_phi == 'Quản lý':
                chi_tiet_phi.so_tien = self.tinh_phi_quan_ly()
            elif self.loai_phi == 'Gửi xe':
                chi_tiet_phi.so_tien = self.tinh_phi_gui_xe()
            elif self.loai_phi == 'Sinh hoạt':
                chi_tiet_phi.so_tien = self.tinh_phi_sinh_hoat()

            if chi_tiet_phi.so_tien is None:
                chi_tiet_phi.so_tien = 0.0  

            if chi_tiet_phi.da_dong:
                chi_tiet_phi.so_tien = 0.0

            chi_tiet_phi.save()  

    def tinh_phi_sinh_hoat(self):
        """Tính tổng phí sinh hoạt từ tiền điện, tiền nước, tiền internet"""
        if not self.ho_khau.ngay_lap:
            return 0
        current_month = timezone.now().month
        cap_nhat_phi = CapNhatPhiSinhHoat.objects.filter(ho_khau=self.ho_khau, thang=current_month, nam=self.nam).first()
        if cap_nhat_phi:
            return cap_nhat_phi.tien_dien + cap_nhat_phi.tien_nuoc + cap_nhat_phi.tien_internet
        return 0

    def tinh_phi_dich_vu(self):
        """Tính phí dịch vụ theo diện tích căn hộ"""
        if not self.ho_khau.ngay_lap:
            return 0
        if self.gia_phi_dich_vu:
            return self.ho_khau.dien_tich * self.gia_phi_dich_vu
        return 0

    def tinh_phi_quan_ly(self):
        """Tính phí quản lý theo diện tích căn hộ"""
        if not self.ho_khau.ngay_lap:
            return 0
        if self.gia_phi_quan_ly:
            return self.ho_khau.dien_tich * self.gia_phi_quan_ly
        return 0

    def tinh_phi_gui_xe(self):
        """Tính phí gửi xe (theo loại xe)"""
        if not self.ho_khau.ngay_lap:
            return 0
        phi_gui_xe = 0
        if self.gia_phi_gui_xe_may and self.ho_khau.so_xe_may:
            phi_gui_xe += self.ho_khau.so_xe_may * self.gia_phi_gui_xe_may  
        if self.gia_phi_gui_o_to and self.ho_khau.so_o_to:
            phi_gui_xe += self.ho_khau.so_o_to * self.gia_phi_gui_o_to  
        return phi_gui_xe


class ChiTietPhiTheoThang(models.Model):
    phi = models.ForeignKey(Phi, on_delete=models.CASCADE)
    thang = models.IntegerField()
    so_tien = models.IntegerField(default=0.0)
    da_dong = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.phi.ho_khau.so_can_ho} - {self.phi.loai_phi} tháng {self.thang} - {self.so_tien}"

    @property
    def tinh_tong_so_tien(self):
        """Tính tổng số tiền của loại phí này cho tháng hiện tại"""
        if self.phi.loai_phi == 'Sinh hoạt':
            return self.phi.tinh_phi_sinh_hoat()
        elif self.phi.loai_phi == 'Dịch vụ':
            return self.phi.tinh_phi_dich_vu()
        elif self.phi.loai_phi == 'Quản lý':
            return self.phi.tinh_phi_quan_ly()
        elif self.phi.loai_phi == 'Gửi xe':
            return self.phi.tinh_phi_gui_xe()
        return 0

    def save(self, *args, **kwargs):
        """Override phương thức save để tự động đặt so_tien về 0 khi da_dong = True"""
        if self.da_dong:
            self.so_tien = 0.0  # Đặt số tiền về 0 khi đã thanh toán
        super().save(*args, **kwargs)

class CapNhatPhiSinhHoat(models.Model):
    ho_khau = models.ForeignKey(HoKhau, on_delete=models.CASCADE)
    tien_dien = models.IntegerField(null=True, blank=True)
    tien_nuoc = models.IntegerField(null=True, blank=True)
    tien_internet = models.IntegerField(null=True, blank=True)
    thang = models.IntegerField()
    nam = models.IntegerField(default=timezone.now().year)

    class Meta:
        unique_together = ('ho_khau', 'thang', 'nam') 

    def __str__(self):
        return f"Phí sinh hoạt {self.ho_khau.so_can_ho} tháng {self.thang} năm {self.nam}"
    
    def save(self, *args, **kwargs):
        """Override phương thức save để tự động cập nhật bảng Phi và ChiTietPhiTheoThang khi có thay đổi"""
        super().save(*args, **kwargs)  # Save CapNhatPhiSinhHoat instance

        phi_records = Phi.objects.filter(ho_khau=self.ho_khau, loai_phi='Sinh hoạt')
        for phi in phi_records:
            chi_tiet_phi, created = ChiTietPhiTheoThang.objects.get_or_create(
                phi=phi, thang=self.thang
            )

            chi_tiet_phi.so_tien = self.tien_dien + self.tien_nuoc + self.tien_internet

            if chi_tiet_phi.da_dong:
                chi_tiet_phi.so_tien = 0.0

            chi_tiet_phi.save()
