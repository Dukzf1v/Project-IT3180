from django.db import models

class NguoiDung(models.Model):
    VAI_TRO_CHOICES = [
        ('Quản trị hệ thống', 'Quản trị hệ thống'),
        ('Quản lý chung cư', 'Quản lý chung cư'),
        ('Kế toán', 'Kế toán'),
    ]
    vai_tro = models.CharField(max_length=30, choices=VAI_TRO_CHOICES)
    so_dien_thoai = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return f"{self.vai_tro} - {self.email}"

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
    thoi_gian_bat_dau_o = models.DateField(null=True, blank=True)
    thoi_gian_ket_thuc_o = models.DateField(null=True, blank=True)
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES)

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
    ma_can_cuoc = models.CharField(max_length=15)
    so_dien_thoai = models.CharField(max_length=15)
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES)
    thoi_gian_chuyen_den = models.DateField()
    thoi_gian_chuyen_di = models.DateField(null=True, blank=True)
    quan_he_voi_chu_ho = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.ho_ten} ({self.ma_can_cuoc})"

class LichSuNhanKhau(models.Model):
    HANH_DONG_CHOICES = [
        ('Chuyển đến', 'Chuyển đến'),
        ('Chuyển đi', 'Chuyển đi'),
        ('Qua đời', 'Qua đời'),
        ('Cập nhật thông tin', 'Cập nhật thông tin'),
    ]
    nhan_khau = models.ForeignKey(NhanKhau, on_delete=models.CASCADE)
    thoi_gian = models.DateField()
    hanh_dong = models.CharField(max_length=30, choices=HANH_DONG_CHOICES)
    ghi_chu = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Lịch sử {self.nhan_khau.ho_ten} - {self.hanh_dong} ngày {self.thoi_gian}"

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
    bien_so = models.CharField(max_length=50)
    mau = models.CharField(max_length=50)
    mo_ta = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.loai_phuong_tien} - {self.bien_so} ({self.mau})"

class CapNhatPhiSinhHoat(models.Model):
    ho_khau = models.ForeignKey(HoKhau, on_delete=models.CASCADE)
    tien_dien = models.FloatField(null=True, blank=True)
    tien_nuoc = models.FloatField(null=True, blank=True)
    tien_internet = models.FloatField(null=True, blank=True)
    thang = models.IntegerField()
    nam = models.IntegerField()

    def __str__(self):
        return f"Phí sinh hoạt {self.ho_khau.so_can_ho} tháng {self.thang} năm {self.nam}"

class DanhSachPhiDongGop(models.Model):
    ten_phi = models.CharField(max_length=30, primary_key=True)
    so_tien_goi_y = models.FloatField()

    def __str__(self):
        return self.ten_phi

class DongGopPhi(models.Model):
    phi = models.ForeignKey(DanhSachPhiDongGop, on_delete=models.CASCADE)
    ho_khau = models.ForeignKey(HoKhau, on_delete=models.CASCADE)
    ngay_dong = models.DateField()
    so_tien_dong = models.FloatField()
    ghi_chu = models.TextField(null=True, blank=True)

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
    gia_phi = models.FloatField()
    tien_nop_moi_thang = models.FloatField()
    nam = models.IntegerField()

    def __str__(self):
        return f"{self.ho_khau.so_can_ho} - {self.loai_phi} năm {self.nam}"

class ChiTietPhiTheoThang(models.Model):
    phi = models.ForeignKey(Phi, on_delete=models.CASCADE)
    thang = models.IntegerField()
    so_tien = models.FloatField()

    def __str__(self):
        return f"{self.phi.ho_khau.so_can_ho} - {self.phi.loai_phi} tháng {self.thang} - {self.so_tien}"

class PhanAnh(models.Model):
    TRANG_THAI_CHOICES = [
        ('Chưa xử lý', 'Chưa xử lý'),
        ('Đang xử lý', 'Đang xử lý'),
        ('Đã xử lý', 'Đã xử lý'),
    ]
    nhan_khau = models.ForeignKey(NhanKhau, on_delete=models.CASCADE)
    ngay_gui = models.DateField()
    noi_dung = models.TextField()
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='Chưa xử lý')
    phan_hoi = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Phản ánh của {self.nhan_khau.ho_ten} ngày {self.ngay_gui} - {self.trang_thai}"
